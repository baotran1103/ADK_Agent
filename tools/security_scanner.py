from typing import Optional


def create_security_scanner_function():
    """
    Create security scanner function that returns structured analysis directive.
    Rules are embedded in agent instruction, no need to pass them here.
    """
    
    def scan_code_security(
        file_content: str,
        file_path: str,
        language: str
    ) -> str:
        """
        Scan code for security vulnerabilities.
        Returns minimal directive - agent has rules embedded in instruction.
        
        Args:
            file_content: Full content of the file to scan
            file_path: Path to the file (for context)
            language: Programming language (python, php, javascript, java, go, etc.)
            
        Returns:
            JSON string with scan directive (NOT full prompt)
        """
        import json
        
        # Return structured directive only - agent knows the rules
        directive = {
            "task": "security_analysis",
            "file": file_path,
            "language": language,
            "code": file_content,
            "instructions": "Analyze this code using the <security_rules> embedded in your instruction. Return JSON with findings array.",
            "categories": [
                "SQL_INJECTION", "XSS", "AUTH_BYPASS", "HARDCODED_SECRETS",
                "COMMAND_INJECTION", "PATH_TRAVERSAL", "UNSAFE_DESERIALIZATION",
                "WEAK_CRYPTO", "INFO_DISCLOSURE", "SESSION_SECURITY", "CORS"
            ]
        }
        
        return json.dumps(directive, ensure_ascii=False, indent=2)
    
    return scan_code_security
