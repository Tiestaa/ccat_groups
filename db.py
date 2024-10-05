from cat.utils import singleton
from cat.log import log
from typing import List

import sqlite3

GROUPS_TABLE_NAME = "GROUP"
USER_IN_GROUP_TABLE_NAME = "USER_IN_GROUP"
DB_NAME = "cat.db"

""" TODO: AGGIUNGERE TUTTI I CONTROLLI """

@singleton
class sqldb:

    def is_connected(self) -> bool:
     try:
        self.conn.cursor()
        return True
     except Exception as ex:
        return False

    def insert_group(self, group_name: str, owner_id: str) -> None:
        if not self.is_connected():
            self.conn = sqlite3.connect(DB_NAME)
        
        try:
            self.conn.executescript("INSERT INTO '{GROUPS_TABLE_NAME}' (name, owner_cat_id) VALUES ('{group_name}', '{owner_id}')")
            self.conn.commit()
            log.info(f"User: {owner_id} created group: {group_name}")
        except Exception as ex:
           log.error(f"Error creating group: {group_name} by user: {owner_id} --> {ex}")
        
    
    def insert_user_in_group(self, group_name: str, user_id: str) -> None:
        if not self.is_connected():
            self.conn = sqlite3.connect(DB_NAME)

        try:
            self.conn.executescript("INSERT INTO '{USER_IN_GROUP_TABLE_NAME}' (group_name, user_id) VALUES ('{group_name}', '{user_id}')")
            self.conn.commit()
            log.info(f"User {user_id} inserted in group: {group_name}")
        except Exception as ex:
           log.error(f"Error inserting user {user_id} in group:{group_name} --> {ex}")
        

    def delete_user_in_group(self, group_name: str, user_id: str) -> None:
       "to implement"
       pass

    def getGroupsbyUser(self, user_id: str) -> List[str]:
       """ Given user, returns all accessible profile for him """
       pass

    def deleteGroup(self,user_id: str, group_name: str) -> int:
        """ Given user_id, group_name delete the group if user is the owner """
        pass

    def __init__(self):
        self.conn = sqlite3.connect(DB_NAME)
        self.conn.executescript("CREATE TABLE IF NOT EXISTS '{GROUPS_TABLE_NAME}' (name VARCHAR(255) PRIMARY KEY, owner_cat_id VARCHAR(255))")
        self.conn.executescript("CREATE TABLE IF NOT EXISTS '{USER_IN_GROUP_TABLE_NAME}' (group_name VARCHAR(255), user_id VARCHAR(255) FOREIGN KEY (group_name) REFERENCES '{GROUPS_TABLE_NAME}'(name))")

        self.conn.commit()
        log.info("D for groups support created")
            
            
