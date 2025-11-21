"""
Semgrep Security Scanner - Deep scan for CRITICAL/HIGH vulnerabilities.
Only called when Gemini finds potential security issues.
"""
import json
import subprocess
import tempfile
import os
from pathlib import Path


def create_semgrep_scanner_function():
    """
    Semgrep scanner for deep security analysis.
    Only use for CRITICAL/HIGH severity verification.
    """
    
    def scan_with_semgrep(
        file_content: str,
        file_path: str,
        language: str
    ) -> str:
        """
        Deep security scan using Semgrep.
        
        Args:
            file_content: Full file content
            file_path: File path (for extension)
            language: Programming language
            
        Returns:
            JSON with Semgrep findings
        """
        
        try:
            # Detect file extension
            ext_map = {
                "php": ".php",
                "python": ".py",
                "javascript": ".js",
                "java": ".java",
                "go": ".go",
                "ruby": ".rb"
            }
            ext = ext_map.get(language.lower(), ".txt")
            
            # Write to temp file
            with tempfile.NamedTemporaryFile(mode='w', suffix=ext, delete=False) as f:
                f.write(file_content)
                temp_path = f.name
            
            # Run Semgrep with security ruleset
            cmd = [
                "semgrep",
                "--config=auto",  # Auto-detect rules
                "--json",
                "--severity=ERROR",  # Only CRITICAL/HIGH
                "--severity=WARNING",
                temp_path
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # Clean up
            os.unlink(temp_path)
            
            if result.returncode in [0, 1]:  # 0=clean, 1=findings
                findings = json.loads(result.stdout)
                
                # Parse results
                issues = []
                for finding in findings.get("results", []):
                    issues.append({
                        "rule_id": finding.get("check_id", ""),
                        "severity": finding.get("extra", {}).get("severity", "MEDIUM"),
                        "message": finding.get("extra", {}).get("message", ""),
                        "line": finding.get("start", {}).get("line", 0),
                        "code": finding.get("extra", {}).get("lines", "")
                    })
                
                return json.dumps({
                    "status": "success",
                    "tool": "semgrep",
                    "file": file_path,
                    "total_issues": len(issues),
                    "issues": issues
                }, ensure_ascii=False, indent=2)
            
            else:
                return json.dumps({
                    "status": "error",
                    "message": result.stderr
                }, ensure_ascii=False)
                
        except subprocess.TimeoutExpired:
            return json.dumps({
                "status": "error",
                "message": "Semgrep timeout (>30s)"
            }, ensure_ascii=False)
            
        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": f"Semgrep failed: {str(e)}"
            }, ensure_ascii=False)
    
    return scan_with_semgrep
