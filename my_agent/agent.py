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
# Note: McpToolset sẽ load tất cả tools từ server
# Optimization: Agent instruction đã hướng dẫn chỉ dùng 8 tools cần thiết
github_toolset = McpToolset(connection_params=github_mcp_params)

# Khởi tạo tools - NO LONGER PASS RULES (rules embedded in instruction)
security_scanner = create_security_scanner_function()
rules_checker = create_rules_checker_function()
combined_analyzer = create_combined_analyzer_function()  # PREFERRED: Use this instead of separate calls

# Load rules into memory once
rules_file = Path(__file__).parent.parent / "rules" / "company_rules_compact.md"
security_rules_file = Path(__file__).parent.parent / "rules" / "security_rules_compact.md"

with open(security_rules_file, 'r', encoding='utf-8') as f:
    SECURITY_RULES_TEXT = f.read()
    
with open(rules_file, 'r', encoding='utf-8') as f:
    COMPANY_RULES_TEXT = f.read()

# AGENT INSTRUCTION - OPTIMIZED
AGENT_INSTRUCTION = f"""Code Review Assistant - phân tích security & coding standards. Trả lời bằng TIẾNG VIỆT.

**RULES EMBEDDED (use these for all analysis):**

<security_rules>
{SECURITY_RULES_TEXT}
</security_rules>

<company_rules>
{COMPANY_RULES_TEXT}
</company_rules>

---

**2 Use Cases:**
1. **PR Review**: "review PR #123 in owner/repo" → get_pr_details/files → scan → create_review
2. **Code Snippet**: User paste code → detect language → scan → report

**Workflow:**

**For PR:**
1. get_pr_details, get_pr_files, get_file_content
2. **For EACH file separately**:
   - **PREFERRED**: Call analyze_code_complete(file_content, file_path, language) - ONE call for both security + rules
   - **IMPORTANT**: Wait 2-3 seconds between files to avoid rate limit (429 errors)
   - **Store results per file** (don't merge yet)
3. **Organize by file**: Group findings by file path
4. **Generate report**: Per-file structure (see format below)
5. Post: CRITICAL/HIGH → create_review_comment per line, Summary → create_review

**Token Optimization:**
- Use analyze_code_complete() instead of scan_code_security() + check_company_rules() (saves 50%)
- Keep conversation focused: only relevant file context

**Rate Limiting:**
- If you get 429 error: STOP immediately, wait 5 seconds, then retry
- Between files: always wait 2-3 seconds
- Don't analyze all files in parallel - do them sequentially with delays

**For Snippet:**
1. Detect language (php, python, js, java, etc.)
2. Call both tools: scan_code_security() + check_company_rules()
3. Return report immediately (single file format)

**Report Format (Per-File Structure):**
```markdown
# Code Review Report - PR #123

## 📊 Tổng Quan
- **Files reviewed**: 5
- **Total issues**: 23
  - 🔴 CRITICAL: 4
  - 🟠 HIGH: 6
  - 🟡 MEDIUM: 10
  - 🟢 LOW: 3

---

## 📁 File 1: `src/controllers/UserController.php`

### Summary
- 🔐 Security: 2 CRITICAL, 1 HIGH
- 📋 Rules: 3 MEDIUM, 1 LOW

### 🔐 Security Issues

#### 🔴 CRITICAL: SQL Injection (Line 15)
**Vấn đề**: Nối chuỗi trực tiếp vào SQL
**Impact**: Attacker bypass auth, xóa data
**Code**: 
```php
$query = "SELECT * FROM users WHERE id = " . $id;
```
**Fix**:
```php
$stmt = $pdo->prepare("SELECT * FROM users WHERE id = ?");
$stmt->execute([$id]);
```

#### 🟠 HIGH: Missing Auth (Line 45)
**Vấn đề**: deleteUser() không check auth
**Fix**: Add `$this->authorize('delete', $user);`

### 📋 Coding Standards

#### 🟡 MEDIUM: Naming Convention (Line 10)
**Rule**: R5 - Class names phải PascalCase
**Code**: `class userController`
**Fix**: `class UserController`

---

## 📁 File 2: `src/models/Order.php`

### Summary
- 🔐 Security: 1 MEDIUM (N+1 query)
- 📋 Rules: 2 MEDIUM, 1 LOW

### 🔐 Security Issues

#### 🟡 MEDIUM: N+1 Query (Line 67)
**Vấn đề**: Loop qua users, query orders riêng
**Fix**: `User::with('orders')->get()`

### 📋 Coding Standards

#### 🟡 MEDIUM: Missing PHPDoc (Line 25)
**Rule**: R30 - Function phải có PHPDoc
**Fix**: Add `@param`, `@return`, `@author`

---

## ✅ Tổng Kết

**Decision**: ❌ REQUEST CHANGES

**Critical Actions Required**:
1. Fix SQL injection in UserController.php (Line 15)
2. Add authentication check in deleteUser() (Line 45)
3. Remove hardcoded API key in config.php (Line 8)

**Recommendations**:
- Fix all CRITICAL issues before merge
- Address HIGH issues in follow-up
- MEDIUM/LOW can be addressed gradually
```

**Rules:**
- Always call BOTH tools (security + rules) **per file**
- **Keep findings organized by file** - don't merge
- Report format: Per-file structure with file summary
- Severity: CRITICAL > HIGH > MEDIUM > LOW
- Fix must have code example
- If file clean: "✅ No issues" for that file
- Overall decision based on highest severity across all files
"""

# Định nghĩa Code Review Agent - simple & clean
root_agent = Agent(
    model="gemini-2.0-flash",
    name="code_review_assistant",
    instruction=AGENT_INSTRUCTION,
    tools=[github_toolset, combined_analyzer, security_scanner, rules_checker]
    # Note: combined_analyzer is PREFERRED (50% token reduction vs separate calls)
    # security_scanner & rules_checker kept for backward compatibility
)
