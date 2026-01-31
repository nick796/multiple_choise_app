import json
import random
from question import Question

class Quiz:
    def __init__(self, filename):
        with open(filename) as f:
            self.questions = json.load(f)

        self.score = 0
        self.current_index = 0
        self.selected_questions = []

        self.wrong_answers = {}
    def start(self, difficulty, count):
        filtered = [q for q in self.questions if q["difficulty"] == difficulty]
        self.selected_questions = random.sample(filtered, count)
        self.current_index = 0
        self.score = 0

    def get_current_question(self):
        q = self.selected_questions[self.current_index]
        # Take a dictionary q and pass its keys & values as named arguments to Question.
        return Question(**q)

    def check_answer(self, answer):
        correct = self.get_current_question().answer == answer
        if correct:
            self.score += 1
        else:
            self.wrong_answers[self.get_current_question().id] = (
                self.get_current_question().id,
                self.get_current_question().question_text ,
                self.get_current_question().answer,
                answer)
        self.current_index += 1
        return correct
    def is_finished(self):
        return self.current_index >= len(self.selected_questions)