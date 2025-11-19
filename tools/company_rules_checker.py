def create_rules_checker_function():
    """
    Create company rules checker function that returns structured analysis directive.
    Rules are embedded in agent instruction, no need to pass them here.
    """
    
    def check_company_rules(
        file_content: str,
        file_path: str,
        language: str
    ) -> str:
        """
        Check code against company coding rules.
        Returns minimal directive - agent has rules embedded in instruction.
        
        Args:
            file_content: Full content of the file to check
            file_path: Path to the file (for context)
            language: Programming language (python, php, javascript, java, go, etc.)
            
        Returns:
            JSON string with check directive (NOT full prompt)
        """
        import json
        
        # Return structured directive only - agent knows the rules
        directive = {
            "task": "rules_compliance_check",
            "file": file_path,
            "language": language,
            "code": file_content,
            "instructions": "Check this code using the <company_rules> embedded in your instruction. Return JSON with violations array.",
            "rules_to_check": [
                "R1-R5: Naming conventions",
                "R6-R10: Code structure",
                "R11-R15: Comments & docs",
                "R16-R20: Error handling",
                "R21-R25: Performance",
                "R26-R30: Security basics",
                "R31-R35: Testing",
                "R36-R40: Git & versioning",
                "R41-R43: Dependencies"
            ]
        }
        
        return json.dumps(directive, ensure_ascii=False, indent=2)
    
    return check_company_rules
