import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import comments
import sentiment_analysis
import time

def main():
    #Function to handle closing the application when clicking the X.
    def on_closing():
        root.destroy()
        root.quit()

    #Function to handle clicking event, to retrieve, analyze, and display data and findings.
    def button_clicked():
        #Clear the lists before calling the functions to prevent stacking same results on click
        process_data(5)
        if comments.comment_list:
            comments.comment_list.clear()
            comments.video_id_list.clear()

        comments.get_video_ids(comments.youtube, textbox.get('1.0', tk.END))
        process_data(25)
        comments.get_comments_per_vid_id(comments.video_id_list)
        process_data(38)
        comments.generate_csv()
        process_data(60)
        sentiment_analysis.perform_analysis() 
        process_data(80)
        categories, values = sentiment_analysis.create_average()
        process_data(90)
        create_matplotlib_widget(categories, values)
        process_data(100)
        time.sleep(0.7)
        show_data_dashboard()

    def show_data_dashboard():
        notebook.select(1)

    def process_data(number):
        # Simulate data processing (replace with your actual data processing logic)
        if progress_frame.winfo_manager() == "":
            progress_frame.pack(fill=tk.BOTH, expand=True)
        progress_var.set(number)
        root.update_idletasks()
        
        # for i in range(101):
        #     time.sleep(0.03)
        #     progress_var.set(i)  # Update the progress bar value
        #     root.update_idletasks()  # Refresh the GUI
            # Simulate data processing delay (replace with your actual processing)
            # root.after(100)

        # After processing is complete, switch to the data dashboard tab
        # show_data_dashboard()
    #Function to create the matplotlib widget dynamically after the button has been pressed.
    def create_matplotlib_widget(cat, val):    
        
        for child in display_frame.winfo_children():
            child.destroy()
        #Bar chart of averages.
        # fig, ax = plt.subplots(figsize=(6, 4), sharex=True, sharey=True, dpi=100)
        # ax.bar(cat, val)
        # ax.set_title('Sentiment Percentage Averages')
        # ax.set_xlabel('Sentiment')
        # ax.set_ylabel('Percentage')

        # Pie Chart of averages
        colors = ['#ff0000', '#ffa500', '#008000']
        fig = plt.figure(figsize=(8,8))
        ax = fig.add_subplot(111)
        ax.pie(val, labels=cat, autopct='%1.1f%%', shadow=False, startangle=140, colors=colors)

        canvas = FigureCanvasTkAgg(fig, display_frame)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    #Build the structure of the GUI
    root = tk.Tk()
    root.geometry('600x600')
    root.title('Sentiment Analysis')

    #Create a notebook (tabs)
    notebook = ttk.Notebook(root)
    notebook.pack(fill=tk.BOTH, expand=True)

    tab1 = ttk.Frame(notebook)
    notebook.add(tab1, text="Input Form")

    label = tk.Label(tab1, text="Sentiment Analysis", font=('Arial', 18))
    label2 = tk.Label(tab1, text="Type your desired topic in the text box", font=('Arial', 13))
    label.pack(padx=10, pady=10)
    label2.pack(padx=10, pady=0)

    textbox = tk.Text(tab1, height=1, width=30, font=('Arial', 16))
    textbox.pack(padx=60, pady=10)

    button = tk.Button(tab1, text="Go", font=('Arial', 18), command=button_clicked)
    button.pack(padx=10, pady=10)

    progress_frame = tk.Frame(tab1)
    progress_frame.pack_forget()

    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(progress_frame, variable=progress_var, mode="determinate")
    progress_bar.pack(pady=10)


    tab2 = ttk.Frame(notebook)
    notebook.add(tab2,text="Display Dashboard")

      #Frame for our matplotlib widget
    display_frame = tk.Frame(tab2)
    display_frame.pack(fill=tk.BOTH, expand=True)
    
    # label = tk.Label(root, text="Sentiment Analysis", font=('Arial', 18))
    # label2 = tk.Label(root, text="Type your desired topic in the text box", font=('Arial', 13))
    # label.pack(padx=10, pady=10)
    # label2.pack(padx=10, pady=0)

    # textbox = tk.Text(root, height=1, width=30, font=('Arial', 16))
    # textbox.pack(padx=60, pady=10)

    # #Run our data retrieval, cleaning, analysis when the button is clicked. 
    # button = tk.Button(root, text="Go", font=('Arial', 18), command=button_clicked)
    # button.pack(padx=10, pady=10)

    # #Frame for our matplotlib widget
    # frame = tk.Frame(root)
    # frame.pack(fill=tk.BOTH, expand=True)

    #Exit and init handling
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()


