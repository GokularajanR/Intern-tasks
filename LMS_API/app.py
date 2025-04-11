# cli_client.py
import requests
import json

API_BASE_URL = "http://127.0.0.1:8000"

def print_response(response):
    print("-" * 20)
    try:
        if 200 <= response.status_code < 300:
            print(f"API Call Successful (Status: {response.status_code})")
            try:
                data = response.json()
                if isinstance(data, (dict, list)):
                    print(json.dumps(data, indent=2))
                else:
                    print(data)
            except json.JSONDecodeError:
                 print(f"Response Content: {response.text}")
        else:
            print(f"API Error (Status: {response.status_code})")
            try:
                error_details = response.json()
                print(f"  Error Detail: {error_details.get('detail', 'No detail provided')}")
            except json.JSONDecodeError:
                print(f"  Error Content: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Network Error connecting to API: {e}")
    print("-" * 20)


def main():
    while True:
        print("\n\nLibrary Management System Menu (via API v1.1):")
        print("1. Add User")
        print("2. Remove User")
        print("3. Add Book")
        print("4. Remove Book")
        print("5. Search Book (by Title/Author Prefix)")
        print("6. Display Books")
        print("7. Display Users")
        print("8. Exit")

        choice = input("Enter your choice: ")

        try:
            if choice == "1":
                name = input("Enter name : ")
                uid = input("Enter UID : ")
                ph_no = input("Enter phone number : ")
                if not all([name, uid, ph_no]):
                    print("Error: Name, UID, and Phone Number cannot be empty.")
                    continue
                payload = {"name": name, "uid": uid, "ph_no": ph_no}
                response = requests.post(f"{API_BASE_URL}/users", json=payload)
                print_response(response)

            elif choice == "2":
                uid = input("Enter UID of user to remove : ")
                if not uid:
                    print("UID cannot be empty.")
                    continue
                response = requests.delete(f"{API_BASE_URL}/users/{uid}")
                print_response(response)

            elif choice == "3":
                title = input("Enter book title : ")
                auth = input("Enter Author : ")
                isbn = input("Enter ISBN code : ")
                if not all([title, auth, isbn]):
                     print("Error: Title, Author, and ISBN cannot be empty.")
                     continue
                payload = {"title": title, "author": auth, "isbn": isbn}
                response = requests.post(f"{API_BASE_URL}/books", json=payload)
                print_response(response)

            elif choice == "4":
                isbn = input("Enter ISBN of book to remove : ")
                if not isbn:
                    print("ISBN cannot be empty.")
                    continue
                response = requests.delete(f"{API_BASE_URL}/books/{isbn}")
                print_response(response)

            elif choice == "5":
                key = input("Enter search key (title/author): ")
                response = requests.get(f"{API_BASE_URL}/books/search", params={"key": key})
                print_response(response)

            elif choice == "6":
                response = requests.get(f"{API_BASE_URL}/books")
                print_response(response)

            elif choice == "7":
                response = requests.get(f"{API_BASE_URL}/users")
                print_response(response)

            elif choice == "8":
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")

        except Exception as e:
             print(f"\nAn unexpected client-side error occurred: {e}")


if __name__ == "__main__":
    main()