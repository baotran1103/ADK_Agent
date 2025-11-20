import os
import sys
from pathlib import Path

# Add parent directory to path to import tools
sys.path.insert(0, str(Path(__file__).parent.parent))

from google.adk.agents import Agent
from google.adk.tools.mcp_tool import McpToolset, StreamableHTTPConnectionParams

# Import tools
from tools.combined_analyzer import create_combined_analyzer_function
from tools.slack_notifier import create_slack_notifier_function

# Kết nối Remote GitHub MCP server qua HTTP với PAT
github_mcp_params = StreamableHTTPConnectionParams(
    type="http",
    url="https://api.githubcopilot.com/mcp/",
    headers={
        "Authorization": f"Bearer {os.getenv('ACCESS_TOKEN')}",
    }
)

# Khởi tạo GitHub MCPToolset
github_toolset = McpToolset(connection_params=github_mcp_params)

# Khởi tạo tools
combined_analyzer = create_combined_analyzer_function()
slack_notifier = create_slack_notifier_function() 
# Load instruction and rules from files
instruction_file = Path(__file__).parent.parent / "docs" / "AGENT_INSTRUCTION.md"
rules_file = Path(__file__).parent.parent / "rules" / "company_rules_compact.md"
security_rules_file = Path(__file__).parent.parent / "rules" / "security_rules_compact.md"

with open(instruction_file, 'r', encoding='utf-8') as f:
    BASE_INSTRUCTION = f.read()

with open(security_rules_file, 'r', encoding='utf-8') as f:
    SECURITY_RULES_TEXT = f.read()
    
with open(rules_file, 'r', encoding='utf-8') as f:
    COMPANY_RULES_TEXT = f.read()

# Build final instruction by injecting rules into base instruction
# Replace placeholder tags with actual rule content
AGENT_INSTRUCTION = BASE_INSTRUCTION.replace(
    '`<security_rules>`',
    SECURITY_RULES_TEXT
).replace(
    '`<company_rules>`',
    COMPANY_RULES_TEXT
)

# Định nghĩa Code Review Agent
root_agent = Agent(
    model="gemini-2.0-flash",
    name="code_review_assistant",
    instruction=AGENT_INSTRUCTION,
    tools=[
        github_toolset,           # GitHub operations (pull_request_read, get_file_contents)
        combined_analyzer,        # Security + company rules analysis
        slack_notifier           # Slack notifications
    ]
)
