from pydantic import BaseModel,ValidationError,ValidationInfo,field_validator
from typing import List, Dict

from cat.experimental.form import form, CatForm, CatFormState
from cat.db import crud
from cat.log import log

from .db import sqldb

def getUserPermission(username: str) -> Dict:
   for key, value in crud.get_users().items():
       if value['username'] == username:
           return value['permissions']

class UserInfo(BaseModel):
    user_id: str
    group_name: str

    @field_validator('user_id')
    @classmethod
    def userExists(cls, value: str)-> str:
        users = list(map(lambda x: x[1]['username'],crud.get_users().items()))
        if value not in users:
            raise ValueError(f"user '{value}' does't exists")
        else:
            return value
        
    @field_validator('group_name')
    @classmethod
    def userExists(cls, value: str)-> str:
        groups = sqldb().getGroups()
        if value not in groups:
            raise ValueError(f"group '{value}' does't exists")
        else:
            return value

@form
class UserInsertGroupForm(CatForm):
    description = "Add user in group"
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

    def next(self):
        user_permission = getUserPermission(self.cat.user_id)
        if ("USERS" not in user_permission) or ("READ" not in user_permission['USERS']):
            return {"output": "Permissions not valid"}
        else:
            return super().next()

    def submit(self, form_data):
        db = sqldb()
        user_id = form_data["user_id"]
        group_name = form_data["group_name"]

        ret = db.insert_user_in_group(group_name, user_id, self.cat.user_id)

        return {
            "output": ret
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

        ret = db.delete_user_in_group(group_name, user_id, self.cat.user_id)
        
        return {
            "output": ret
        }


