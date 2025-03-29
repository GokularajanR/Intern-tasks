with open("notes.txt", "w") as file:
    file.write("Sentence A.\n")
    file.write("Sentence B.\n")
    file.write("Sentence C.\n")

with open("notes.txt", "r") as file:
    content = file.read()
    print("File Content:\n")
    print(content)