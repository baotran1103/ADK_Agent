# 🛡️ SECURITY RULES - QUY TẮC BẢO MẬT CODE

> Checklist kiểm tra bảo mật cho mọi ngôn ngữ lập trình

---

## 1. 🔴 SQL INJECTION (Mức độ: CRITICAL)

### ❌ KHÔNG ĐƯỢC PHÉP:
```php
// Nối chuỗi trực tiếp
$query = "SELECT * FROM users WHERE id = " . $_GET['id'];

// String interpolation không an toàn
$query = "SELECT * FROM users WHERE email = '$email'";
```

### ✅ BẮT BUỘC:
```php
// Dùng prepared statements
$stmt = $pdo->prepare("SELECT * FROM users WHERE id = ?");
$stmt->execute([$id]);

// Hoặc named parameters
$stmt = $pdo->prepare("SELECT * FROM users WHERE email = :email");
$stmt->execute(['email' => $email]);
```

**Kiểm tra:**
- Không có nối chuỗi trong SQL queries (`"SELECT * " . $var`)
- Không có string interpolation (`"... WHERE id = $id"`)
- Phải dùng parameterized queries
- ORM (Eloquent, Doctrine) phải dùng query builder, không raw SQL

---

## 2. 🔴 XSS (Cross-Site Scripting) (Mức độ: CRITICAL)

### ❌ KHÔNG ĐƯỢC PHÉP:
```php
// Echo trực tiếp user input
echo $_GET['name'];
echo $request->input('comment');

// Blade không escape
{!! $userContent !!}
```

### ✅ BẮT BUỘC:
```php
// PHP: escape HTML entities
echo htmlspecialchars($_GET['name'], ENT_QUOTES, 'UTF-8');

// Laravel Blade: auto-escape
{{ $userContent }}

// JavaScript: escape trước khi insert vào DOM
element.textContent = userInput; // Không dùng innerHTML
```

**Kiểm tra:**
- Không echo/print trực tiếp `$_GET`, `$_POST`, `$_REQUEST`
- Blade phải dùng `{{ }}` không dùng `{!! !!}` với user input
- JavaScript không dùng `innerHTML`, `eval()`, `document.write()` với user data

---

## 3. 🔴 AUTHENTICATION & AUTHORIZATION (Mức độ: CRITICAL)

### ❌ KHÔNG ĐƯỢC PHÉP:
```php
// Không check authentication
public function deleteUser($id) {
    User::find($id)->delete(); // Ai cũng xóa được!
}

// Check yếu
if ($_SESSION['user']) { ... } // Session có thể fake
```

### ✅ BẮT BUỘC:
```php
// Laravel middleware
Route::delete('/user/{id}', function($id) {
    // Middleware 'auth' đã check authentication
})->middleware('auth');

// Check authorization (user có quyền không?)
public function deleteUser($id) {
    $this->authorize('delete', User::find($id));
    User::find($id)->delete();
}
```

**Kiểm tra:**
- Mọi endpoint nhạy cảm phải có authentication check
- Phải verify authorization (user có quyền thao tác resource không?)
- Không hardcode roles trong code (`if ($user->role == 'admin')`)
- Phải dùng Policy/Gate (Laravel) hoặc decorator pattern

---

## 4. 🔴 HARDCODED SECRETS (Mức độ: CRITICAL)

### ❌ KHÔNG ĐƯỢC PHÉP:
```php
$apiKey = "sk_live_abc123xyz789"; // API key trong code
$password = "MyP@ssw0rd123"; // Password hardcoded
$dbHost = "mysql://user:pass@localhost/db"; // Connection string có credentials
```

### ✅ BẮT BUỘC:
```php
// Dùng environment variables
$apiKey = env('STRIPE_API_KEY');
$password = env('DB_PASSWORD');

// Hoặc config files (không commit vào git)
$config = require __DIR__ . '/config.local.php';
```

**Kiểm tra:**
- Không có string chứa: `password`, `api_key`, `secret`, `token`, `private_key`
- Không có pattern: `sk_live_`, `pk_test_`, `ghp_`, `xoxb-`
- Phải dùng `env()` hoặc config files
- File `.env` phải có trong `.gitignore`

