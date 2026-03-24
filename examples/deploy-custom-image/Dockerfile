ARG SOURCE_IMAGE

FROM ${SOURCE_IMAGE}
# Pin to a specific tag/digest when reproducibility is required
COPY --from=ccr.ccs.tencentyun.com/ags-image/envd:latest --chmod=755 /usr/bin/envd /usr/bin/envd
