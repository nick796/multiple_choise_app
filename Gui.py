import tkinter as tk
from tkinter import Tk
from quiz import Quiz

class GUI(tk.Tk):
    def __init__(self,quiz):
        super().__init__()
        self.title("My App")
        self.geometry("700x400")
        self.buttons =[]

        self.my_quiz = quiz
        
        self.create_start_screen()
    def create_start_screen(self):
        self.start_frame = tk.Frame(self)
        self.start_frame.pack(fill="both", expand=True)

        self.difficulty_var = tk.StringVar(value="easy")
        self.count_var = tk.IntVar(value=1)

        tk.Label(self.start_frame, text="Difficulty",font=("Arial",14)).pack()
        for d in ("easy", "medium", "hard"):
            tk.Radiobutton(
                self.start_frame,
                text=d.capitalize(),
                value=d,
                variable=self.difficulty_var,font=("Arial",14)
            ).pack()

        tk.Label(self.start_frame, text="Number of questions",font=("Arial",14)).pack()
        self.my_spinbox = tk.Spinbox(
            self.start_frame,
            from_=1,
            to=20,
            textvariable=self.count_var,font=("Arial",14)
        )
        self.my_spinbox.pack()

        self.start_button = tk.Button(
            self.start_frame,
            text="Start Quiz",
            command=self.start_quiz,font=("Arial",14)
        )
        self.start_button.pack(pady=20)
  
    def start_quiz(self):
        difficulty = self.difficulty_var.get()
        count = self.count_var.get()
        self.total_questions = count
        self.my_quiz.start(difficulty, count)  # logic

        self.start_frame.destroy()           # UI
        self.create_quiz_screen()            # UI
        self.show_question()                 # UI

    def create_quiz_screen(self):
        
        self.create_frames()
        self.create_text_widget()
        self.create_buttons()
        
    def create_frames(self):
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill="both",expand=True)
        
        self.text_frame = tk.Frame(self.main_frame)
        self.text_frame.pack()
        
        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.pack()
        for i in range(2):
            self.button_frame.columnconfigure(i, weight=1)
            self.button_frame.rowconfigure(i, weight=1)
            
    def create_text_widget(self):
        self.text_widget = tk.Text(self.text_frame, width=50, height=5,font=("Arial",14))
        self.text_widget.pack()
    
    def create_buttons(self):
        
        for r in range(2):
            for c in range(2):
                btn = tk.Button(
                    self.button_frame,
                    text="Click me",
                    font=("Arial", 15)
                )
                btn.grid(row=r, column=c, padx=40, pady=20, sticky="nsew")
                self.buttons.append(btn)
    
     # ---------- QUIZ FLOW ----------

    def show_question(self):
        q = self.my_quiz.get_current_question()

        self.text_widget.config(state="normal")
        self.text_widget.delete("1.0", "end")
        self.text_widget.insert("1.0", q.question_text, "center")
        self.text_widget.config(state="disabled")

        for btn, choice in zip(self.buttons, q.choices):
            btn.config(
                text=choice,
                command=lambda c=choice: self.on_answer(c)
            )

    def on_answer(self, choice):
        self.my_quiz.check_answer(choice)

        if self.my_quiz.is_finished():
            self.show_results()
        else:
            self.show_question()

    # ---------- RESULTS ----------

    def show_results(self):
        self.main_frame.destroy()

        result_frame = tk.Frame(self)
        result_frame.pack(fill="both", expand=True)

        tk.Label(
            result_frame,
            text="Quiz Finished!",
            font=("Arial", 20)
        ).pack(pady=20)

        tk.Label(
            result_frame,
            text=f"Score: {self.my_quiz.score}/{self.total_questions}",
            font=("Arial", 16)
        ).pack(pady=10)

        tk.Button(
            result_frame,
            text="Restart",
            font=("Arial", 14),
            command=lambda: self.restart(result_frame)
        ).pack(pady=20)
        
        self.show_mistakes = tk.Button(
            result_frame,
            text="More info",
            font=("Arial", 14),
            command= self.more_info
        )
        self.show_mistakes.pack()
        # Show where i did the mistake but on the terminal
        for i in self.my_quiz.wrong_answers:
            print(self.my_quiz.wrong_answers[i])
    def more_info(self):
        info_window = tk.Toplevel(self)
        info_window.title("Info Window")
        info_window.geometry("700x400")
        
        info_container = tk.Frame(info_window)
        info_container.pack(fill="both", expand=True)
        
        info_text = tk.Text(info_container,width=50, height=10,font=("Arial",14))
        info_text.pack(side="left",fill="both",expand=True,padx=10,pady=10)
        
        scrollbar = tk.Scrollbar(info_container, command=info_text.yview,width=30)
        scrollbar.pack(side="right", fill="y")
        info_text.config(yscrollcommand=scrollbar.set)

        info_text.config(state="normal")
        info_text.delete("1.0","end")
        for wrong_answer in self.my_quiz.wrong_answers:
            info_text.insert("end",
                             f"Question {self.my_quiz.wrong_answers[wrong_answer][0]}: {self.my_quiz.wrong_answers[wrong_answer][1]}\n"
                             f"[Correct Answer]: {self.my_quiz.wrong_answers[wrong_answer][2]}\n"
                             f"[Your Answer]: {self.my_quiz.wrong_answers[wrong_answer][3]}\n\n")
        info_text.config(state="disabled")
       
        close_button = tk.Button(
            info_window,
            text="Close",
            font=("Arial", 14),
            command= info_window.destroy
            )
        close_button.pack(pady=10)
    
    def restart(self, frame):
        frame.destroy()
        self.buttons = []
        self.my_quiz.wrong_answers = {}
        self.create_start_screen()
   