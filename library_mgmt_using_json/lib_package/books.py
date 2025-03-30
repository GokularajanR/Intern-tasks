import json

class catalog:
    def __init__(self):
        self.data_link = "books.json"
        self.dump_json([])
    
    def add_book(self, title:str, author:str, isbn:str) -> bool:
        try:
            temp_dict = {"title" : title, "author" : author, "isbn" : isbn}
            books = self.load_json()
            
            books.append(temp_dict)
            self.dump_json(books)
            return True
        
        except:
            print("failed")
            return False
        
    def remove_book(self, isbn:str):
        try:
            if self.isempty():
                return False
            temp_list = self.load_json()
            for i in range(len(temp_list)):
                if temp_list[i]["isbn"] == isbn:
                    del temp_list[i]
            self.dump_json(temp_list)
            return True
        except:
            return False
        
    def search_book(self, string:str):
        try:
            if self.isempty():
                return False
            temp_list = self.load_json()
            new_list = []
            string = string.lower()
            for i in range(len(temp_list)):
                if temp_list[i]["title"][:len(string)] == string or temp_list[i]["author"][:len(string)] == string:
                    new_list.append(temp_list[i])
            return new_list
        except:
            return False

    def isempty(self):
        temp_list = self.load_json()
        if len(temp_list) == 0:
            return True
        return False
    
    def load_json(self):
        try:
            with open(self.data_link,'r') as obj:
                data = json.load(obj)
            return data
        
        except:
            print("Error in loading file")
            return False
        
    def dump_json(self, data):
        try:
            with open(self.data_link,'w') as obj:
                json.dump(data, obj)
            return True
        
        except TypeError as e:
            print(e)
            return False