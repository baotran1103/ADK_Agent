<?php
/**
 * Test file với nhiều lỗi bảo mật và vi phạm coding standards
 * Dùng để test Code Review Agent
 */

// ❌ CRITICAL: Hardcoded credentials
define('DB_PASSWORD', 'MySecretPass123!');
$api_key = "sk_live_abc123xyz789";

class userController {  // ❌ Naming: phải PascalCase
    
    // ❌ CRITICAL: SQL Injection - nối chuỗi trực tiếp
    public function getUser($id) {
        $query = "SELECT * FROM users WHERE id = " . $id;
        return mysqli_query($this->db, $query);
    }
    
    // ❌ CRITICAL: SQL Injection với string interpolation
    public function getUserByEmail($email) {
        $sql = "SELECT * FROM users WHERE email = '$email'";
        return $this->db->query($sql);
    }
    
    // ❌ CRITICAL: XSS - echo user input trực tiếp
    public function displayUsername() {
        echo $_GET['name'];  // Không escape!
    }
    
    // ❌ HIGH: Command Injection
    public function pingHost($host) {
        $output = shell_exec("ping -c 1 " . $host);
        return $output;
    }
    
    // ❌ HIGH: Path Traversal
    public function readFile($filename) {
        $content = file_get_contents("uploads/" . $filename);
        return $content;
    }
    
    // ❌ CRITICAL: No authentication check
    public function deleteUser($userId) {
        // Ai cũng có thể xóa user!
        User::find($userId)->delete();
    }
    
    // ❌ MEDIUM: Weak cryptography
    public function hashPassword($password) {
        return md5($password);  // MD5 quá yếu
    }
    
    // ❌ HIGH: Information disclosure
    public function handleError($e) {
        echo "Error: " . $e->getMessage();  // Leak stack trace
        echo "File: " . $e->getFile();
        echo "Line: " . $e->getLine();
    }
    
    // ❌ MEDIUM: SELECT * không nên dùng
    public function getAllUsers() {
        $query = "SELECT * FROM users";  // Lấy cả password hash!
        return $this->db->query($query);
    }
    
    // ❌ MEDIUM: Không có PHPDoc
    // ❌ MEDIUM: Function quá dài (>50 lines)
    public function processOrder($orderId, $userId, $items, $shippingAddress, $paymentMethod) {
        // Logic phức tạp không có documentation
        $order = Order::find($orderId);
        
        if ($order) {
            $total = 0;
            foreach ($items as $item) {
                $product = Product::find($item['id']);
                $price = $product->price;
                $quantity = $item['quantity'];
                $total = $total + ($price * $quantity);  // ❌ Có thể integer overflow
            }
            
            // ❌ MEDIUM: Magic number
            if ($total > 1000) {
                $discount = $total * 0.1;
                $total = $total - $discount;
            }
            
            $order->total = $total;
            $order->status = 'pending';
            $order->save();
            
            // ❌ LOW: Nên dùng constant thay vì hardcode string
            if ($paymentMethod == 'credit_card') {
                $this->processPayment($order);
            }
            
            return $order;
        }
        
        return null;
    }
    
    // ❌ MEDIUM: Không validate input
    public function updateProfile($data) {
        $user = Auth::user();
        $user->name = $data['name'];  // Không check null, XSS
        $user->email = $data['email'];  // Không validate email format
        $user->bio = $data['bio'];  // Không check length
        $user->save();
    }
    
    // ❌ LOW: Tên biến không rõ nghĩa
    public function calc($a, $b, $c) {
        $x = $a + $b;
        $y = $x * $c;
        $z = $y - 100;
        return $z;
    }
    
    // ❌ CRITICAL: Unsafe deserialization
    public function loadUserPreferences() {
        $data = unserialize($_COOKIE['preferences']);  // RCE risk!
        return $data;
    }
    
    // ❌ HIGH: CORS misconfiguration
    public function apiEndpoint() {
        header('Access-Control-Allow-Origin: *');  // Cho phép mọi origin!
        header('Access-Control-Allow-Credentials: true');  // Nguy hiểm!
        
        return json_encode(['data' => 'sensitive info']);
    }
    
    // ❌ MEDIUM: N+1 query problem
    public function getUsersWithOrders() {
        $users = User::all();  // Query 1
        
        $result = [];
        foreach ($users as $user) {
            $orders = Order::where('user_id', $user->id)->get();  // N queries!
            $result[] = [
                'user' => $user,
                'orders' => $orders
            ];
        }
        
        return $result;
    }
}

// ❌ CRITICAL: eval() với user input
if (isset($_POST['code'])) {
    eval($_POST['code']);  // Remote Code Execution!
}

// ❌ MEDIUM: Kết nối database không đóng
$conn = mysqli_connect("localhost", "root", "password", "database");
mysqli_query($conn, "SELECT * FROM users");
// Không có mysqli_close($conn)

// ❌ LOW: Code trùng lặp
function calculateTax1($amount) {
    return $amount * 0.1;
}

function calculateTax2($amount) {
    return $amount * 0.1;  // Giống hệt calculateTax1
}

// ❌ MEDIUM: Dùng deprecated function
$data = mysql_query("SELECT * FROM users");  // mysql_* deprecated!

// ❌ LOW: Thiếu return type declaration (PHP 7+)
function getTotal($items) {
    $total = 0;
    foreach ($items as $item) {
        $total += $item['price'];
    }
    return $total;
}

?>
