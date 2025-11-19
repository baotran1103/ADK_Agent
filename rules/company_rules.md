# Company Coding Standards

> Laravel/PHP Project
> 
> Based on: PSR-12, PHP CodeSniffer, PHPDocumentor standards

---

## 📋 Table of Contents

1. [PHP Standards](#php-standards)
2. [SQL Standards](#sql-standards)
3. [Comment Standards](#comment-standards)
4. [Checklist](#checklist)

---

## 🔷 PHP Standards

### 1. Format - PSR-12 Compliance

**Rule:** Write all PHP code based on PSR-12 standard

**Requirements:**
- Use **Camel Case** for functions and variables
- Check coding standard with `phpcs` (PHP CodeSniffer)
- Use VSCode with PSR-12 linter extension

**Reference:** https://www.php-fig.org/psr/psr-12/

---

### 2. PHP Constants

**Rule:** The PHP constants `true`, `false`, and `null` MUST be lowercase

**Correct:**
```php
if ($foo === true) {
    $bar = false;
}
function foo($bar = null) {
    // ...
}
```

**Wrong:**
```php
if ($foo === TRUE) {  // WRONG
    $bar = FALSE;     // WRONG
}
```

---

### 3. Parameter Validation

**Rule:** All parameters must be checked for validation before processing to avoid PHP errors

**Correct:**
```php
function inverse($x) {
    // Check validation for $x
    if ($x === 0) {
        throw new Exception('Division by zero.');
    }
    return 1 / $x;
}
```

**Why:** Prevents runtime errors and improves code reliability

---

### 4. Naming Convention - Functions & Variables

**Rule:** Functions and variables are named in **camelCase**

**Correct:**
- `getData()`
- `calculateTotal()`
- `$userId`
- `$totalAmount`

**Wrong:**
- `get_data()` ❌ (snake_case)
- `GetData()` ❌ (PascalCase)
- `getdata()` ❌ (no case)

---

### 5. Naming Convention - Classes & Files

**Rule:** Filename and namespace must be the same

**Correct:**
- File: `BasePricing.php`
- Class: `class BasePricing`

**Wrong:**
- File: `basePricing.php` ❌ (lowercase first letter)
- File: `base_pricing.php` ❌ (snake_case)

---

### 6. Author Comments

**Rule:** Comment author name in function

**Format:**
```php
/**
 * Description of function
 * 
 * @author lastname.firstname
 */
```

**Example:**
```php
/**
 * Calculate total price with discount
 * 
 * @author tran.bao
 */
public function calculateTotal($price, $discount) {
    // ...
}
```

---

### 7. Namespace Declaration

**Rule:** Define namespace at top of file with one blank line after

**Correct:**
```php
<?php
namespace Vendor\Model;

use Vendor\Model\Bar;
use OtherVendor\OtherPackage\HttpRequest as Request;

class Foo {
    // ...
}
```

**Path Example:**
- Path: `project/ps/xxx`
- Namespace: `project\ps\test`

---

## 🔷 MVC Patterns

### 8. Data Access from Controller

**Rule:** We shouldn't access data origin directly from controller

**Correct Approach:**
- Get data from table → use **Model**
- Get data from file → create **File class** to process
- Get cache → use **Cache library**

**Wrong:**
```php
// DON'T do this in Controller
$data = DB::table('users')->get();
```

**Correct:**
```php
// Use Model
$data = User::all();
```

---

### 9. Function Visibility in Controllers

**Rule:** Only action functions should be `public`, other functions must be `private`

**Correct:**
```php
class UserController {
    // Public - action method
    public function index() {
        return $this->processData();
    }
    
    // Private - helper method
    private function processData() {
        // ...
    }
}
```

---

### 10. Common Functions in Base Controller

**Rule:** Declare common functions in BaseController

**Example:**
```php
class BaseController {
    protected function validateInput($data) {
        // Common validation logic
    }
    
    protected function logActivity($action) {
        // Common logging logic
    }
}
```

---

### 11. System Logging

**Rule:** We should use logs for system operations

**Example:**
```php
Log::info('User logged in', ['user_id' => $userId]);
Log::error('Payment failed', ['order_id' => $orderId, 'error' => $e->getMessage()]);
```

---

### 12. Input Validation

**Rule:** We MUST validate input forms before processing

**Example:**
```php
$validated = $request->validate([
    'email' => 'required|email|max:255',
    'price' => 'required|numeric|min:0',
]);
```

---

### 13. Loop Depth

**Rule:** Depth of loop must be less than 4

**Wrong:**
```php
foreach ($a as $item1) {
    foreach ($b as $item2) {
        foreach ($c as $item3) {
            foreach ($d as $item4) {  // TOO DEEP!
                foreach ($e as $item5) {  // WAY TOO DEEP!
                    // ...
                }
            }
        }
    }
}
```

**Solution:** Refactor into separate functions

---

## 🔷 Performance Optimization

### 14. Singleton Pattern for Constructors

**Rule:** If a class uses `__construct()`, use singleton pattern to improve memory

**Correct:**
```php
class Db {
    private static $instance = null;
    private $connect;
    
    private function __construct() {
        if ($this->connect) {
            return $this->connect;
        }
        $this->connect = new \PDO(...);
    }
    
    public static function getInstance() {
        if (self::$instance === null) {
            self::$instance = new self();
        }
        return self::$instance;
    }
}
```

---

### 15. Strict Comparison (===)

**Rule:** Use `===` operator for faster performance and type safety

**Correct:**
```php
$test = true;
if ($test === 1) {
    return 'correct';  // Won't return (true !== 1)
}
```

**Wrong:**
```php
$test = true;
if ($test == 1) {  // Type coercion!
    return 'correct';  // Will return 'correct'
}
```

---

### 16. Avoid Looping Function Calls

**Rule:** Don't use for/foreach to loop a function that can process arrays

**Correct:**
```php
processItems($arrItems);  // Process entire array at once
```

**Wrong:**
```php
foreach ($arrItems as $item) {
    processItem($item);  // Inefficient
}
```

---

### 17. String Quoting

**Rule:** Always use single quotes unless you need variable parsing

**Correct:**
```php
$str1 = 'My String';           // No variables
$str2 = "My {$variable}";      // With variable
```

**Wrong:**
```php
$str1 = "My String";           // Unnecessary double quotes
$str2 = "My $variable";        // Use curly braces for clarity
```

---

### 18. Calculate Once, Use Multiple Times

**Rule:** Calculate and assign value to variable if used multiple times

**Wrong:**
```php
for ($i = 0; $i < count($arrA); $i++) {
    echo count($arrA);  // Calling count() repeatedly
}
```

**Correct:**
```php
$len = count($arrA);  // Calculate once
for ($i = 0; $i < $len; $i++) {
    echo $len;
}
```

---

## 🔷 SQL Standards

### 19. Uppercase SQL Keywords

**Rule:** Use UPPERCASE for SQL keywords

**Correct:**
```sql
SELECT name FROM customer WHERE price > 100
```

**Wrong:**
```sql
select name From customer where price > 100
```

---

### 20. Correct Data Types in WHERE Clause

**Rule:** Use correct data type in WHERE clause (don't quote integers)

**Correct:**
```sql
SELECT email FROM customer WHERE price = 1;  -- price is INT
```

**Wrong:**
```sql
SELECT email FROM customer WHERE price = '1';  -- Unnecessary quotes
```

---

### 21. Avoid Reserved Words as Aliases

**Rule:** Don't use table alias same as MySQL function name

**Correct:**
```sql
SELECT id FROM t_order
SELECT id FROM t_order AS o
```

**Wrong:**
```sql
SELECT id FROM t_order AS order  -- 'order' is a MySQL function
```

---

### 22. Don't Use SELECT *

**Rule:** Avoid `SELECT *`, specify columns explicitly

**Correct:**
```sql
SELECT email, name, bill FROM customer
```

**Wrong:**
```sql
SELECT * FROM customer
```

**Why:** Better performance, clearer intent, prevents unnecessary data transfer

---

### 23. Use COUNT with Indexed Column

**Rule:** Don't use `COUNT(*)`, use `COUNT(indexed_column)`

**Correct:**
```sql
SELECT COUNT(bill) AS total FROM customer
```

**Wrong:**
```sql
SELECT COUNT(*) AS total FROM customer
```

---

### 24. Use <> Instead of !=

**Rule:** Use `<>` for "not equal" comparison

**Correct:**
```sql
SELECT email FROM customer WHERE name <> 'ABC'
```

**Wrong:**
```sql
SELECT email FROM customer WHERE name != 'ABC'
```

---

### 25. Always Use WHERE in UPDATE

**Rule:** Put WHERE clauses in SQL UPDATE statements

**Correct:**
```sql
UPDATE sd_request
SET available_field_1 = 'my_value'
WHERE available_field_1 IS NOT NULL
```

**Wrong:**
```sql
UPDATE sd_request
SET available_field_1 = 'my_value'  -- Updates ALL rows!
```

---

### 26. Use Indexes

**Rule:** Use indexes on frequently queried columns to improve speed

**Best Practices:**
- Index foreign keys
- Index columns in WHERE clauses
- Index columns in JOIN conditions

---

### 27. Handle NULL Values Carefully

**Rule:** Write queries carefully when value can be NULL

**Correct:**
```sql
WHERE column IS NULL
WHERE column IS NOT NULL
```

**Wrong:**
```sql
WHERE column = NULL    -- Always false!
WHERE column != NULL   -- Always false!
```

---

## 🔷 Comment Standards

All comments must follow **PHPDocumentor** format
Reference: http://phpdoc.org/docs/latest/index.html

### 28. File Comment

**Format:**
```php
/**
 * [Description of file purpose]
 *
 * @package App
 * @subpackage Controllers
 * 
 * @author lastname.firstname <lastname.firstname@rivercrane.vn>
 */
```

---

### 29. Class Comment

**Format:**
```php
/**
 * [Description of class purpose]
 *
 * @author lastname.firstname <lastname.firstname@rivercrane.vn>
 */
class UserService {
    // ...
}
```

---

### 30. Function Comment

**Format:**
```php
/**
 * Get data from table doing.
 *
 * @param string $url  The URL api 
 * @throws Daito\ps1\Exception (If have)
 * @author lastname.firstname
 * @lastupdate lastname.firstname
 *
 * @return array $data The data of table doing
 */
public function getData($url) {
    // Start process 
    // End process
    return $data;
}
```

**Required Elements:**
- Description of function purpose
- `@param` for each parameter with type and description
- `@throws` for exceptions (if any)
- `@author` - function creator
- `@lastupdate` - last person who modified
- `@return` with type and description

---

### 31. Variable Comment

**Format:**
```php
/**
 * @var array Request parameters
 */
private static $_params;
```

---

### 32. Condition Comment

**Rule:** Write comments for complex processes

**Example:**
```php
if ($condition) {
    // Description of complex logic here
    // Explanation of why this approach is used
    // Code for complex process
}
```

---

## 🔷 Checklist Before Deployment

### 33. Bulk Insert for Large Data

**Rule:** When inserting large amounts of records (e.g., 1M), use bulk insert with `array_chunk`

**Example:**
```php
$arrData = [...]; // 1 million records
$chunks = array_chunk($arrData, 1000);

foreach ($chunks as $chunk) {
    DB::table('users')->insert($chunk);
}
```

---

### 34. Test Batch Processing

**Rule:** Test batch processing with large data volumes to adjust performance in time

**Action Items:**
- Test with realistic data volumes
- Monitor memory usage
- Measure execution time
- Optimize queries if needed

---

### 35. Validate Numeric Variables

**Rule:** Check lower and upper bounds clearly against database data type

**Example:**
```php
// Database column: INT (max 2,147,483,647)
if ($quantity < 0 || $quantity > 2147483647) {
    throw new Exception('Invalid quantity');
}
```

---

### 36. Validate String Length

**Rule:** Check string length against database column length

**Example:**
```php
// Database column: VARCHAR(255)
if (strlen($email) > 255) {
    throw new Exception('Email too long');
}
```

**Wrong Example:**
```php
// Database: CHAR(10)
// Input: "abcdefghj@gmail.com" (21 chars)
// Result: ERROR - exceeds column length
```

---

### 37. Check for XSS (Cross-Site Scripting)

**Rule:** Validate input data for special characters

**Dangerous Characters:**
- `~!@#$%^&*()`
- `\r\n` (newlines)
- `<?php ?>`
- `<script>`

**Use:**
- `htmlspecialchars()` for output
- Laravel's validation rules
- Input sanitization

---

### 38. Git Workflow - Check Branch

**Rule:** Before coding, check you're on the correct branch and feature

**Commands:**
```bash
git branch              # Check current branch
git checkout feature/xxx  # Switch to correct branch
```

---

### 39. Git Workflow - Pull Before Commit

**Rule:** Always pull latest changes before committing

**Commands:**
```bash
git pull origin develop
git add .
git commit -m "message"
git push origin feature/xxx
```

---

### 40. Git Workflow - Resolve Conflicts Carefully

**Rule:** Be careful when resolving merge conflicts

**Best Practices:**
- Understand both versions of conflicting code
- Test after resolving conflicts
- Ask team member if unsure
- Don't blindly accept incoming/current changes

---

### 41. Data Format - Price Alignment

**Rule:** Price and numeric values should be right-aligned with format `99,999`

**Example:**
```
Wrong:           Correct:
$1000            $1,000
$5000000         $5,000,000
```

---

### 42. Data Format - Date Time

**Rule:** Japan date time format: `yyyy-MM-dd`

**Examples:**
- `2025-01-18`
- `2024-12-31`

**Not:**
- `18/01/2025`
- `01-18-2025`

---

### 43. Data Format - Zipcode

**Rule:** Japan zipcode format: `NNN-NNNN`

**Example:**
- `100-0001`
- `150-0043`

**Not:**
- `1000001`
- `100 0001`

---

## 📊 Summary

### Severity Levels

**CRITICAL** 🔴
- Hardcoded credentials
- SQL injection vulnerabilities
- Missing WHERE in UPDATE/DELETE
- Direct data access in controllers

**HIGH** 🟠
- Missing input validation
- Wrong data types in queries
- No parameter validation
- Loop depth > 3

**MEDIUM** 🟡
- Wrong naming conventions
- Missing comments
- Using SELECT *
- Not using strict comparison (===)

**LOW** 🟢
- Minor formatting issues
- Missing PHPDoc elements
- Using != instead of <>
- Using double quotes unnecessarily

---

**Last Updated:** 2025-11-18
**Maintained By:** Bao Tran
**Reference:** PSR-12, PHPDocumentor, Laravel Best Practices
