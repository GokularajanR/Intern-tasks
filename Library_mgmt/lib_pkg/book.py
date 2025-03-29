class Book:
    def __init__(self, title:str, author:str, isbn:str):
        self.title = title
        self.isbn = isbn
        self.author = author
        self.status = True

    def __repr__(self) -> str:
        return f"Book name : {self.title}\nAuthor name : {self.author}\nISBN : {self.isbn}\n"
    
    def __str__(self):
        return f"Book name : {self.title}\nAuthor name : {self.author}\nISBN : {self.isbn}\n"

    
    def get_avail(self):
        return self.status
    
class Catalog:
    def __init__(self):
        self.book_list = []
    
    def add_book(self, book:Book) -> bool:
        try:
            if not isinstance(book,Book):
                return
            self.book_list.append(book)
            return True
        except:
            return False
        
    def remove_book(self, isbn:str) -> bool:
        try:
            if self.isempty():
                print("catalog empty")
                return False
            for i in range(len(self.book_list)):
                if self.book_list[i].isbn == isbn :
                    del self.book_list[i]
                    return True
            return False
        
        except:
            return False
        
    def search_book(self, key:str = " ") -> list:
        try:
            if self.isempty():
                print("catalog empty")
                return None
            if key == " ":
                return self.book_list
            
            search_res = []
            key_len = len(key)
            for i in self.book_list:
                if i.title[:key_len] == key or i.author[:key_len] == key :
                    search_res.append(i)
            return search_res
        except:
            return None
        
    def isempty(self) -> bool:
        if len(self.book_list) == 0:
            return True
        return False
    
    def __str__(self) -> str:
        ret = "\n"
        for i in self.book_list:
            ret = ret + str(i)
        
        return "No books added" if self.isempty() else ret