import requests
import random

class Quiz:
    def __init__(self):
        self.score = 0
        self.q_n = 0
        self.__URL = "https://opentdb.com/api.php?amount=1&category=17&difficulty=hard&type=multiple" #Using opentdb API for quiz questions
        self.question = None
        self.options = None
        self.__ans = None

    
    def get_q(self):
        try:
            response = requests.get(self.__URL)
            self.question = response.json()['results'][0]['question']
            ans = response.json()['results'][0]['correct_answer']
            self.options = response.json()['results'][0]['incorrect_answers']
            n = random.randint(0, 4)
            self.options.insert(n, ans)
            self.__ans = n
            self.q_n += 1
            return True
        except Exception as e:
            print(f"Internal Error : {e}")
            return False
        

    def grade(self, n : int):
        if n - 1 == self.__ans:
            print("Correct!")
            self.score += 1
            return 1
        elif n not in [1,2,3,4]:
            print(f"Invalid choice. The correct answer is: Option {self.__ans + 1} : {self.options[self.__ans]}")
            return -1
        else:
            print(f"Wrong! The correct answer is: Option {self.__ans + 1} : {self.options[self.__ans]}")
            return 0
        
    def display(self):
        print(f"Question: {self.question}")
        print(f"Option 1: {self.options[0]}")
        print(f"Option 2: {self.options[1]}")
        print(f"Option 3: {self.options[2]}")
        print(f"Option 4: {self.options[3]}")

    def stop(self):
        print("Exiting the quiz")
        print(f"Your score is: {round(self.score/self.q_n * 100,2)}%")
        return True
    
