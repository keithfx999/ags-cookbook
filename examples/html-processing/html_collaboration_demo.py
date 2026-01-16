#!/usr/bin/env python3
"""
Agent Sandbox沙箱协作演示
展示Code和Browser沙箱的协作能力：HTML创建 → 渲染截图 → 代码编辑 → 再次渲染对比
"""

import os
import time
from datetime import datetime

# 设置环境变量（可通过环境变量预先设置，或在此处直接修改）
if not os.getenv('E2B_DOMAIN'):
    os.environ['E2B_DOMAIN'] = 'tencentags.com'
if not os.getenv('E2B_API_KEY'):
    os.environ['E2B_API_KEY'] = 'your_api_key'

def create_initial_html(output_dir):
    """创建初始HTML文件"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Agent Sandbox Demo</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            text-align: center;
            padding: 50px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
            margin: 0;
        }}
        .container {{
            background: rgba(255, 255, 255, 0.1);
            padding: 40px;
            border-radius: 15px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            max-width: 600px;
            margin: 0 auto;
        }}
        h1 {{
            color: #fff;
            font-size: 3em;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }}
        .timestamp {{
            font-size: 1.2em;
            margin-top: 20px;
            opacity: 0.8;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Welcome to Agent Sandbox</h1>
        <p class="timestamp">Created: {timestamp}</p>
    </div>
</body>
</html>"""
    
    html_file_path = os.path.join(output_dir, "demo.html")
    with open(html_file_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"初始HTML文件已创建: {html_file_path}")
    return html_content, html_file_path

def get_html_editor_code():
    """返回HTML编辑器的代码"""
    return '''
import re
from datetime import datetime

print("🔧 Code Interpreter开始处理HTML文件...")

# 读取HTML文件
try:
    with open('/tmp/demo.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    print("HTML文件读取成功")
except Exception as e:
    print(f"读取HTML文件失败: {e}")
    exit(1)

print("原始HTML内容预览:")
print(html_content[:200] + "..." if len(html_content) > 200 else html_content)

# 在</body>标签前添加新内容
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
new_section = f"""
        <div style="margin-top: 30px; padding: 20px; background: rgba(255, 255, 255, 0.2); border-radius: 10px; border: 2px solid rgba(255, 255, 255, 0.3);">
            <h2 style="color: #ffeb3b; margin-bottom: 15px;">Edit by Code Interpreter Sandbox</h2>
            <p style="font-size: 1.1em; line-height: 1.6;">
                This content was dynamically added by the Code Interpreter sandbox!<br>
                Processing completed at: {current_time}
            </p>
            </div>
        </div>"""

# 在</div></body>之前插入新内容
if '</div>' in html_content and '</body>' in html_content:
    # 找到最后一个</div>标签的位置（应该是container的结束标签）
    last_div_pos = html_content.rfind('</div>')
    if last_div_pos != -1:
        # 在container结束标签前插入新内容
        modified_html = html_content[:last_div_pos] + new_section + '\\n    ' + html_content[last_div_pos:]
        print("HTML内容修改成功")
    else:
        print("未找到合适的插入位置")
        exit(1)
else:
    print("HTML结构不符合预期")
    exit(1)

# 保存修改后的HTML
try:
    with open('/tmp/demo_edited.html', 'w', encoding='utf-8') as f:
        f.write(modified_html)
    print("修改后的HTML已保存: demo_edited.html")
except Exception as e:
    print(f"保存HTML文件失败: {e}")
    exit(1)

print("修改后HTML内容预览:")
print(modified_html[:300] + "..." if len(modified_html) > 300 else modified_html)

print("Code Interpreter HTML编辑任务完成!")
print("修改统计:")
print(f"   原始文件大小: {len(html_content)} 字符")
print(f"   修改后大小: {len(modified_html)} 字符")
print(f"   新增内容: {len(modified_html) - len(html_content)} 字符")
'''

async def browser_render_and_screenshot(sandbox, html_file, output_name, output_dir):
    """使用Browser沙箱渲染HTML并截图"""
    from playwright.async_api import async_playwright
    
    # 构建CDP连接URL
    cdp_url = f"https://{sandbox.get_host(9000)}/cdp"
    
    async with async_playwright() as playwright:
        # 连接到Browser沙箱
        browser = await playwright.chromium.connect_over_cdp(
            cdp_url, 
            headers={"X-Access-Token": str(sandbox._envd_access_token)}
        )
        context = browser.contexts[0]
        page = context.pages[0]
        
        # 打开HTML文件
        file_url = f"file:///home/user/{html_file}"
        await page.goto(file_url)
        await page.wait_for_load_state("networkidle")
        
        # 截图
        screenshot_bytes = await page.screenshot(full_page=True)
        
        # 保存截图到沙箱
        sandbox.files.write(f"{output_name}.png", screenshot_bytes)
        
        # 直接保存到输出目录
        screenshot_path = os.path.join(output_dir, f"{output_name}.png")
        with open(screenshot_path, "wb") as f:
            f.write(screenshot_bytes)
        
        print(f"截图已保存: {screenshot_path}")
        return await page.title()

