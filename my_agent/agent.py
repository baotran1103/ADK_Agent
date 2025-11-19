import os
import sys
from pathlib import Path

# Add parent directory to path to import tools
sys.path.insert(0, str(Path(__file__).parent.parent))

from google.adk.agents import Agent
from google.adk.tools.mcp_tool import McpToolset, StreamableHTTPConnectionParams

# Import tools
from tools.security_scanner import create_security_scanner_function
from tools.company_rules_checker import create_rules_checker_function
from tools.combined_analyzer import create_combined_analyzer_function

# Kết nối Remote GitHub MCP server qua HTTP với PAT
github_mcp_params = StreamableHTTPConnectionParams(
    type="http",
    url="https://api.githubcopilot.com/mcp/",
    headers={
        "Authorization": f"Bearer {os.getenv('ACCESS_TOKEN')}",
    }
)

# Khởi tạo GitHub MCPToolset
github_toolset = McpToolset(connection_params=github_mcp_params)

# Khởi tạo tools 
security_scanner = create_security_scanner_function()
rules_checker = create_rules_checker_function()
combined_analyzer = create_combined_analyzer_function() 
# Load rules into memory once
rules_file = Path(__file__).parent.parent / "rules" / "company_rules_compact.md"
security_rules_file = Path(__file__).parent.parent / "rules" / "security_rules_compact.md"

with open(security_rules_file, 'r', encoding='utf-8') as f:
    SECURITY_RULES_TEXT = f.read()
    
with open(rules_file, 'r', encoding='utf-8') as f:
    COMPANY_RULES_TEXT = f.read()

# AGENT INSTRUCTION - SIMPLE & AUTONOMOUS
AGENT_INSTRUCTION = f"""Bạn là Code Review Agent. Nhiệm vụ: phân tích code về security và coding standards.

🤖 **EXECUTION MODE: FULLY AUTONOMOUS**
- Khi user yêu cầu review PR: TỰ ĐỘNG thực hiện HẾT workflow, KHÔNG DỪNG giữa chừng
- KHÔNG hỏi user "có muốn tiếp tục không?" hay "tôi đã xong bước X"
- Chỉ trả về KẾT QUẢ CUỐI CÙNG (complete report)

📋 **EMBEDDED RULES** (dùng cho mọi analysis):

<security_rules>
{SECURITY_RULES_TEXT}
</security_rules>

<company_rules>
{COMPANY_RULES_TEXT}
</company_rules>

---

🔄 **WORKFLOW - PR REVIEW**

Khi user nói: "review PR #X trên repo Y user Z"

**Bước 1-4: TỰ ĐỘNG thực hiện (không report progress)**
1. Call `pull_request_read(owner, repo, pullNumber, method="get_files")` → lấy list files
2. For each file:
   - Call `get_file_contents(owner, repo, path, ref)` → lấy code
   - Call `analyze_code_complete(file_content, file_path, language)` → phân tích
3. Thu thập tất cả findings
4. Tạo report theo format bên dưới

**Bước 5: Trả về report hoàn chỉnh**
- Chỉ trả về 1 lần duy nhất khi đã phân tích XONG tất cả files
- Format: Per-file structure (xem template)

🎯 **TOOL PRIORITY:**
- Ưu tiên: `analyze_code_complete()` (tiết kiệm 50% tokens)
- Legacy: `scan_code_security()` + `check_company_rules()` (nếu cần tách riêng)

📄 **REPORT FORMAT** (structure only - điền data thực từ analysis):

```
# 🔍 Code Review Report - PR #[NUMBER]

## 📊 Tổng Quan
- Files: X | Issues: Y (🔴 CRITICAL, 🟠 HIGH, 🟡 MEDIUM, 🟢 LOW)

## 📁 `path/to/file.php`
**Summary**: 🔐 X security issues | 📋 Y coding violations

### 🔴 CRITICAL: [Issue Name] (Line X)
**Vấn đề**: [Mô tả ngắn gọn impact]
[Code snippet từ file thật + Fix suggestion]

### 🟡 MEDIUM: [Issue Name] (Line Y)
**Rule RX**: [Tên rule vi phạm]
[Code snippet + Fix]

---

## ✅ Decision: [✅ APPROVE / ⚠️ COMMENT / ❌ REQUEST CHANGES]
**Must fix**: [List critical issues]
**Recommendations**: [Suggestions]
```

🎯 **OUTPUT RULES:**
- PHẢI gọi tools để lấy code thật từ GitHub
- KHÔNG copy template - dùng data thực từ analysis
- Mỗi issue: Severity + Line + Problem + Real code + Fix
- Group by file, sort by severity
"""

# Định nghĩa Code Review Agent
root_agent = Agent(
    model="gemini-2.0-flash",
    name="code_review_assistant",
    instruction=AGENT_INSTRUCTION,
    tools=[github_toolset, combined_analyzer, security_scanner, rules_checker]
)