---

## 5. 🟠 COMMAND INJECTION (Mức độ: HIGH)

### ❌ KHÔNG ĐƯỢC PHÉP:
```php
// Shell command với user input
exec("ls -la " . $_GET['dir']);
system("convert " . $filename . " output.jpg");

// Backticks
$output = `ping -c 1 $host`;
```

### ✅ BẮT BUỘC:
```php
// Escape shell arguments
$dir = escapeshellarg($_GET['dir']);
exec("ls -la $dir");

// Hoặc dùng array syntax (không qua shell)
exec(['ls', '-la', $_GET['dir']]);

// Tốt nhất: dùng PHP functions thay shell
$files = scandir($_GET['dir']); // Thay vì exec("ls")
```

**Kiểm tra:**
- Không dùng `exec()`, `system()`, `shell_exec()`, backticks với user input
- Nếu bắt buộc dùng: phải `escapeshellarg()` hoặc `escapeshellcmd()`
- Ưu tiên dùng PHP native functions thay shell commands

---

## 6. 🟠 PATH TRAVERSAL (Mức độ: HIGH)

### ❌ KHÔNG ĐƯỢC PHÉP:
```php
// Đọc file dựa vào user input
$file = $_GET['file'];
include($file); // Có thể: ?file=../../../../etc/passwd

readfile("uploads/" . $_POST['filename']);
```

### ✅ BẮT BUỘC:
```php
// Validate filename (không có ../ hoặc /)
$file = basename($_GET['file']); // Chỉ lấy filename, bỏ path
$allowedDir = '/var/www/uploads/';
$fullPath = realpath($allowedDir . $file);

if (strpos($fullPath, $allowedDir) !== 0) {
    throw new Exception("Invalid file path");
}

readfile($fullPath);
```

**Kiểm tra:**
- File operations phải validate path
- Không cho phép `../` trong user input
- Dùng `basename()` để strip path
- Dùng `realpath()` và check prefix
- Whitelist allowed directories

---

## 7. 🟠 UNSAFE DESERIALIZATION (Mức độ: HIGH)

### ❌ KHÔNG ĐƯỢC PHÉP:
```php
// Unserialize user input
$data = unserialize($_COOKIE['user_data']); // RCE risk!

// Python
import pickle
data = pickle.loads(user_input) # RCE risk!
```

### ✅ BẮT BUỘC:
```php
// Dùng JSON thay serialize
$data = json_decode($_COOKIE['user_data'], true);

// Nếu bắt buộc serialize: sign data
$data = unserialize(verify_signature($_COOKIE['user_data']));
```

**Kiểm tra:**
- Không dùng `unserialize()` với user input
- Python: không dùng `pickle.loads()` với external data
- Ưu tiên JSON, không dùng native serialization
- Nếu dùng serialize: phải có signature/HMAC verification

---

## 8. 🟡 WEAK CRYPTOGRAPHY (Mức độ: MEDIUM)

### ❌ KHÔNG ĐƯỢC PHÉP:
```php
// MD5, SHA1 cho passwords
$hash = md5($password); // Dễ crack
$hash = sha1($password); // Vẫn yếu

// Mã hóa không an toàn
$encrypted = base64_encode($data); // Base64 không phải encryption!
```

### ✅ BẮT BUỘC:
```php
// Dùng bcrypt hoặc Argon2 cho passwords
$hash = password_hash($password, PASSWORD_ARGON2ID);

// Verify
if (password_verify($inputPassword, $hash)) { ... }

// Encryption: dùng libsodium hoặc OpenSSL
$encrypted = sodium_crypto_secretbox($data, $nonce, $key);
```

**Kiểm tra:**
- Không dùng `md5()`, `sha1()` cho passwords
- Không dùng `base64_encode()` khi cần encryption
- Phải dùng `password_hash()` với bcrypt/Argon2
- Encryption phải dùng modern library (libsodium, OpenSSL)

---

## 9. 🟡 INFORMATION DISCLOSURE (Mức độ: MEDIUM)

