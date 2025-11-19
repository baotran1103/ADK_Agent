<?php
/**
 * Example của clean code tuân thủ security và coding standards
 * Dùng để so sánh với vulnerable_code.php
 * 
 * @author Development Team
 * @lastupdate 2025-11-18
 */

namespace App\Controllers;

use App\Models\User;
use App\Models\Order;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\DB;
use Illuminate\Http\Request;

/**
 * User Controller - handles user-related operations
 * Follows security best practices and company coding standards
 */
class UserController
{
    private const DISCOUNT_THRESHOLD = 1000;
    private const DISCOUNT_RATE = 0.1;
    private const MAX_BIO_LENGTH = 500;
    
    /**
     * Get user by ID with security checks
     * 
     * @param int $id User ID
     * @return User|null
     */
    public function getUser(int $id): ?User
    {
        // ✅ Prepared statement - no SQL injection
        return User::find($id);
    }
    
    /**
     * Get user by email safely
     * 
     * @param string $email User email
     * @return User|null
     */
    public function getUserByEmail(string $email): ?User
    {
        // ✅ Query builder with parameter binding
        return User::where('email', '=', $email)->first();
    }
    
    /**
     * Display username with proper escaping
     * 
     * @param Request $request
     * @return string
     */
    public function displayUsername(Request $request): string
    {
        // ✅ Blade auto-escapes with {{ }}
        $name = $request->input('name', 'Guest');
        return view('user.profile', ['name' => htmlspecialchars($name, ENT_QUOTES, 'UTF-8')]);
    }
    
    /**
     * Ping host safely (avoid command injection)
     * 
     * @param string $host Hostname to ping
     * @return array
     */
    public function pingHost(string $host): array
    {
        // ✅ Validate input first
        if (!filter_var($host, FILTER_VALIDATE_DOMAIN, FILTER_FLAG_HOSTNAME)) {
            throw new \InvalidArgumentException('Invalid hostname');
        }
        
        // ✅ Use escapeshellarg
        $safeHost = escapeshellarg($host);
        $output = shell_exec("ping -c 1 $safeHost");
        
        return ['output' => $output];
    }
    
    /**
     * Read file with path traversal protection
     * 
     * @param string $filename Filename to read
     * @return string
     * @throws \Exception
     */
    public function readFile(string $filename): string
    {
        // ✅ Validate path
        $allowedDir = storage_path('uploads/');
        $filename = basename($filename);  // Strip path
        $fullPath = realpath($allowedDir . $filename);
        
        if (strpos($fullPath, $allowedDir) !== 0) {
            throw new \Exception('Invalid file path');
        }
        
        return file_get_contents($fullPath);
    }
    
    /**
     * Delete user with authentication and authorization
     * 
     * @param int $userId User ID to delete
     * @return bool
     * @throws \Illuminate\Auth\Access\AuthorizationException
     */
    public function deleteUser(int $userId): bool
    {
        // ✅ Check authentication
        if (!Auth::check()) {
            throw new \Illuminate\Auth\AuthenticationException();
        }
        
        $user = User::findOrFail($userId);
        
        // ✅ Check authorization
        $this->authorize('delete', $user);
        
        return $user->delete();
    }
    
    /**
     * Hash password securely
     * 
     * @param string $password Plain password
     * @return string
     */
    public function hashPassword(string $password): string
    {
        // ✅ Use bcrypt/Argon2
        return password_hash($password, PASSWORD_ARGON2ID);
    }
    
    /**
     * Handle errors without information disclosure
     * 
     * @param \Exception $e Exception object
     * @return \Illuminate\Http\JsonResponse
     */
    public function handleError(\Exception $e): \Illuminate\Http\JsonResponse
    {
        // ✅ Log details internally
        \Log::error('Error occurred', [
            'message' => $e->getMessage(),
            'file' => $e->getFile(),
            'line' => $e->getLine(),
            'trace' => $e->getTraceAsString()
        ]);
        
        // ✅ Generic error message to users
        return response()->json([
            'error' => 'An error occurred. Please try again later.'
        ], 500);
    }
    
    /**
     * Get all users with only necessary fields
     * 
     * @return \Illuminate\Database\Eloquent\Collection
     */
    public function getAllUsers(): \Illuminate\Database\Eloquent\Collection
    {
        // ✅ Select only needed fields, không SELECT *
        return User::select(['id', 'name', 'email', 'created_at'])->get();
    }
    
