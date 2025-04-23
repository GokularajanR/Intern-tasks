from backend import UserList

obj = UserList()
obj.add_user("Gokul", "gulugulu")
obj.add_user("Ayush", "pizzapasta")
obj.add_user("Yuva", "guava")

obj.login("Gokul", "gulugulu")
obj.login("Gokul", "wrongpassword")
obj.login("Gokul", "wrongpassword")
obj.login("Gokul", "wrongpassword") #Limit reached
obj.login("Gokul", "gulugulu") #Account locked
obj.login("Ayush", "pizzapasta") #Works fine