### ❌ KHÔNG ĐƯỢC PHÉP:
```php
// Error messages chi tiết
catch (Exception $e) {
    echo "Database error: " . $e->getMessage(); // Leak DB structure
}

// Stack trace cho users
ini_set('display_errors', 1); // Production!

// Excessive data in API
return User::all(); // Trả về cả password hash, tokens...
```

### ✅ BẮT BUỘC:
```php
// Generic error messages
catch (Exception $e) {
    Log::error($e); // Log chi tiết
    return response()->json(['error' => 'Internal server error'], 500);
}

// API: chỉ trả fields cần thiết
return User::select(['id', 'name', 'email'])->get();

// Hoặc dùng API Resources
return UserResource::collection(User::all());
```

**Kiểm tra:**
- Production: `display_errors = 0`
- Error messages không reveal stack trace, SQL queries, paths
- API responses không trả sensitive fields (password, tokens)
- Log sensitive data phải được mask

---

## 10. 🟢 SESSION SECURITY (Mức độ: LOW)

### ✅ BẮT BUỘC:
```php
// Session config an toàn
ini_set('session.cookie_httponly', 1); // Không access từ JS
ini_set('session.cookie_secure', 1);   // Chỉ HTTPS
ini_set('session.use_strict_mode', 1); // Không accept uninitialized session ID

// Regenerate session ID sau login
session_regenerate_id(true);
```

**Kiểm tra:**
- Session cookies phải có `HttpOnly`, `Secure`, `SameSite` flags
- Session ID phải regenerate sau authentication
- Session timeout hợp lý (< 30 phút cho sensitive apps)

---

## 11. 🟢 CORS CONFIGURATION (Mức độ: LOW)

### ❌ KHÔNG ĐƯỢC PHÉP:
```php
// Allow all origins
header('Access-Control-Allow-Origin: *'); // Nguy hiểm nếu có credentials
```

### ✅ BẮT BUỘC:
```php
// Whitelist specific origins
$allowedOrigins = ['https://example.com', 'https://app.example.com'];
$origin = $_SERVER['HTTP_ORIGIN'] ?? '';

if (in_array($origin, $allowedOrigins)) {
    header("Access-Control-Allow-Origin: $origin");
    header('Access-Control-Allow-Credentials: true');
}
```

**Kiểm tra:**
- Không dùng `Access-Control-Allow-Origin: *` với credentials
- Phải whitelist cụ thể domains
- Validate origin trước khi set header

---

## 📋 SECURITY CHECKLIST TỔNG HỢP

Khi review code, kiểm tra:

- [ ] **Input Validation**: Mọi user input đều được validate
- [ ] **Output Encoding**: Escape khi render HTML/JS/SQL
- [ ] **Authentication**: Endpoints nhạy cảm đều có auth check
- [ ] **Authorization**: Verify user có quyền thao tác resource
- [ ] **Secrets Management**: Không hardcode credentials
- [ ] **SQL Injection**: Dùng prepared statements
- [ ] **XSS Prevention**: Escape output, không dùng innerHTML
- [ ] **CSRF Protection**: Forms có CSRF tokens
- [ ] **Error Handling**: Không leak sensitive info
- [ ] **Logging**: Log security events, mask sensitive data
- [ ] **Dependencies**: Không dùng outdated/vulnerable packages
- [ ] **HTTPS**: Production phải dùng HTTPS
- [ ] **Rate Limiting**: API có rate limiting
- [ ] **File Upload**: Validate file type, size, scan malware

---

## 🎯 SEVERITY LEVELS

- 🔴 **CRITICAL**: SQL injection, XSS, Auth bypass, Hardcoded secrets → Fix ngay
- 🟠 **HIGH**: Command injection, Path traversal, Unsafe deserialization → Fix trong 24h
- 🟡 **MEDIUM**: Weak crypto, Info disclosure → Fix trong tuần
- 🟢 **LOW**: Session config, CORS → Fix khi có thời gian

---

**GHI CHÚ**: Checklist này áp dụng cho mọi ngôn ngữ (PHP, Python, JavaScript, Java...). Adjust examples theo syntax của từng ngôn ngữ.
