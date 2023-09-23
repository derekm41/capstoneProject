import tkinter as tk
from tkinter import messagebox
import comments
#testing partial
from functools import partial

class myGUI:


    def __init__(self):

        self.root = tk.Tk()
        self.root.geometry('500x500')
        self.root.title('Sentiment Analysis')

        self.label = tk.Label(self.root, text="Sentiment Analysis", font=('Arial', 18))
        self.label2 = tk.Label(self.root, text="Type your desired topic in the text box", font=('Arial', 13))
        self.label.pack(padx=10, pady=10)
        self.label2.pack(padx=10, pady=0)

        self.textbox = tk.Text(self.root, height=1, width=30, font=('Arial', 16))
        self.textbox.pack(padx=60, pady=10)

        # self.check_state = tk.IntVar()

        # self.check = tk.Checkbutton(self.root, text='Go', font=('Arial', 16), variable=self.check_state)
        # self.check.pack(padx=10, pady=10)

        # self.button = tk.Button(self.root, text="Show Message", font=('Arial', 18), command=lambda: comments.test_function(self.textbox.get('1.0', tk.END)))
        # self.button.pack(padx=10, pady=10)

        #Run our data retrieval, cleaning, analysis when the button is clicked. 
        self.button = tk.Button(self.root, text="Go", font=('Arial', 18), command=self.button_clicked)
                                

                                # command=lambda:comments.get_video_ids(comments.youtube, self.textbox.get('1.0', tk.END)))
        self.button.pack(padx=10, pady=10)

        self.root.mainloop()

    # def show_message(self):
    #     print('Hello World')
    #     print(self.check_state.get())
    #     if self.check_state.get() == 0:
    #         print(self.textbox.get('1.0', tk.END))
    #     else:
    #         messagebox.showinfo(title='Message', message=self.textbox.get('1.0', tk.END))

    def button_clicked(self):
        #Clear the lists before calling the functions to prevent stacking same results on click
        if comments.comment_list:
            comments.comment_list.clear()
            comments.video_id_list.clear()

        comments.get_video_ids(comments.youtube, self.textbox.get('1.0', tk.END))
        comments.get_comments_per_vid_id(comments.video_id_list)
        # comments.check_comment_csv()
        comments.generate_csv()


myGUI()

    


