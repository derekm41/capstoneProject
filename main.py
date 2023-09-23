import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import comments
import sentiment_analysis

def main():
    #Function to handle closing the application when clicking the X.
    def on_closing():
        root.destroy()
        root.quit()

    #Function to handle clicking event, to retrieve, analyze, and display data and findings.
    def button_clicked():
        #Clear the lists before calling the functions to prevent stacking same results on click
        if comments.comment_list:
            comments.comment_list.clear()
            comments.video_id_list.clear()

        comments.get_video_ids(comments.youtube, textbox.get('1.0', tk.END))
        comments.get_comments_per_vid_id(comments.video_id_list)
        comments.generate_csv()
        sentiment_analysis.perform_analysis() 
        categories, values = sentiment_analysis.create_average()
        create_matplotlib_widget(categories, values)

    
    #Function to create the matplotlib widget dynamically after the button has been pressed.
    def create_matplotlib_widget(cat, val):    
        
        for child in frame.winfo_children():
            child.destroy()

        fig, ax = plt.subplots(figsize=(6, 4), sharex=True, sharey=True, dpi=100)
        ax.bar(cat, val)
        ax.set_title('Sentiment Percentage Averages')
        ax.set_xlabel('Sentiment')
        ax.set_ylabel('Percentage')
        

        canvas = FigureCanvasTkAgg(fig, frame)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    #Build the structure of the GUI
    root = tk.Tk()
    root.geometry('600x600')
    root.title('Sentiment Analysis')

    label = tk.Label(root, text="Sentiment Analysis", font=('Arial', 18))
    label2 = tk.Label(root, text="Type your desired topic in the text box", font=('Arial', 13))
    label.pack(padx=10, pady=10)
    label2.pack(padx=10, pady=0)

    textbox = tk.Text(root, height=1, width=30, font=('Arial', 16))
    textbox.pack(padx=60, pady=10)

    #Run our data retrieval, cleaning, analysis when the button is clicked. 
    button = tk.Button(root, text="Go", font=('Arial', 18), command=button_clicked)
    button.pack(padx=10, pady=10)

    #Frame for our matplotlib widget
    frame = tk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True)

    #Exit and init handling
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()


