from pydantic import BaseModel
from cat.experimental.form import form, CatForm
from .db import sqldb

"""
    TODO
    1. aggiungere validator che prenda user che esistano
    2. personalizzare il messaggio che mostra utenti e id disponibili da poter aggiugnere
    3. solo groups che esistono (collegato a 1)
"""

class UserInfo(BaseModel):
    user_id: str
    group_name: str

@form
class UserInsertGroupForm(CatForm):
    description = "Add user in group "
    model_class = UserInfo
    start_examples = [
        "insert user in group",
        "add user in group",
        "extend the group"
    ]

    stop_examples = [
        "stop adding a user in group",
        "stop inserting user",
    ]

    ask_confirm = True

    def submit(self, form_data):
        db = sqldb()
        user_id = form_data["user_id"]
        group_name = form_data["group_name"]

        db.insert_user_in_group(group_name, user_id)

        return {
            "output": f"Inserted user {user_id} in group {group_name}"
        }

@form
class UserDeleteGroupForm(CatForm):
    description = "Delete user from group"
    model_class = UserInfo
    start_examples = [
        "delete user from a group",
        "remove user from a group"
    ]

    stop_examples = [
        "stop deleting the user from a group",
        "stop removing user"
    ]

    ask_confirm = True

    def submit(self, form_data):
        db = sqldb()
        user_id = form_data["user_id"]
        group_name = form_data["group_name"]

        db.delete_user_in_group(group_name, user_id)
        
        return {
            "output": f"Deleted user {user_id} from group {group_name}"
        }


