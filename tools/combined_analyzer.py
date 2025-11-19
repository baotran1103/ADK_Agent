"""
Combined analysis tool that performs both security and rules checking in one call.
Reduces token usage by 50% by eliminating duplicate tool invocations.
"""
import json

def create_combined_analyzer_function():
    """
    Create combined analyzer that checks both security and company rules.
    Returns minimal directive - agent knows rules from instruction.
    """
    
    def analyze_code_complete(
        file_content: str,
        file_path: str,
        language: str
    ) -> str:
        """
        Comprehensive code analysis - security + company rules in ONE call.
        Agent has both <security_rules> and <company_rules> embedded in instruction.
        
        Args:
            file_content: Full content of the file to analyze
            file_path: Path to the file (for context)
            language: Programming language (python, php, javascript, java, go, etc.)
            
        Returns:
            Instruction to analyze code (agent will use embedded rules)
        """
        
        # Return friendly analysis request
        return f"""Đang phân tích file: {file_path}

📋 **File Info**
- Language: {language}
- Lines: {len(file_content.splitlines())}

🔍 **Analysis Tasks**
- Security scan (11 categories from <security_rules>)
- Coding standards check (43 rules from <company_rules>)

---

**Code to analyze:**
```{language}
{file_content}
```

---

Hãy check kỹ từng dòng code và trả về kết quả theo format JSON gọn gàng nhé! 🎯"""
    
    return analyze_code_complete
