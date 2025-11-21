# 🎯 Hybrid Code Review Agent - Architecture

## 📊 **Token Optimization Strategy**

### **Before (Combined Analyzer)**
- Single tool: `analyze_code_complete`
- Gemini AI analyzes everything
- Token usage: ~30-40K per file

### **After (Hybrid Approach)**
- Tool 1: `analyze_with_gemini` - Fast AI (all rules)
- Tool 2: `scan_with_semgrep` - Deep verify (CRITICAL/HIGH only)
- Token usage: ~25-35K per file (saves 15-20%)

**Why more efficient:**
1. Semgrep runs locally (no token cost for scan)
2. Only verify CRITICAL/HIGH (skip 80% of files)
3. Semgrep returns minimal JSON (vs full prompt)

---

## 🔄 **Workflow**

```
┌─────────────────────────────────────────────────────┐
│ Step 1: Get PR Files (GitHub MCP)                   │
│ └─> branch_name, files[]                            │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ Step 2: Get File Content (GitHub MCP)               │
│ └─> file_content (use ref=branch_name)              │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ Step 3: Gemini AI Analysis (FAST)                   │
│ Tool: analyze_with_gemini()                          │
│ └─> All issues: Security + Company Rules (R1-R43)   │
└─────────────────────────────────────────────────────┘
                        ↓
                   [Decision]
                  Has CRITICAL/HIGH
                  security issues?
                  /            \
              YES /              \ NO
                 /                \
                ↓                  ↓
┌─────────────────────────────┐  Skip to Step 5
│ Step 4: Semgrep Verify      │
│ Tool: scan_with_semgrep()   │
│ └─> Verified vulnerabilities│
└─────────────────────────────┘
                ↓
┌─────────────────────────────────────────────────────┐
│ Step 5: Merge & Organize                             │
│ └─> Gemini + Semgrep (dedupe, sort by severity)     │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ Step 6: Verify Fixes (Google Search)                │
│ └─> Only CRITICAL/HIGH: Official docs, OWASP        │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ Step 7: Generate Report (Vietnamese)                │
│ └─> Sorted by severity, with sources                │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ Step 8: Slack Notification (if CRITICAL ≥ 1)        │
│ └─> Alert team with top issues                      │
└─────────────────────────────────────────────────────┘
```

---

## 🛠️ **Tools**

### **1. GitHub MCP Toolset**
```python
github_toolset
├─ pull_request_read(owner, repo, pullNumber, method="get_files")
└─ get_file_contents(owner, repo, path, ref=branch_name)
```
**Purpose:** Get PR data and file content

---

### **2. Gemini AI Analyzer**
```python
analyze_with_gemini(file_content, file_path, language)
```

**What it does:**
- AI analysis using embedded rules
- Checks: Security (11 categories) + Company rules (R1-R43)
- Fast: No external API

**Returns:**
```json
{
  "action": "ANALYZE_WITH_RULES",
  "code": "<?php ... ?>",
  "instruction": "Analyze using embedded rules"
}
```

**Token cost:** ~25K per file

---

### **3. Semgrep Scanner**
```python
scan_with_semgrep(file_content, file_path, language)
```

**What it does:**
- Runs Semgrep CLI locally
- Deep security scan
- Only called for CRITICAL/HIGH verification

**Returns:**
```json
{
  "status": "success",
  "issues": [
    {
      "rule_id": "php.lang.security.sqli",
      "severity": "ERROR",
      "line": 45,
      "message": "SQL injection detected"
    }
  ]
}
```

**Token cost:** ~5K (minimal JSON)
**Time cost:** 5-10 seconds per file

---

### **4. Slack Notifier**
```python
send_slack_notification(message, severity)
```

**What it does:**
- Sends webhook to Slack
- Only if CRITICAL ≥ 1
- Includes: PR link, top issues

**Token cost:** ~1K

---

## 💾 **Token Savings Calculation**

### **Example: 2-file PR with 1 CRITICAL issue**

**Old approach (combined_analyzer):**
```
File 1: 35K tokens (Gemini analyzes everything)
File 2: 35K tokens (Gemini analyzes everything)
Total: 70K tokens
```

**New approach (hybrid):**
```
File 1: 25K (Gemini) + 5K (Semgrep verify) = 30K
File 2: 25K (Gemini only, no CRITICAL) = 25K
Total: 55K tokens
Savings: 15K (21%)
```

**Example: 5-file PR with 2 CRITICAL issues**
```
Old: 5 × 35K = 175K
New: 2 × 30K + 3 × 25K = 135K
Savings: 40K (23%)
```

---

## 🎯 **Key Benefits**

### **1. Accuracy**
- ✅ Gemini: Fast, comprehensive (all rules)
- ✅ Semgrep: Industry-standard SAST tool
- ✅ Combined: Best of AI + traditional tools

### **2. Performance**
- ✅ Gemini: Instant analysis
- ✅ Semgrep: Only for high-priority issues
- ✅ Parallel: Can run on multiple files

### **3. Token Efficiency**
- ✅ Gemini: Optimized with embedded rules
- ✅ Semgrep: Local execution (no token cost)
- ✅ Conditional: Skip Semgrep when not needed

### **4. Maintainability**
- ✅ Clear separation of concerns
- ✅ Easy to add more tools (SonarQube, etc.)
- ✅ Instruction in external file

---

## 📝 **Rules**

### **Tool Call Limits (NO DUPLICATES)**
- `pull_request_read`: **1 call per PR**
- `get_file_contents`: **1 call per file**
- `analyze_with_gemini`: **1 call per file**
- `scan_with_semgrep`: **0-1 call per file** (conditional)
- `send_slack_notification`: **1 call per PR**

### **When to Use Semgrep**
```
✅ YES - Run Semgrep if:
- Gemini found CRITICAL security issue
- Gemini found HIGH security issue
- Issue is from <security_rules> (not company rules)

❌ NO - Skip Semgrep if:
- Only MEDIUM/LOW issues
- Only company rule violations (R1-R43)
- No security issues found
```

---

## 🚀 **Setup**

### **1. Install Semgrep (Docker)**
```dockerfile
RUN pip install semgrep
```

### **2. Update Agent**
```python
from tools.gemini_analyzer import create_gemini_analyzer_function
from tools.semgrep_scanner import create_semgrep_scanner_function

tools=[
    github_toolset,
    gemini_analyzer,
    semgrep_scanner,
    slack_notifier
]
```

### **3. Rebuild & Restart**
```bash
docker-compose build
docker-compose up -d
```

---

## ✅ **Testing Checklist**

- [ ] PR #1 (clean code) → No CRITICAL, skip Semgrep
- [ ] PR #2 (mixed issues) → Some CRITICAL, run Semgrep
- [ ] PR #3 (vulnerable code) → Many CRITICAL, run Semgrep
- [ ] Verify: No duplicate tool calls
- [ ] Verify: Results sorted (CRITICAL → LOW)
- [ ] Verify: Slack notification sent
- [ ] Verify: Token usage < 60K for 2-file PR

---

## 📚 **Files Modified**

```
├── tools/
│   ├── gemini_analyzer.py          # NEW: Fast AI analysis
│   ├── semgrep_scanner.py          # NEW: Deep security scan
│   └── slack_notifier.py           # EXISTING
├── docs/
│   ├── AGENT_INSTRUCTION.md        # UPDATED: Hybrid workflow
│   └── HYBRID_ARCHITECTURE.md      # NEW: This file
├── my_agent/
│   └── agent.py                    # UPDATED: New tools
└── Dockerfile                      # UPDATED: Install Semgrep
```
