// cdp_proxy.go — Chrome DevTools Protocol proxy for AGS sandbox
//
// Runs inside the sandbox, listens on 0.0.0.0:9222, forwards to Chrome at
// 127.0.0.1:1337.
//
// Build (static binary, no CGO):
//
//	CGO_ENABLED=0 GOOS=linux GOARCH=amd64 \
//	  go build -ldflags="-s -w" -o cdp_proxy cdp_proxy.go
//
// Compress with upx (recommended, ~40% of original size):
//
//	upx --best cdp_proxy
package main

import (
	"bytes"
	"flag"
	"io"
	"log"
	"net"
	"net/http"
	"net/http/httputil"
	"regexp"
	"strconv"
	"strings"
)

var (
	listenAddr = flag.String("listen", ":9222", "local listen address (host:port or :port)")
	targetAddr = flag.String("target", "127.0.0.1:1337", "Chrome CDP target address")

	// Match ws:// or wss:// URLs that reference the Chrome port (:1337).
	// Character class [^/\s"] mirrors Python's [^/\s\"] to stop at path boundaries.
	wsURLRe = regexp.MustCompile(`wss?://[^/\s"]+:1337`)
)

// rewriteJSONBody rewrites Chrome CDP port references in /json* HTTP responses.
//
// Two-step rewrite (matches Python cdp_proxy.py behaviour exactly):
//  1. Replace ws[s]://host:1337   → ws://localhost<localPort>  (covers webSocketDebuggerUrl)
//  2. Replace localhost:1337      → localhost<localPort>        (covers devtoolsFrontendUrl)
func rewriteJSONBody(body []byte, localPort string) []byte {
	s := string(body)
	s = wsURLRe.ReplaceAllString(s, "ws://localhost"+localPort)
	s = strings.ReplaceAll(s, "localhost:1337", "localhost"+localPort)
	return []byte(s)
}

func main() {
	flag.Parse()

	// Normalise listen address: accept "9222" or ":9222" or "0.0.0.0:9222".
	listenOn := *listenAddr
	if !strings.Contains(listenOn, ":") {
		listenOn = ":" + listenOn
	}
	_, port, err := net.SplitHostPort(listenOn)
	if err != nil {
		log.Fatalf("invalid listen address %q: %v", listenOn, err)
	}
	urlPort := ":" + port // e.g. ":9222" — used in URL rewriting

	proxy := &httputil.ReverseProxy{
		Director: func(req *http.Request) {
			req.URL.Scheme = "http"
			req.URL.Host = *targetAddr
			// Set Host to "localhost:1337" to match Python cdp_proxy.py behaviour
			// and satisfy Chrome's DNS-rebinding protection.
			req.Host = "localhost:1337"
		},
		ModifyResponse: func(resp *http.Response) error {
			if !strings.HasPrefix(resp.Request.URL.Path, "/json") {
				return nil
			}
			// defer closes the *original* body: Go defers evaluate the receiver
			// at the defer statement, before resp.Body is reassigned below.
			defer resp.Body.Close()
			body, err := io.ReadAll(resp.Body)
			if err != nil {
				return err
			}
			rewritten := rewriteJSONBody(body, urlPort)
			// Update both the header map and the struct field so downstream
			// consumers (and the wire) see the correct Content-Length.
			resp.Header.Set("Content-Length", strconv.Itoa(len(rewritten)))
			resp.ContentLength = int64(len(rewritten))
			resp.Body = io.NopCloser(bytes.NewReader(rewritten))
			return nil
		},
	}

	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		if strings.EqualFold(r.Header.Get("Upgrade"), "websocket") {
			tunnelWebSocket(w, r, *targetAddr)
			return
		}
		proxy.ServeHTTP(w, r)
	})

	log.Printf("cdp_proxy listening on %s -> %s", listenOn, *targetAddr)
	log.Fatal(http.ListenAndServe(listenOn, nil))
}

// tunnelWebSocket transparently tunnels a WebSocket connection at the TCP level.
//
// Unlike a frame-level proxy this approach:
//   - Preserves all WebSocket extensions (e.g. permessage-deflate)
//   - Forwards Ping/Pong frames without parsing them
//   - Has lower latency (no double frame encode/decode)
func tunnelWebSocket(w http.ResponseWriter, r *http.Request, target string) {
	dst, err := net.Dial("tcp", target)
	if err != nil {
		http.Error(w, "dial failed: "+err.Error(), http.StatusBadGateway)
		return
	}
	defer dst.Close()

	hijacker, ok := w.(http.Hijacker)
	if !ok {
		http.Error(w, "hijack not supported", http.StatusInternalServerError)
		return
	}
	src, bufrw, err := hijacker.Hijack()
	if err != nil {
		// Hijack failed: connection ownership was NOT transferred, w is still valid.
		http.Error(w, "hijack failed: "+err.Error(), http.StatusInternalServerError)
		return
	}
	defer src.Close()

	// Rewrite Host header to match what Chrome expects, then forward the full
	// HTTP/1.1 Upgrade request (including Connection: Upgrade, Sec-WebSocket-*).
	// r.Write() serialises directly to the TCP stream, bypassing http.Transport,
	// so hop-by-hop headers are preserved intentionally.
	r.Host = "localhost:1337"
	if err := r.Write(dst); err != nil {
		log.Printf("tunnelWebSocket: write upgrade request failed: %v", err)
		return // deferred Close()s clean up both sides
	}

	// Bidirectional copy.
	// bufrw.Reader drains any bytes already buffered by the HTTP server before
	// switching to raw reads from src.
	// Channel capacity 2 ensures the second goroutine can send without blocking
	// after the first one finishes and deferred Close()s fire.
	done := make(chan struct{}, 2)
	go func() { io.Copy(dst, bufrw.Reader); done <- struct{}{} }()
	go func() { io.Copy(src, dst); done <- struct{}{} }()
	<-done
	// Deferred dst.Close() + src.Close() cause the other goroutine's io.Copy
	// to return an error and exit cleanly.
}
