import json
import os

class User:
    def __init__(self, name:str, uid:str, ph_no:str):
        self.name = name
        self.ph_no = ph_no
        self.uid = uid

    def __repr__(self) -> str:
        return f"User name : {self.name}\nuid : {self.uid}\nphone no. : {self.ph_no}\n"

    def __str__(self) -> str:
        return f"User name : {self.name}\nuid : {self.uid}\nphone no. : {self.ph_no}\n"

    def to_dict(self):
         return {"name": self.name, "uid": self.uid, "ph_no": self.ph_no}

class User_cat:
    def __init__(self):
        self.user_list = []

    def add_user(self, user:User) -> bool:
        if not isinstance(user,User):
            return False
        for existing_user in self.user_list:
            if existing_user.uid == user.uid:
                print(f"user alr exists")
                return False
        try:
            self.user_list.append(user)
            return True
        except Exception as e: 
            print(f"erorr adding user: {e}")
            return False

    def remove_user(self, uid:str) -> bool:
        original_length = len(self.user_list)
        self.user_list = [user for user in self.user_list if user.uid != uid]
        user_was_removed = len(self.user_list) < original_length
        if not user_was_removed and not self.isempty():
             print(f"user not found")
        elif self.isempty() and original_length == 0:
             print("no users")

        return user_was_removed

    def get_user_by_uid(self, uid:str) -> User | None:
         for user in self.user_list:
             if user.uid == uid:
                 return user
         return None

    def isempty(self) -> bool:
        return len(self.user_list) == 0

    def get_all_users_as_dicts(self) -> list:
         return [user.to_dict() for user in self.user_list]

    def __str__(self) -> str:
        if self.isempty():
            return "No users added"
        ret = "Registered Users\n"
        for i in self.user_list:
            ret += str(i) + "\n"
        return ret

class catalog:
    def __init__(self, data_link="books.json"):
        self.data_link = data_link
        if not os.path.exists(self.data_link):
             self.dump_json([])
             print(f"Initialized empty book file: {self.data_link}")
        else:
            data = self.load_json()
            if data is False or not isinstance(data, list):
                print(f"Data format corrupt. Clearing json file")
                self.dump_json([])


    def add_book(self, title:str, author:str, isbn:str) -> bool:
        books = self.load_json()
        if books is False: 
             print("Failed to load books, cannot add.")
             return False

        for book in books:
            if book.get("isbn") == isbn:
                print(f"Internal check: Book ISBN {isbn} already exists.")
                return False

        try:
            temp_dict = {"title" : title, "author" : author, "isbn" : isbn}
            books.append(temp_dict)
            return self.dump_json(books)
        except Exception as e:
            print(f"Internal error adding book: {e}")
            return False

    def remove_book(self, isbn:str) -> bool:
        books = self.load_json()
        if books is False or self.isempty(books):
            print("No books in catalog")
            return False

        original_length = len(books)
        new_books_list = [book for book in books if book.get("isbn") != isbn]

        if len(new_books_list) == original_length:
            print(f"Internal check: Book ISBN {isbn} not found for removal.")
            return False

        return self.dump_json(new_books_list)


    def search_book(self, search_key:str) -> list | bool:
        books = self.load_json()
        if books is False or self.isempty(books):
             print("Cannot search cstalog is empty or failed to load.")
             return [] 

        new_list = []
        search_key_lower = search_key.lower()
        try:
            for book in books:
                title_prefix = book.get("title", "")[:len(search_key)].lower()
                author_prefix = book.get("author", "")[:len(search_key)].lower()

                if title_prefix == search_key_lower or author_prefix == search_key_lower:
                    new_list.append(book) 
            return new_list
        except Exception as e:
             print(f"Internal error during search: {e}")
             return []

    def isempty(self, book_list=None) -> bool:
        temp_list = book_list if book_list is not None else self.load_json()
        return temp_list is False or len(temp_list) == 0

    def load_json(self):
        if not os.path.exists(self.data_link):
            print(f"Error: Data file '{self.data_link}' not found.")
            return False 
        try:
            with open(self.data_link,'r') as obj:
                content = obj.read()
                if not content:
                    return [] 
                data = json.loads(content)
                if not isinstance(data, list): 
                     print(f"Error: Data in '{self.data_link}' is not a JSON list.")
                     return False
            return data
        except json.JSONDecodeError:
             print(f"Error: Could not decode JSON from '{self.data_link}'. File might be corrupt.")
             return False
        except Exception as e:
            print(f"Error in loading file '{self.data_link}': {e}")
            return False 

    def dump_json(self, data):
        try:
            with open(self.data_link,'w') as obj:
                json.dump(data, obj, indent=4)
            return True
        except TypeError as e:
            print(f"Failed to serialize data to JSON: {e}")
            return False
        except Exception as e:
             print(f"Error writing to file '{self.data_link}': {e}")
             return False