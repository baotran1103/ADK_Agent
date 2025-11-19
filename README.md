# Code Review Agent - AI-Powered PR Review System

[![ADK](https://img.shields.io/badge/Powered%20by-Google%20ADK-blue)](https://github.com/google/adk)
[![Python](https://img.shields.io/badge/Python-3.13+-green)](https://python.org)
[![Security](https://img.shields.io/badge/Security-Semgrep-orange)](https://semgrep.dev)

An intelligent AI agent that performs comprehensive code reviews on GitHub Pull Requests, combining:
- 🔐 **Security scanning** (Semgrep + LLM analysis)
- 📋 **Company rules enforcement** (YAML-defined standards)
- 💡 **Code quality analysis** (logic, performance, best practices)

## 🏗️ Architecture

```
GitHub PR
    ↓
┌─────────────────────────────────────────────┐
│   MAIN AGENT (Code Review Assistant)       │
│   Model: gemini-2.0-flash                  │
│   Role: Orchestrator + Analyzer            │
└─────────────────────────────────────────────┘
    │
    ├─── Tool 1: GitHub MCP (get PR, post review)
    ├─── Tool 2: Security Scanner (Semgrep + LLM)
    └─── Tool 3: Company Rules Checker (YAML)
```

## 🎯 Features

### **1. Security Analysis (Top Priority)**
- **Semgrep Static Analysis**: Pattern-based vulnerability detection
- **LLM Deep Reasoning**: Logic-based security issues
- **Detects**:
  - SQL Injection
  - XSS (Cross-Site Scripting)
  - Hardcoded secrets (API keys, passwords, tokens)
  - Command injection
  - Path traversal
  - Weak cryptography
  - Authentication/authorization issues
  - Unsafe deserialization

### **2. Company Rules Enforcement**
Defined in `rules/company_rules.yaml`:
- **Naming Conventions**: PascalCase, snake_case, UPPER_CASE
- **Code Structure**: Max lines, docstrings, file organization
- **Security Patterns**: Forbidden functions (eval, exec), required patterns
- **Decorators**: Required @require_auth, @transaction.atomic, @rate_limit
- **Dependencies**: Allowed/forbidden packages, version constraints

### **3. Code Quality & Logic**
- Logic errors (off-by-one, null handling, edge cases)
- Code smells (duplication, complexity, deep nesting)
- Performance issues (N+1 queries, inefficient algorithms)
- Best practices (SOLID, DRY, error handling)

## 🚀 Quick Start

### **Prerequisites**
- Docker & Docker Compose
- GitHub Personal Access Token with repo permissions
- Google Gemini API key

### **Setup**

1. **Clone repository**:
```bash
git clone https://github.com/baotran1103/code-review-agent
cd code-review-agent
```

2. **Configure environment** (`.env`):
```env
GEMINI_API_KEY='your-gemini-api-key'
ACCESS_TOKEN=your-github-pat
```

3. **Customize company rules** (optional):
Edit `rules/company_rules.yaml` to match your standards.

4. **Build and run**:
```bash
docker-compose build
docker-compose up -d
```

5. **Access web UI**:
Open http://localhost:8080

## 💻 Usage

### **Option 1: Web UI**
1. Open http://localhost:8080
2. Type: `review PR #123 in owner/repo`
3. Agent performs 7-step review workflow
4. Review posted to GitHub automatically

### **Option 2: Chat Interface**
```
YOU: review PR #42 in myorg/myrepo

AGENT: 
📊 Review Summary
Files Analyzed: 8
Total Issues: 12
- 🔴 Critical: 2 (SQL injection, hardcoded secret)
- 🟠 High: 3 (missing auth decorators)
- 🟡 Medium: 5 (code quality)
- 🟢 Low: 2 (style)

Recommendation: ❌ Changes Requested

Top Issues:
1. SQL Injection in src/user_service.py line 45
2. Hardcoded API key in config.py line 12
3. Missing @require_auth in src/api/users.py line 23

Review posted to GitHub.
```

### **Follow-up Questions**
```
YOU: explain the SQL injection issue in more detail

AGENT: [provides detailed explanation with code examples]

YOU: suggest a fix for the hardcoded API key

AGENT: [provides specific fix recommendation]
```

## 📝 Review Workflow (7 Steps)

1. **Fetch PR Details**: Get files, diffs, metadata from GitHub
2. **Security Analysis**: Run Semgrep + LLM reasoning
3. **Company Rules Check**: Enforce naming, structure, decorators
4. **Code Quality Analysis**: Find logic errors, performance issues
5. **Rank & Organize**: Deduplicate, sort by severity
6. **Generate Report**: Clear, actionable feedback with examples
7. **Post to GitHub**: Line comments + overall review

## 🛠️ Customization

### **Company Rules** (`rules/company_rules.yaml`)
```yaml
naming_conventions:
  class_names:
    pattern: "^[A-Z][a-zA-Z0-9]*$"  # PascalCase
    
  function_names:
    pattern: "^[a-z][a-z0-9_]*$"  # snake_case

security_patterns:
  forbidden_patterns:
    - pattern: "password\\s*=\\s*['\"].*['\"]"
      message: "Hardcoded passwords not allowed"
      severity: "CRITICAL"

required_decorators:
  api_endpoints:
    decorators:
      - "@require_auth"
      - "@require_https"
```

### **Agent Configuration** (`my_agent/agent.py`)
- Change model: `model="gemini-2.0-flash-exp"`
- Modify instruction: Edit `AGENT_INSTRUCTION`
- Add tools: Extend `tools=[...]`

## 📦 Project Structure

```
code-review-agent/
├── my_agent/
│   └── agent.py              # Main agent with instructions
├── tools/
│   ├── security_scanner.py   # Semgrep + LLM security tool
│   └── company_rules_checker.py  # YAML rules enforcer
├── rules/
│   └── company_rules.yaml    # Company coding standards
├── examples/
│   └── review_workflow.py    # Usage examples
├── Dockerfile                # Container with Semgrep
├── docker-compose.yml        # Service orchestration
├── pyproject.toml            # Python dependencies
└── README.md                 # This file
```

## 🔧 Tools Details

### **1. Security Scanner**
```python
scan_code_security(
    file_content="...",
    file_path="src/auth.py",
    language="python",
    git_diff="..."  # optional
)
```
Returns: Semgrep findings + LLM analysis prompt

### **2. Company Rules Checker**
```python
check_company_rules(
    file_content="...",
    file_path="src/service.py",
    language="python"
)
```
Returns: Naming, structure, security, decorator violations

## 🐛 Troubleshooting

### **Semgrep not found**
Agent will fall back to LLM-only security analysis.

To install Semgrep in Docker:
```dockerfile
RUN apt-get update && \
    apt-get install -y curl && \
    curl -sSL https://github.com/returntocorp/semgrep/releases/latest/download/semgrep-linux.tar.gz | tar -xz -C /usr/local/bin
```

### **GitHub API rate limit**
Agent will notify and pause. Wait for rate limit reset.

### **Large PRs (>100 files)**
Agent will ask: "Focus on specific files or review all?"

### **Unsupported language**
Agent will skip Semgrep, perform LLM logic analysis only.

## 🔐 Security Best Practices

1. **Never commit** `.env` file (contains secrets)
2. **Use minimal GitHub token scopes** (only repo access needed)
3. **Review company rules** before deploying
4. **Monitor agent activity** for false positives
5. **Rotate tokens regularly**

## 📚 Documentation

- [Google ADK Documentation](https://developers.google.com/adk)
- [GitHub MCP Server](https://github.com/github/github-mcp-server)
- [Semgrep Rules](https://semgrep.dev/docs/writing-rules/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request (and let the agent review it! 😄)

## 📄 License

MIT License - See LICENSE file

## 🙏 Acknowledgments

- **Google ADK** - Agent Development Kit framework
- **Semgrep** - Open-source security scanner
- **GitHub MCP Server** - GitHub integration via MCP

## 📞 Support

- Create an issue: [GitHub Issues](https://github.com/baotran1103/code-review-agent/issues)
- Email: your-email@example.com

---

**Built with ❤️ using Google ADK, Semgrep, and GitHub MCP**