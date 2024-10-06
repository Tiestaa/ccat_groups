from cat.utils import singleton
from cat.log import log

from typing import List

import sqlite3

from .HTTPexception import HTTPexception

DB_PATH = "/app/cat/data/cat.db"


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
            self.conn = sqlite3.connect(DB_PATH)
        cursor = self.conn.cursor()
        
        try:
            cursor.execute("INSERT INTO GROUPS (name, owner_cat_id) VALUES  (?, ?)", (group_name, owner_id))
            self.conn.commit()
            log.info(f"User: {owner_id} created group: {group_name}")
        except Exception as ex:
           log.error(f"Error creating group: {group_name} by user: {owner_id} --> {ex}")
        
    """ Add user in group. Only the owner of group can do this. It returns the string for chat """
    def insert_user_in_group(self, group_name: str, user_id: str, owner_group: str) -> str:
        if not self.is_connected():
            self.conn = sqlite3.connect(DB_PATH)
        cursor = self.conn.cursor()

        try:
            res = cursor.execute("SELECT * FROM GROUPS WHERE GROUPS.name = ?", [group_name]).fetchone()
            if res is None:
                raise HTTPexception(f"The group name {group_name} doesn't exist!", 404)
            if res[1] != owner_group:
                raise HTTPexception(f"{user_id} doesn't have the access to group {group_name}", 403)

            cursor.execute("INSERT INTO USER_IN_GROUP (group_name, user_id) VALUES (?, ?)", (group_name, user_id))
            self.conn.commit()
            log.info(f"User {user_id} inserted in group {group_name}")
            return f"User {user_id} inserted in group {group_name}"
        except Exception as ex:
           log.error(f"Error inserting user {user_id} in group:{group_name} --> {ex}")
           return f"Error inserting user {user_id} in group {group_name} --> {ex}"

    def delete_user_in_group(self, group_name: str, user_id: str, owner_group: str) -> None:
        if not self.is_connected():
            self.conn = sqlite3.connect(DB_PATH)
        cursor = self.conn.cursor()

        try:
            res = cursor.execute("SELECT a.name, a.ownowner_cat_id, b.user_id FROM GROUPS as a INNER JOIN USER_IN_GROUP as b on a.name = b.group_name WHERE a.name = ?", [group_name]).fetchone()
            log.warning(res)
            if res is None:
                raise HTTPexception(f"The group name {group_name} or user {user_id} doesn't exist!", 404)
            if res[1] != owner_group:
                raise HTTPexception(f"{user_id} doesn't have the access to group {group_name}", 403)

            cursor.execute("DELETE FROM USER_IN_GROUP WHERE group_name = ? AND user_id = ?", (group_name, user_id))
            self.conn.commit()
            log.info(f"User {user_id} deleted from group {group_name}")
            return f"User {user_id} deleted from group {group_name}"
        
        except Exception as ex:
           log.error(f"Error deleting user {user_id} from group:{group_name} --> {ex}")
           return f"Error deleting user {user_id} from group {group_name} --> {ex}"

    def getGroupsbyUser(self, user_id: str) -> List[str]:
        """ Given user, returns all accessible profile for him """
        if not self.is_connected():
            self.conn = sqlite3.connect(DB_PATH)
        cursor = self.conn.cursor()

        try:

            res = cursor.execute("""
            SELECT a.group_name
            FROM USER_IN_GROUP as a
            WHERE a.user_id = ?
            UNION
            SELECT b.name
            FROM GROUPS as b
            WHERE b.owner_cat_id = ?
            """, (user_id, user_id))
            profiles = list(map(lambda x: x[0],res.fetchall()))
            return profiles
        except Exception as ex:
            log.error(f"Error fetching profile groups based on used_id: {user_id} --> {ex}")
            return []

    def deleteGroup(self,user_id: str, group_name: str) -> int:
        """ Given user_id, group_name delete the group if user is the owner """
        pass

    def create_db(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.executescript("CREATE TABLE IF NOT EXISTS GROUPS (name VARCHAR(255) PRIMARY KEY, owner_cat_id VARCHAR(255))")
        self.conn.executescript("CREATE TABLE IF NOT EXISTS USER_IN_GROUP (group_name VARCHAR(255), user_id VARCHAR(255), FOREIGN KEY(group_name) REFERENCES '{GROUPS_TABLE_NAME}'(name))")

        self.conn.commit()
        log.info("Database for groups support created")

    def getGroups(self) -> List[str]:
        if not self.is_connected():
            self.conn = sqlite3.connect(DB_PATH)
        cursor = self.conn.cursor()

        try:
            res = cursor.execute("SELECT a.name FROM GROUPS WHERE 1")
            return list(map(lambda x: x[0],res.fetchall()))
        
        except Exception as ex:
            log.error(f"Error fetching groups --> {ex}")
            return []
        
    def __init__(self):
        pass
            
            
