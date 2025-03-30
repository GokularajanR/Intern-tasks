from lib_package import User,catalog,User_cat

cat = catalog()
users = User_cat()
    
def main():
    while True:
        print("\n\nMenu:")
        print("1. Add User")
        print("2. Remove User")
        print("3. Add Book")
        print("4. Remove Book")
        print("5. Search Book")
        print("6. Display Books")
        print("7. Display Users")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter name : ")
            uid = input("Enter UID : ")
            phno = input("Enter phone number : ")
            users.add_user(User(name,uid,phno))

        elif choice == "2":
            uid = input("Enter UID of user to remove : ")
            users.remove_user(uid)

        elif choice == "3":
            title = input("Enter book title : ")
            auth = input("Enter Author : ")
            isbn = input("Enter ISBN code : ")
            cat.add_book(title, auth, isbn)

        elif choice == "4":
            isbn = input("Enter ISBN of user to remove : ")
            cat.remove_book(isbn)

        elif choice == "5":
            key = input("Enter search key (searches name and author)")
            print(cat.search_book(key))

        elif choice == "6":
            print(cat)

        elif choice == "7":
            print(users)

        elif choice == "8":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()