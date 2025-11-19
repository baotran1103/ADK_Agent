# Company Coding Rules - Compact Version

> Optimized for LLM token efficiency
> Full examples: company_rules.md

---

## PHP Standards (Rules 1-7)

| ID | Rule | Check | Severity |
|----|------|-------|----------|
| R1 | PSR-12 Compliance | Code follows PSR-12, camelCase for functions/variables | MEDIUM |
| R2 | PHP Constants Lowercase | `true`, `false`, `null` phải lowercase | LOW |
| R3 | Parameter Validation | Validate params trước khi process (check null, type, range) | HIGH |
| R4 | Naming: Functions/Variables | camelCase: `getUserData()`, `$userId` | MEDIUM |
| R5 | Naming: Classes/Files | PascalCase, filename = classname: `UserController.php` | MEDIUM |
| R6 | Author Comments | Function phải có `@author lastname.firstname` | LOW |
| R7 | Namespace Declaration | Namespace ở đầu file, 1 blank line sau | LOW |

---

## MVC Patterns (Rules 8-13)

| ID | Rule | Check | Severity |
|----|------|-------|----------|
| R8 | No Direct Data Access | Controller không dùng `DB::table()` trực tiếp, phải qua Model | CRITICAL |
| R9 | Controller Method Visibility | Chỉ action methods là `public`, helpers là `private` | MEDIUM |
| R10 | Common Functions in BaseController | Shared logic phải ở BaseController | MEDIUM |
| R11 | System Logging | Dùng `Log::info()`, `Log::error()` cho operations | MEDIUM |
| R12 | Input Validation | MUST validate input với `$request->validate()` | CRITICAL |
| R13 | Loop Depth < 4 | Nested loops không quá 3 levels | HIGH |

---

## Performance (Rules 14-18)

| ID | Rule | Check | Severity |
|----|------|-------|----------|
| R14 | Singleton Pattern | Class có `__construct()` nên dùng singleton | MEDIUM |
| R15 | Strict Comparison (===) | Dùng `===` thay vì `==` | MEDIUM |
| R16 | No Loop Function Calls | Không loop function có thể process array | MEDIUM |
| R17 | String Quoting | Single quotes `'text'`, double chỉ khi cần parse `"$var"` | LOW |
| R18 | Calculate Once | Assign giá trị vào variable nếu dùng nhiều lần | LOW |

---

## SQL Standards (Rules 19-27)

| ID | Rule | Check | Severity |
|----|------|-------|----------|
| R19 | Uppercase SQL Keywords | `SELECT`, `FROM`, `WHERE` phải UPPERCASE | LOW |
| R20 | Correct Data Types in WHERE | INT không quote: `WHERE id = 1` (không phải `'1'`) | LOW |
| R21 | No Reserved Words as Aliases | Không dùng MySQL function names làm alias | MEDIUM |
| R22 | No SELECT * | Specify columns: `SELECT id, name` không `SELECT *` | MEDIUM |
| R23 | COUNT with Indexed Column | `COUNT(id)` thay vì `COUNT(*)` | MEDIUM |
| R24 | Use <> not != | `WHERE status <> 'done'` | LOW |
| R25 | WHERE in UPDATE Required | UPDATE phải có WHERE clause | CRITICAL |
| R26 | Use Indexes | Index foreign keys, WHERE columns, JOIN columns | HIGH |
| R27 | Handle NULL Properly | `IS NULL` / `IS NOT NULL`, không dùng `= NULL` | MEDIUM |

---

## Comment Standards (Rules 28-32)

| ID | Rule | Check | Severity |
|----|------|-------|----------|
| R28 | File Comment | PHPDoc với `@package`, `@author` | LOW |
| R29 | Class Comment | PHPDoc với description, `@author` | LOW |
| R30 | Function Comment | PHPDoc: description, `@param`, `@return`, `@author`, `@lastupdate` | MEDIUM |
| R31 | Variable Comment | `@var type description` cho class properties | LOW |
| R32 | Condition Comment | Comment cho complex logic | LOW |

---

## Pre-Deployment Checklist (Rules 33-43)

| ID | Rule | Check | Severity |
|----|------|-------|----------|
| R33 | Bulk Insert | Large data (>1000 rows) dùng `array_chunk()` + bulk insert | HIGH |
| R34 | Test Batch Processing | Test với large dataset, monitor memory/time | MEDIUM |
| R35 | Validate Numeric Bounds | Check min/max theo DB data type (INT max: 2,147,483,647) | HIGH |
| R36 | Validate String Length | Check length theo DB column size (VARCHAR(255)) | HIGH |
| R37 | Check for XSS | Validate special chars, dùng `htmlspecialchars()` | CRITICAL |
| R38 | Git: Check Branch | Confirm đúng branch trước khi code | LOW |
| R39 | Git: Pull Before Commit | `git pull` trước khi commit | LOW |
| R40 | Git: Resolve Conflicts Carefully | Hiểu cả 2 versions, test sau khi resolve | MEDIUM |
| R41 | Format: Price Alignment | Right-aligned, format `99,999` | LOW |
| R42 | Format: Date Time | Japan format `yyyy-MM-dd` | LOW |
| R43 | Format: Zipcode | Japan format `NNN-NNNN` | LOW |

---

## Severity Summary

**CRITICAL** 🔴 (Block merge)
- R8: Direct DB access in controller
- R12: Missing input validation  
- R25: UPDATE without WHERE
- R37: XSS vulnerabilities

**HIGH** 🟠 (Request changes)
- R3: No parameter validation
- R13: Loop depth > 3
- R26: Missing indexes
- R33: Large data without bulk insert
- R35-36: Bounds/length validation

**MEDIUM** 🟡 (Warning)
- R1, R4-5, R9-11, R14-16, R21-23, R27, R30, R34, R40

**LOW** 🟢 (Info)
- R2, R6-7, R17-20, R24, R28-29, R31-32, R38-39, R41-43

---

**Total: 43 rules | Token count: ~150 lines vs 816 lines (81% reduction)**
