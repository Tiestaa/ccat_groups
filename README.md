# Ccat Groups

[![Ccat Groups](https://raw.githubusercontent.com/Tiestaa/ccat_groups/main/ccat_groups.png)](https://) 


[![awesome plugin](https://custom-icon-badges.demolab.com/static/v1?label=&message=awesome+plugin&color=383938&style=for-the-badge&logo=cheshire_cat_ai)](https://)  

## Usage
1. Install and activate the plugin
2. Use chat to select commands.
```python
Commands available:
Help page for declarative memory profiling. Commands available:
[@p group_name]     - changes the current group to group_name
[@c gorup_name]     - creates a group named group_name
[@r group_name]     - deletes the group named group_name
[@p]                - prints active group  
[@l]                - gets groups' list for current session
[@d]                - deactivates profiling. Active groups is set to None
[@h]                - help 
```
3. Add user in group using Forms! Just send a message to chat like `insert user ... in group ...` and provide all the information required. You can send `remove user ... from group ...` to remove the user from the selected group.

> Note:
> At the moment, the only one who can add or remove users from groups is the group owner.
> Only the group owner can upload documents in group.
> To add user to a group, group owner must have the permission to READ from USERS
> 
> This plugin doesn't cause the loss of generality. By deactivating profiling (using`@d`), the standard behaviour will be restored

### Example
1. User `admin` creates a group called `test` and switches the current group to test by using  `@p test`
2. `admin` uploads documents to Rabbit Hole.
3. `admin` adds the user `pippo` to `test`
4. `pippo` can use command `@l` to get the groups' list, that includes the group `test`
5. `pippo` can switch his active group to `test` by using command: `@p test`
6. ⁠When ⁠ `pippo` ⁠ makes a query about something, the retrieval phase includes all the documents previously uploaded by the admin belonging to the group `test`


## Todo
- [ ] Add recursive groups?
- [ ] Handle permissions in a better way. (SQL table for permissions?  Like in social network, a group can have more than one admin)

> Note
> This plugin takes inpiration from profiling plugin: https://github.com/marcoserafini2/declarative_memory_profiling/tree/main