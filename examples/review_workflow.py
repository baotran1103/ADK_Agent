"""
Example workflow for PR review
Demonstrates how to interact with the Code Review Agent
"""

# Example 1: Review a PR
review_request = """
review PR #42 in myorg/myrepo
"""

# Example 2: Review specific files only
review_focused = """
review PR #42 in myorg/myrepo, focus on src/auth.py and src/api.py
"""

# Example 3: Review with context
review_with_context = """
review PR #42 in myorg/myrepo

Context: This PR adds new authentication endpoints. 
Please pay special attention to security and ensure all endpoints have @require_auth decorator.
"""

# Example 4: Follow-up questions
follow_up = """
explain the SQL injection issue you found in user_service.py line 45 in more detail
"""

# Example 5: Re-review after fixes
re_review = """
re-review PR #42 in myorg/myrepo after fixes
"""

# Example workflow conversation:
"""
USER: review PR #123 in baotran1103/my-api-project

AGENT: (follows 7-step workflow)
1. Fetches PR details from GitHub
2. Scans each file with Semgrep
3. Performs LLM security analysis
4. Checks company rules
5. Analyzes code quality
6. Ranks and organizes findings
7. Posts review to GitHub

AGENT RESPONSE:
📊 Review Summary
Files Analyzed: 8
Total Issues: 12
- 🔴 Critical: 2
- 🟠 High: 3
- 🟡 Medium: 5
- 🟢 Low: 2

Recommendation: ❌ Changes Requested

Review posted to GitHub: https://github.com/baotran1103/my-api-project/pull/123

Top issues found:
1. SQL Injection in src/user_service.py (line 45)
2. Missing @require_auth in src/api/users.py (line 23)
3. Hardcoded API key in config.py (line 12)

---

USER: explain the SQL injection issue in more detail

AGENT: 
The SQL injection vulnerability in src/user_service.py line 45:

**Current Code**:
```python
query = f"SELECT * FROM users WHERE username = '{username}'"
cursor.execute(query)
```

**Problem**:
String formatting with user input directly in SQL query. An attacker can inject:
- username = "admin' OR '1'='1"
- This becomes: SELECT * FROM users WHERE username = 'admin' OR '1'='1'
- Bypasses authentication and returns all users

**Fix**:
```python
query = "SELECT * FROM users WHERE username = %s"
cursor.execute(query, (username,))
```

Use parameterized queries - the database driver handles escaping.

---

USER: re-review after I fixed those issues

AGENT: (re-runs workflow)
✅ Review Summary
All critical and high issues resolved!
- 🟡 Medium: 5 (code quality improvements)
- 🟢 Low: 2 (style suggestions)

Recommendation: ✅ Approved with minor suggestions

Review posted to GitHub.
"""