    /**
     * Process order with proper validation and documentation
     * 
     * @param int $orderId Order ID
     * @param int $userId User ID
     * @param array $items Order items
     * @param string $shippingAddress Shipping address
     * @param string $paymentMethod Payment method
     * @return Order
     * @throws \Exception
     */
    public function processOrder(
        int $orderId,
        int $userId,
        array $items,
        string $shippingAddress,
        string $paymentMethod
    ): Order {
        // ✅ Use transaction for data integrity
        return DB::transaction(function () use ($orderId, $userId, $items, $shippingAddress, $paymentMethod) {
            $order = Order::findOrFail($orderId);
            
            // ✅ Extract to separate method
            $total = $this->calculateOrderTotal($items);
            $total = $this->applyDiscount($total);
            
            $order->update([
                'total' => $total,
                'status' => Order::STATUS_PENDING,
                'shipping_address' => $shippingAddress
            ]);
            
            // ✅ Use constant instead of magic string
            if ($paymentMethod === Order::PAYMENT_CREDIT_CARD) {
                $this->processPayment($order);
            }
            
            return $order;
        });
    }
    
    /**
     * Calculate order total
     * 
     * @param array $items Order items
     * @return float
     */
    private function calculateOrderTotal(array $items): float
    {
        $total = 0.0;
        
        foreach ($items as $item) {
            $total += ($item['price'] * $item['quantity']);
        }
        
        return $total;
    }
    
    /**
     * Apply discount if threshold met
     * 
     * @param float $total Order total
     * @return float
     */
    private function applyDiscount(float $total): float
    {
        if ($total > self::DISCOUNT_THRESHOLD) {
            return $total * (1 - self::DISCOUNT_RATE);
        }
        
        return $total;
    }
    
    /**
     * Update user profile with validation
     * 
     * @param array $data Profile data
     * @return User
     * @throws \Illuminate\Validation\ValidationException
     */
    public function updateProfile(array $data): User
    {
        // ✅ Validate input
        $validated = validator($data, [
            'name' => 'required|string|max:255',
            'email' => 'required|email|max:255|unique:users,email,' . Auth::id(),
            'bio' => 'nullable|string|max:' . self::MAX_BIO_LENGTH
        ])->validate();
        
        $user = Auth::user();
        $user->update($validated);
        
        return $user;
    }
    
    /**
     * Calculate final price with tax and fees
     * 
     * @param float $basePrice Base price
     * @param float $taxRate Tax rate
     * @param float $additionalFee Additional fee
     * @return float
     */
    public function calculateFinalPrice(float $basePrice, float $taxRate, float $additionalFee): float
    {
        $priceWithTax = $basePrice * (1 + $taxRate);
        $finalPrice = $priceWithTax + $additionalFee;
        
        return round($finalPrice, 2);
    }
    
    /**
     * Load user preferences safely
     * 
     * @return array
     */
    public function loadUserPreferences(): array
    {
        // ✅ Use JSON instead of serialize
        $json = $_COOKIE['preferences'] ?? '{}';
        return json_decode($json, true) ?? [];
    }
    
    /**
     * API endpoint with proper CORS
     * 
     * @return \Illuminate\Http\JsonResponse
     */
    public function apiEndpoint(): \Illuminate\Http\JsonResponse
    {
        // ✅ Whitelist specific origins
        $allowedOrigins = ['https://example.com', 'https://app.example.com'];
        $origin = $_SERVER['HTTP_ORIGIN'] ?? '';
        
        if (in_array($origin, $allowedOrigins)) {
            header("Access-Control-Allow-Origin: $origin");
            header('Access-Control-Allow-Credentials: true');
        }
        
        return response()->json(['data' => 'sensitive info']);
    }
    
    /**
     * Get users with orders (avoid N+1 query)
     * 
     * @return \Illuminate\Database\Eloquent\Collection
     */
    public function getUsersWithOrders(): \Illuminate\Database\Eloquent\Collection
    {
        // ✅ Eager loading to prevent N+1
        return User::with('orders')->get();
    }
    
    /**
     * Calculate tax (reusable utility method)
     * 
     * @param float $amount Amount to calculate tax on
     * @return float
     */
    public function calculateTax(float $amount): float
    {
        return round($amount * 0.1, 2);
    }
}
