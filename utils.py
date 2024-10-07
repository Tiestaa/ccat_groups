from typing import Final
COMMANDS: Final[str] = """
Help page for declarative memory profiling. Commands available:
[@p group_name]     - changes the current group to group_name
[@c gorup_name]     - creates a group named group_name
[@r group_name]     - deletes the group named group_name
[@p]                - prints active group  
[@l]                - gets groups' list for current session
[@d]                - deactivates profiling. Active groups is set to None
[@h]                - help 
"""

ERROR_COMMAND: Final[str] = """
Error during profiling. Call @h for help.
"""

WORKING_MEMORY_KEY: Final[str] = 'declarative_memory_profile'

ERROR_NAME: Final[str] = """
Invalid group name
"""
