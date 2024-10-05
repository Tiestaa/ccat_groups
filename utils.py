from typing import Final
COMMANDS: Final[str] = """
Help page for declarative memory profiling. Commands available:
[@p profile_name]   - change to profile_name
[@c profile_name]   - create profile_name
[@r profile_name]   - remove profile_name
[@l]                - get list of profile for user
[@d]                - deactivate profiling. No active profile
[@p]                - print current profile_name              
[@h]                - help 
"""

ERROR_COMMAND: Final[str] = """
Error during profiling. Call @h for help.
"""

WORKING_MEMORY_KEY: Final[str] = 'declarative_memory_profile'

ERROR_NAME: Final[str] = """
Invalid profile name
"""
