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
            JSON directive with file content for analysis
        """
        
        # Return structured JSON directive
        result = {
            "action": "ANALYZE_NOW",
            "file_path": file_path,
            "language": language,
            "lines_count": len(file_content.splitlines()),
            "code": file_content,
            "instruction": "Analyze this code using your embedded <security_rules> and <company_rules>. Find all security vulnerabilities and coding standard violations. Return findings in the report format."
        }
        
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    return analyze_code_complete
