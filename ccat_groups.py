from cat.mad_hatter.decorators import tool, hook, plugin
from .db import sqldb
from .utils import *


# inspired by plugin: declarative_memory_profiling

@hook
def after_cat_bootstrap(cat):
    sqldb().create_db()

@hook
def before_rabbithole_insert_memory(doc, cat):
    # insert metadata about user and group
    if cat.working_memory[WORKING_MEMORY_KEY] != None:
        doc.metadata['profile'] = cat.working_memory[WORKING_MEMORY_KEY]

    doc.metadata["user_id"] = cat.user_id
    return doc

@hook
def before_cat_recalls_declarative_memories(declarative_recall_config, cat):

    if (WORKING_MEMORY_KEY in cat.working_memory and cat.working_memory[WORKING_MEMORY_KEY] != None):
        declarative_recall_config["metadata"] = {"profile": cat.working_memory[WORKING_MEMORY_KEY]}
    else:
         declarative_recall_config["metadata"] = {"user_id": cat.user_id}

    return declarative_recall_config


@hook()
def agent_fast_reply(fast_reply, cat):

    if WORKING_MEMORY_KEY not in cat.working_memory:
        cat.working_memory[WORKING_MEMORY_KEY] = None

    if cat.working_memory.user_message_json.text.startswith("@"):

        db = sqldb()

        profile_list = db.getGroupsbyUser(cat.user_id)

        command = cat.working_memory["user_message_json"]["text"]

        match command[:2]:

            # change profile
            case "@p":
                if len(command.split(" ")) < 2:
                    fast_reply["output"] = f"Active profile is: {cat.working_memory[WORKING_MEMORY_KEY]}"
                elif len(command.split(" ")) > 2:
                    fast_reply["output"] = ERROR_COMMAND
                else:
                    profile_name = command.split(" ")[1]
                    if profile_name not in profile_list:
                        fast_reply["output"] = ERROR_NAME
                    else:
                        cat.working_memory[WORKING_MEMORY_KEY] = profile_name
                        fast_reply["output"] = f"Switched to profile '{profile_name}'"
            
            # create profile
            case "@c":
                if len(command.split(" ")) < 2:
                    fast_reply["output"] = ERROR_COMMAND
                else:
                    profile_name = command.split(" ")[1]
                    # TODO: add error cases
                    db.insert_group(profile_name, cat.user_id)
                    fast_reply["output"] = f"{profile_name} created"

            # remove profile
            case "@r":
                if len(command.split(" ")) < 2:
                    fast_reply["output"] = ERROR_COMMAND
                else:
                    profile_name = command.split(" ")[1]
                    code = db.deleteGroup(profile_name, cat.user_id)
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
                formatted_list = "\n- ".join(['',*profile_list])
                fast_reply["output"] = f"Profile list available: {formatted_list}"

            case "@d":
                cat.working_memory[WORKING_MEMORY_KEY] = None
                fast_reply["output"] = f"Profile deactivated."

            case "@h":
                fast_reply["output"] = COMMANDS
            case _:
                fast_reply["output"] = ERROR_COMMAND
    
    return fast_reply