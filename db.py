from typing import List
import sqlite3

from cat.utils import singleton
from cat.log import log

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

    # insert group in db. This throw error, handled in ccat_groups.py
    def insert_group(self, group_name: str, owner_id: str) -> None:
        if not self.is_connected():
            self.conn = sqlite3.connect(DB_PATH)
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO GROUPS (name, owner_cat_id) VALUES  (?, ?)", (group_name, owner_id))
        self.conn.commit()
        log.info(f"User: {owner_id} created group: {group_name}")

    def deleteGroup(self,group_name: str, user_id: str) -> int:
        """ Given user_id, group_name delete the group if user is the owner """
        if not self.is_connected():
            self.conn = sqlite3.connect(DB_PATH)
        cursor = self.conn.cursor()

        groupExists = cursor.execute("SELECT * FROM GROUPS WHERE GROUPS.name = ?", [group_name]).fetchone()
        if groupExists is None:
            raise HTTPexception(f"The group called {group_name} doesn't exist!", 404)
        if groupExists[1] != user_id:
            raise HTTPexception(f"{user_id} doesn't have the access to group {group_name}", 403)
        
        cursor.execute("DELETE FROM GROUPS WHERE GROUPS.name = ?", [group_name])
        self.conn.commit()
        log.info(f"User {user_id} removed group called {group_name}")

           
        
    """ Add user in group. Only the owner of group can do this. It returns the string for chat """
    def insert_user_in_group(self, group_name: str, user_id: str, owner_group: str) -> str:
        if not self.is_connected():
            self.conn = sqlite3.connect(DB_PATH)
        cursor = self.conn.cursor()

        try:
            res = cursor.execute("SELECT * FROM GROUPS WHERE GROUPS.name = ?", [group_name]).fetchone()
            if res is None:
                raise HTTPexception(f"The group called {group_name} doesn't exist!", 404)
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
            res = cursor.execute("SELECT a.name, a.owner_cat_id, b.user_id FROM GROUPS as a INNER JOIN USER_IN_GROUP as b on a.name = b.group_name WHERE a.name = ?", [group_name]).fetchone()
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

    def create_db(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.executescript("CREATE TABLE IF NOT EXISTS GROUPS (name VARCHAR(255) PRIMARY KEY, owner_cat_id VARCHAR(255))")
        self.conn.executescript("CREATE TABLE IF NOT EXISTS USER_IN_GROUP (group_name VARCHAR(255), user_id VARCHAR(255), FOREIGN KEY(group_name) REFERENCES GROUPS(name) ON DELETE CASCADE)")

        self.conn.commit()
        log.info("Database for groups support created")

    def getGroups(self) -> List[str]:
        if not self.is_connected():
            self.conn = sqlite3.connect(DB_PATH)
        cursor = self.conn.cursor()

        try:
            res = cursor.execute("SELECT a.name FROM GROUPS as a WHERE 1")
            return list(map(lambda x: x[0],res.fetchall()))
        
        except Exception as ex:
            log.error(f"Error fetching groups --> {ex}")
            return []
        
    def isGroupOwner(self, group_name: str, user_id: str) -> bool:
        if not self.is_connected():
            self.conn = sqlite3.connect(DB_PATH)
        cursor = self.conn.cursor()
        try:
            res = cursor.execute("SELECT a.owner_cat_id FROM GROUPS as a WHERE a.name = ?", [group_name]).fetchone()
            if res is None or res[0] != user_id:
                return False
            return True
        except Exception as ex:
            log.error(ex)
            return False

        
    def clearRemovedUsers(self, users_list: List[str]) -> None:
        if not self.is_connected():
            self.conn = sqlite3.connect(DB_PATH)
        cursor = self.conn.cursor()

        users_set = set(users_list)

        try:
            res = cursor.execute("SELECT a.user_id FROM USER_IN_GROUP as a WHERE 1 GROUP BY a.user_id")
            users_in_db_set = set(map(lambda x: x[0], res.fetchall()))
            users_to_remove = list(users_in_db_set - users_set)

            cursor.executemany("DELETE FROM USER_IN_GROUP as a WHERE a.user_id = ?", users_to_remove)

            self.conn.commit()

            log.info(f"Cron job called. Removed {len(users_to_remove)} users.")

        except Exception as ex:
            log.error(f"Error deleting removed users --> {ex}")



        
    def __init__(self):
        pass
            
            
