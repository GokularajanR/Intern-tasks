from backend import Quiz
Q = Quiz()

while True:
    print("\nMenu:")
    print("1. Get next question")
    print("2. Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
        Q.get_q()
        Q.display()
        user_answer = input("Enter your answer (1/2/3/4): ")
        Q.grade(int(user_answer))

    elif choice == "2":
        Q.stop()
        break

    else:
        print("Invalid choice. Please try again.")