# Security Rules - Compact Version

> Optimized for LLM token efficiency
> Full examples: security_rules.md

---

## 🔴 CRITICAL Issues (Block merge immediately)

| Category | Patterns to Detect | Fix Required |
|----------|-------------------|--------------|
| **SQL Injection** | String concat in SQL: `"SELECT * " . $var`, interpolation: `"WHERE id = $id"`, raw SQL without params | Use prepared statements, parameterized queries, ORM query builder |
| **XSS** | Direct echo: `echo $_GET['name']`, Blade unescaped: `{!! $user_input !!}`, `innerHTML` with user data | Use `htmlspecialchars()`, Blade `{{ }}`, `textContent` in JS |
| **Auth Bypass** | No auth check on sensitive endpoints, missing authorization, hardcoded roles | Use middleware, check policies/gates, verify user permissions |
| **Hardcoded Secrets** | API keys, passwords, tokens in code: `$api_key = "sk_live_..."`, `DB_PASSWORD = "secret"` | Use env variables, secrets manager, never commit secrets |

---

## 🟠 HIGH Issues (Request changes)

| Category | Patterns to Detect | Fix Required |
|----------|-------------------|--------------|
| **Command Injection** | `shell_exec()`, `exec()`, `system()` with user input: `exec("ping " . $host)` | Validate input, use whitelists, avoid shell commands, use libraries |
| **Path Traversal** | File operations with user input: `file_get_contents("uploads/" . $filename)` | Validate paths, use basename(), check against whitelist, no `../` |
| **Unsafe Deserialization** | `unserialize()` with external data: `unserialize($_COOKIE['data'])` | Use `json_decode()`, validate source, sign serialized data |
| **Missing Auth Check** | Sensitive operations without authentication: `deleteUser()`, `updateProfile()` | Add auth middleware, verify user identity, check ownership |
| **Info Disclosure** | Detailed error messages, stack traces, debug info in production | Generic errors for users, log details server-side only |

---

## 🟡 MEDIUM Issues (Warning)

| Category | Patterns to Detect | Fix Required |
|----------|-------------------|--------------|
| **Weak Cryptography** | `md5()`, `sha1()` for passwords, weak algorithms | Use `bcrypt`, `Argon2`, `password_hash()` with cost >= 12 |
| **Missing Input Validation** | No validation before processing: `$user->email = $data['email']` without check | Validate format, length, type, range before use |
| **N+1 Query** | Loop with queries: `foreach($users) { $orders = Order::where('user_id', $user->id)->get(); }` | Use eager loading: `User::with('orders')->get()` |
| **No HTTPS** | Sensitive data over HTTP, cookies without `secure` flag | Enforce HTTPS, set `Secure` and `HttpOnly` cookie flags |

---

## 🟢 LOW Issues (Info/Best practice)

| Category | Patterns to Detect | Fix Required |
|----------|-------------------|--------------|
| **Session Security** | Session fixation risks, no regeneration after login | Call `session_regenerate_id()` after auth |
| **CORS Misconfiguration** | `Access-Control-Allow-Origin: *` with credentials | Whitelist specific origins, don't use `*` with credentials |
| **Missing Rate Limiting** | No throttling on sensitive endpoints (login, API) | Implement rate limiting, use middleware |
| **Debug Mode** | `APP_DEBUG=true` in production, detailed errors exposed | Set `APP_DEBUG=false`, hide stack traces |

---

## Detection Patterns by Language

### PHP
- **SQL Injection**: `mysqli_query($db, "... " . $var)`, `"WHERE id = $id"`
- **XSS**: `echo $_GET`, `{!! $var !!}`
- **Command Injection**: `shell_exec()`, `exec()`, `system()`
- **Weak Crypto**: `md5($password)`, `sha1()`
- **Deserialization**: `unserialize($_COOKIE)`

### JavaScript/Node.js
- **XSS**: `innerHTML = userInput`, `eval(userCode)`
- **SQL Injection**: String concat in queries
- **Command Injection**: `child_process.exec()` with user input
- **Path Traversal**: `fs.readFile(userPath)`

### Python
- **SQL Injection**: `cursor.execute("... " + var)`
- **Command Injection**: `os.system()`, `subprocess.call()` with user input
- **Deserialization**: `pickle.loads()` with untrusted data
- **Path Traversal**: `open(user_path)`

### Java
- **SQL Injection**: `Statement.executeQuery("... " + var)`
- **XSS**: Response without escaping
- **Deserialization**: `ObjectInputStream.readObject()`
- **XXE**: XML parsers without DTD disabled

---

## Analysis Guidelines

**CRITICAL** = Immediate security risk, exploitable
- RCE (Remote Code Execution)
- SQL Injection leading to data breach
- Auth bypass allowing privilege escalation
- Hardcoded credentials

**HIGH** = Serious vulnerability, requires fix
- Command injection with limited scope
- Path traversal exposing files
- Info disclosure of sensitive data
- Missing authentication on important endpoints

**MEDIUM** = Security concern, should fix
- Weak cryptography (not immediately exploitable)
- Missing input validation (context dependent)
- Performance issues with security implications

**LOW** = Best practice, improve security posture
- Session configuration
- CORS setup
- Debug mode in staging
- Missing rate limiting

---

**Total: 11 categories | 4 severity levels | Token count: ~100 lines vs 373 lines (73% reduction)**