def html_collaboration_demo():
    """HTML协作处理演示"""
    try:
        print("开始HTML协作处理演示")
        print("=" * 50)
        
        # 步骤0: 创建输出目录
        output_dir = './html_collaboration_output'
        os.makedirs(output_dir, exist_ok=True)
        print(f"输出目录已创建: {output_dir}")
        
        # 步骤1: 创建初始HTML文件
        print("\n步骤1: 创建初始HTML文件")
        print("-" * 30)
        initial_html, html_file_path = create_initial_html(output_dir)
        
        # 步骤2: 创建Browser沙箱并首次渲染
        print("\n步骤2: 创建Browser沙箱并首次渲染")
        print("-" * 30)
        
        from e2b import Sandbox
        browser_sandbox = Sandbox.create(template="browser-v1", timeout=1800)
        print(f"Browser沙箱已创建: {browser_sandbox.sandbox_id}")
        
        # 上传HTML到Browser沙箱
        with open(html_file_path, "r", encoding="utf-8") as f:
            browser_sandbox.files.write("demo.html", f)
        print("HTML文件已上传到Browser沙箱")
        
        # 首次截图
        import asyncio
        title1 = asyncio.run(browser_render_and_screenshot(
            browser_sandbox, "demo.html", "screenshot_before", output_dir
        ))
        print(f"首次渲染完成，页面标题: {title1}")
        
        # 步骤3: 创建Code沙箱并编辑HTML
        print("\n步骤3: 创建Code沙箱并编辑HTML")
        print("-" * 30)
        
        from e2b_code_interpreter import Sandbox as CodeSandbox
        code_sandbox = CodeSandbox.create(template="code-interpreter-v1", timeout=1800)
        print(f"Code沙箱已创建: {code_sandbox.sandbox_id}")
        
        # 上传HTML到Code沙箱
        with open(html_file_path, "r", encoding="utf-8") as f:
            code_sandbox.files.write("/tmp/demo.html", f)
        print("HTML文件已上传到Code沙箱")
        
        # 执行HTML编辑代码
        print("开始执行HTML编辑...")
        result = code_sandbox.run_code(
            get_html_editor_code(),
            on_stdout=lambda data: print(f"[Code] {data}"),
            on_stderr=lambda data: print(f"[Code Error] {data}")
        )
        
        if result.error:
            print(f"Code执行出错: {result.error}")
            return
        
        # 从Code沙箱下载编辑后的HTML
        try:
            edited_html_content = code_sandbox.files.read("/tmp/demo_edited.html")
            edited_html_path = os.path.join(output_dir, "demo_edited.html")
            with open(edited_html_path, "w", encoding="utf-8") as f:
                f.write(edited_html_content)
            print(f"编辑后的HTML已下载到: {edited_html_path}")
        except Exception as e:
            print(f"下载编辑后HTML失败: {e}")
            return
        
        # 步骤4: 上传编辑后的HTML到Browser沙箱并再次渲染
        print("\n步骤4: 上传编辑后HTML并再次渲染")
        print("-" * 30)
        
        # 上传编辑后的HTML到Browser沙箱
        with open(edited_html_path, "r", encoding="utf-8") as f:
            browser_sandbox.files.write("demo_edited.html", f)
        print("编辑后HTML已上传到Browser沙箱")
        
        # 第二次截图
        title2 = asyncio.run(browser_render_and_screenshot(
            browser_sandbox, "demo_edited.html", "screenshot_after", output_dir
        ))
        print(f"第二次渲染完成，页面标题: {title2}")
        
        # 步骤5: 展示协作成果
        print("\nHTML协作处理演示完成!")
        print("=" * 50)
        print("协作成果总结:")
        print(f"   Browser沙箱ID: {browser_sandbox.sandbox_id}")
        print(f"   Code沙箱ID: {code_sandbox.sandbox_id}")
        print(f"   原始页面标题: {title1}")
        print(f"   编辑后页面标题: {title2}")
        print("   生成对比截图: 2张")
        print("   输出文件: 4个")
        
        print("\n协作流程展示:")
        print("   本地创建HTML → Browser沙箱渲染 → 截图1")
        print("   HTML传输到Code沙箱 → 程序化编辑 → 生成新版本")
        print("   新版本传回Browser沙箱 → 再次渲染 → 截图2")
        
        print(f"\n请查看 {output_dir} 目录中的所有文件!")
        print("   所有文件都直接生成在输出目录中，无需移动！")
        
    except Exception as e:
        print(f"演示过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # 清理资源
        try:
            if 'browser_sandbox' in locals():
                browser_sandbox.kill()
                print("Browser沙箱已关闭")
        except:
            pass
        
        try:
            if 'code_sandbox' in locals():
                code_sandbox.kill()
                print("Code沙箱已关闭")
        except:
            pass

if __name__ == "__main__":
    html_collaboration_demo()
