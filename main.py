import json
import random
from question import Question
from Gui import GUI
from quiz import Quiz

def main():
    quiz = Quiz("questions.json")
    app = GUI(quiz)
    app.mainloop()

if __name__ == "__main__":
    main()
