from cat.mad_hatter.decorators import tool, hook, plugin
from .db import sqldb
from .utils import *


@hook
def after_cat_bootstrap(cat):
    cat.sqldb = sqldb()


# inspired by plugin: declarative_memory_profiling
@hook
def agent_fast_reply(fast_reply, cat):

    if cat.working_memory["user_message_json"]["text"].startswith("@"):

        profile_list = cat.sqldb.getGroupsbyUser(cat.user_id)
        command = cat.working_memory["user_message_json"]["text"]

        match command[:2]:

            # change profile
            case "@p":
                profile_name = command.split(" ")[1]
                if profile_name is None or len(profile_name) == 0:
                    fast_reply["output"] = ERROR_COMMAND
                elif profile_name in profile_list:
                    fast_reply["output"] = ERROR_NAME
                else:
                    cat.working_memory[WORKING_MEMORY_KEY] = profile_name
                    fast_reply["output"] = f"Switched to profile '{profile_name}'"
            
            # create profile
            case "@c":
                profile_name = command.split(" ")[1]
                if profile_name is None or len(profile_name) == 0:
                    fast_reply["output"] = ERROR_COMMAND
                else:
                    # TODO: add error cases
                    cat.sqldb.insert_group(profile_name, cat.user_id)
                    f"{profile_name} created"

            # remove profile
            case "@r":
                profile_name = command.split(" ")[1]
                if profile_name is None or len(profile_name) == 0:
                    fast_reply["output"] = ERROR_COMMAND
                else:
                    code = cat.sqldb.deleteGroup(profile_name, cat.user_id)
                    if code == 200:
                        if cat.working_memory[WORKING_MEMORY_KEY] == profile_name:
                            cat.working_memory[WORKING_MEMORY_KEY] = None
                            fast_reply["output"] = f"{profile_name} deleted and deactivate current profile"
                        else:
                            fast_reply["output"] = f"{profile_name} deleted"
                    else:
                        # TODO: add permissions error
                        fast_reply["output"] = f"error deleting {profile_name}"

            case "@l":
                fast_reply["output"] = f"Profile list available: {'\n'.join(profile_list)}"

            case "@d":
                cat.working_memory[WORKING_MEMORY_KEY] = None
                fast_reply["output"] = f"Profile deactivated."

            case "@p":
                fast_reply["output"] = f"Active profile is: {cat.working_memory[WORKING_MEMORY_KEY]}"

            case "@h" | _ :
                fast_reply["output"] = COMMANDS
    
    return fast_reply