class User:
    def __init__(self, name:str, uid:str, ph_no:str):
        self.name = name
        self.ph_no = ph_no
        self.uid = uid

    def __repr__(self) -> str:
        return f"User name : {self.name}\nuid : {self.uid}\nphone no. : {self.ph_no}\n"
    
    def __str__(self) -> str:
        return f"User name : {self.name}\nuid : {self.uid}\nphone no. : {self.ph_no}\n"
    
class User_cat:
    def __init__(self):
        self.user_list = []
    
    def add_user(self, user:User) -> bool:
        try:
            if not isinstance(user,User):
                return
            self.user_list.append(user)
            return True
        except:
            return False
        
    def remove_user(self, uid:str) -> bool:
        try:
            if self.isempty():
                print("No registered users")
                return False
            for i in range(len(self.user_list)):
                if self.user_list[i].uid == uid :
                    del self.user_list[i]
                    return True
            return False
        
        except:
            return False
        
    def isempty(self) -> bool:
        if len(self.user_list) == 0:
            return True
        return False
    
    def __str__(self) -> str:
        ret = "\n"
        for i in self.user_list:
            ret = ret + str(i)

        return "No users added" if self.isempty() else ret
