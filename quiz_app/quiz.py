URL = "https://opentdb.com/api.php?amount=1&category=17&difficulty=hard&type=multiple" #Using opentdb API for quiz questions
import requests
import random

def get_q():
    response = requests.get(URL)
    q = response.json()['results'][0]['question']
    ans = response.json()['results'][0]['correct_answer']
    wrong_ans = response.json()['results'][0]['incorrect_answers']
    return q, ans, wrong_ans

score = 0
q_n = 0

while True:
    print("\nMenu:")
    print("1. Get next question")
    print("2. Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
        question, correct_answer, incorrect_answers = get_q()
        print(f"Question: {question}")
        n = random.randint(0, 4)
        incorrect_answers.insert(n, correct_answer)
        print(f"Options: {incorrect_answers}")
        user_answer = input("Enter your answer (1/2/3/4): ")
        if int(user_answer) - 1 == n:
            print("Correct!")
            score += 1
        elif user_answer not in ["1", "2", "3", "4"]:
            print(f"Invalid choice. The correct answer is: Option {n} : {correct_answer}")
        else:
            print(f"Wrong! The correct answer is: Option {n} : {correct_answer}")
        q_n += 1


    elif choice == "2":
        print("Exiting the quiz. Goodbye!")
        print(f"Your score is: {round(score/q_n * 100,2)}%")
        break
    else:
        print("Invalid choice. Please try again.")