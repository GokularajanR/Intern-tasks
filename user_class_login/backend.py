class User:
    def __init__(self, username, password):
        if not username or not password:
            raise ValueError("Username or password cannot be empty")
        self.username = username
        self.__password = password
        self.failed_attempts = 0
        self.locked = False

    def login(self, password):
        if self.locked:
            print("Account is locked due to too many failed attempts.")
            return False
        

        elif password == self.__password:
            print("Login successful")
            return True
            
        else:
            self.failed_attempts += 1
            if self.failed_attempts >= 3:
                self.locked = True
                print("Account locked due to too many failed attempts")
            else:
                print("username or password incorrect")

        return False
    
class UserList:
    def __init__(self):
        self.users = {}

    def add_user(self, username, password):
        if username in self.users:
            raise ValueError("User already exists")
        self.users[username] = User(username, password)

    def get_user(self, username):
        return self.users[username] if username in self.users else None
    
    def login(self, username, password):
        user = self.get_user(username)
        if user:
            return user.login(password)
        else:
            print("User not found")
            return False