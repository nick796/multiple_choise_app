import json
import random
from question import Question
from Gui import GUI
from quiz import Quiz

# my_quiz = Quiz("questions.json")
# my_quiz.start("easy",2)

# with open("questions.json", "r") as f:
#     questions = json.load(f)

# random_question = random.choice(questions)
# new_question = Question(random_question["id"],random_question["question"],random_question["choices"],random_question["answer"],random_question["difficulty"])
# print(new_question.id,new_question.answer)

# mygui = GUI()
# mygui.text_widget.insert("1.0",new_question.question_text)
# for i,choice in enumerate(new_question.choices):
#     mygui.buttons[i].config(text=choice)
# mygui.mainloop()

def main():
    quiz = Quiz("questions.json")
    app = GUI(quiz)
    app.mainloop()

if __name__ == "__main__":
    main()
