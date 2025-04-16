import json
import os

class User_catalog:
    def __init__(self, data_link="users.json"):
        self.data_link = data_link
        if not os.path.exists(self.data_link):
             self.dump_json([])
             print(f"Initialized empty user file: {self.data_link}")
        else:
            data = self.load_json()
            if data is False or not isinstance(data, list):
                print(f"Data format corrupt. Clearing json file")
                self.dump_json([])

    def load_json(self):
        if not os.path.exists(self.data_link):
            print("file not found")
            return [] 
        try:
            with open(self.data_link, 'r') as fileobj:
                content = fileobj.read()
                if not content:
                    return []
                data = json.loads(content)
                if not isinstance(data, list):
                     print("Data corrupt")
                     return False
            return data
        except Exception as e:
            print(f"internal error : {e}")
            return False

    def dump_json(self, data):
        try:
            with open(self.data_link, 'w') as obj:
                json.dump(data, obj, indent=4)
            return True
        except Exception as e:
             print(f"error writing to user file : {e}")
             return False

    def add_user(self, name: str, uid: str, ph_no: str) -> bool:
        users = self.load_json()
        if users is False: # Check for load failure
             print("Failed to load user data, cannot add user.")
             return False

        for existing_user in users:
            if existing_user.get("uid") == uid:
                print(f"User with UID '{uid}' already exists.")
                return False

        new_user_dict = {"name": name, "uid": uid, "ph_no": ph_no}

        users.append(new_user_dict)
        if self.dump_json(users):
            print(f"User '{name}' ({uid}) added successfully.")
            return True
        else:
            print(f"Failed to save user data after adding user '{name}'.")
            return False

    def remove_user(self, uid: str) -> bool:
        users = self.load_json()
        if users is False:
            print("Failed to load user data, cannot remove user.")
            return False
        if not users: 
             print("User catalog is empty. Cannot remove user.")
             return False

        original_length = len(users)
        new_users_list = [user for user in users if user.get("uid") != uid]

        if len(new_users_list) == original_length:
            print(f"user not found")
            return False
        else:
            if self.dump_json(new_users_list):
                print(f"Success")
                return True
            else:
                print(f"file save failed")
                return False

    def get_user_by_uid(self, uid: str) -> dict | None:
        users = self.load_json()
        if users is False:
             print("user load failed")
             return None
        
        for user in users:
             if user.get("uid") == uid:
                 return user 
        print("User not found.")
        return None

    def isempty(self) -> bool:
        users = self.load_json()
        return users is False or len(users) == 0

    def get_all_users(self) -> list:
        users = self.load_json()
        if users is False:
            print("user load failed")
            return []
        return users 

    def __str__(self) -> str:
        users = self.load_json()

        ret = ""
        for user in users:
            name = user.get('name', 'N/A')
            uid = user.get('uid', 'N/A')
            ph_no = user.get('ph_no', 'N/A')
            ret += f"User name : {name}\nuid : {uid}\nphone no. : {ph_no}\n\n"
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