with open("notes.txt", "a") as file:
    file.write("Sentence D.\n")
    file.write("Sentence E.\n")
    file.write("Sentence F.\n")

with open("notes.txt", "r") as file:
    content = file.read()
    print("File Content:\n")
    print(content)