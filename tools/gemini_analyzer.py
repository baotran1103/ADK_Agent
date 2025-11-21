"""
Gemini AI Code Analyzer - Fast analysis for all rules
Returns directive for agent to analyze using embedded rules
"""
import json


def create_gemini_analyzer_function():
    """
    Gemini-based analyzer for quick comprehensive analysis.
    Checks company rules (R1-R43) + basic security.
    """
    
    def analyze_with_gemini(
        file_content: str,
        file_path: str,
        language: str
    ) -> str:
        """
        Quick AI analysis using embedded rules.
        
        Args:
            file_content: Full file content
            file_path: File path
            language: Programming language (php, python, js, etc.)
            
        Returns:
            JSON directive with code for analysis
        """
        
        result = {
            "action": "ANALYZE_WITH_RULES",
            "file_path": file_path,
            "language": language,
            "lines": len(file_content.splitlines()),
            "code": file_content,
            "instruction": "Analyze using <security_rules> and <company_rules>. Return all findings with severity, line numbers, and rule IDs."
        }
        
        return json.dumps(result, ensure_ascii=False)
    
    return analyze_with_gemini
