import tkinter as tk


root = tk.Tk()

root.geometry('500x500')
root.title("Sentiment Analysis")

#label
label = tk.Label(root, text='Hello World!', font=('Arial', 18))
label.pack(padx=20, pady=20)

textbox = tk.Text(root, height=1, font=('Arial', 16))
textbox.pack(padx=10, pady=10)


buttonframe = tk.Frame(root)
buttonframe.columnconfigure(0, weight=1)
buttonframe.columnconfigure(1, weight=1)
buttonframe.columnconfigure(2, weight=1)

btn1 = tk.Button(buttonframe, text='1', font=('Arial', 18))
btn1.grid(row=0, column=0, sticky=tk.W+tk.E)

btn2 = tk.Button(buttonframe, text='2', font=('Arial', 18))
btn2.grid(row=0, column=1, sticky=tk.W+tk.E)

btn3 = tk.Button(buttonframe, text='3', font=('Arial', 18))
btn3.grid(row=0, column=2, sticky=tk.W+tk.E)

buttonframe.pack(fill=tk.X)

anotherbtn = tk.Button(root, text='Test')
anotherbtn.place(x=200, y=200, height=100, width=100)



root.mainloop()