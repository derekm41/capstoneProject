import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import comments
import sentiment_analysis
import time
import numpy as np
import matplotlib.colors as mcolors

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
        process_data(60)
        sentiment_analysis.perform_analysis(comments.comment_list) 
        process_data(80)
        categories, values = sentiment_analysis.create_average()
        process_data(90)
        create_matplotlib_widget(categories, values)
        process_data(100)
        time.sleep(0.7)
        show_data_dashboard()
    
    #Function to show first tab when processing is done.
    def show_data_dashboard():
        notebook.select(1)
        root.geometry('600x600')

    #Function for dynamically showing analysis label and progress bar
    def process_data(number):
        if analysis_frame.winfo_manager() == "":
            analysis_frame.pack(fill=tk.BOTH, expand=True)
        if progress_frame.winfo_manager() == "":
            progress_frame.pack(fill=tk.BOTH, expand=True)
        progress_var.set(number)
        root.update_idletasks()
      
    #Function to create the matplotlib widget dynamically after the button has been pressed.
    def create_matplotlib_widget(cat, val):    
        #Clear frames of previous data
        for child in pie_frame.winfo_children():
            child.destroy()
        for child in histo_frame.winfo_children():
            child.destroy()
        for child in scatter_frame.winfo_children():
            child.destroy()
        #Show graph tabs
        notebook.tab(1, state='normal')
        notebook.tab(2, state='normal')
        notebook.tab(3, state='normal')

        # Pie Chart of averages
        colors = ['#ff0000', '#ffa500', '#008000']
        pie_fig = plt.figure(figsize=(4.5, 4.5))
        ax = pie_fig.add_subplot(111)
        ax.pie(val, labels=cat, autopct='%1.1f%%', shadow=False, startangle=140, colors=colors)
        ax.set_title('Sentiment Averages')

        pie_canvas = FigureCanvasTkAgg(pie_fig,  pie_frame)
        pie_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        pie_definition = """This pie chart is used to show the distribution of average scores for a given topic. We can use this chart to get a high level view of overall sentiment."""
        pie_text_widget = tk.Text(pie_def_frame, wrap='word', width=100, height=100)
        pie_text_widget.insert('1.0', pie_definition)
        pie_text_widget.pack(side="bottom")

        #Scatter plots of positive or negative comments to show the extremity of the comments.
        scatter_fig = plt.figure(figsize=(4.5, 4.5))
        scatter_ax = scatter_fig.add_subplot(111)
        
        cmap = plt.get_cmap('Reds')
        norm = mcolors.Normalize(vmin=0.0, vmax=2)
        scatter = scatter_ax.scatter(comments.likes, comments.comments, c=comments.sentiment_score, cmap=cmap, norm=norm, s=100, alpha=0.9)

        # Add labels and a colorbar
        scatter_ax.set_xlabel('Likes')
        scatter_ax.set_ylabel('Comments')
        scatter_ax.set_title('Scatter Plot of Likes vs. Comments with Sentiment Scores')

        scatter_ax.set_xlim(0, 10000)
        scatter_ax.set_ylim(0, 2000)

        cbar = plt.colorbar(scatter, ax=scatter_ax)
        cbar.set_label('Sentiment Score')
        
        scatter_canvas = FigureCanvasTkAgg(scatter_fig, scatter_frame)
        scatter_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        scatter_definition = """This scatter is used to show the relationship between numbers of comments, likes, and positive/negative sentiment distribution on videos. The Y axis represents comment count. The X axis represents like count. The intensity of the dot represents sentiment scoring. The darker the red, the more positive the sentiment."""
        scatter_text_widget = tk.Text(scatter_def_frame, wrap='word', width=100, height=100)
        scatter_text_widget.insert('1.0', scatter_definition)
        scatter_text_widget.pack(side="bottom")

        # #Histogram of negative and positive comment distribution
        num_bins = 30
        bin_edges = np.linspace(0, 1.0, num_bins + 1)
        histo_fig = plt.figure(figsize=(4.5, 4.5))
        histo_ax = histo_fig.add_subplot(111)
        histo_ax.hist(sentiment_analysis.negative_scores, bins=bin_edges, edgecolor='black')
        histo_ax.set_xlabel('Negative Sentiment Scores')
        histo_ax.set_ylabel('Frequency')
        histo_ax.set_title('Distribution of Negative Sentiment Scores')
        # histo_ax.grid(True)

        histo_canvas = FigureCanvasTkAgg(histo_fig, histo_frame)
        histo_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        histo_definition = """This Histogram show the distribution of the negative scores. A negative score of 0 represents low negative sentiment and a negative score of 1 represents a high negative sentiment. We can use this histogram to gauge the severity of the negative sentiment."""
        histo_text_widget = tk.Text(histo_def_frame, wrap='word', width=100, height=100)
        histo_text_widget.insert('1.0', histo_definition)
        histo_text_widget.pack(side="bottom")

        
    #Build the structure of the GUI
    root = tk.Tk()
    root.geometry('400x400')
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

    analysis_frame = tk.Frame(tab1)
    analysis_frame.pack_forget()

    analysis_label = tk.Label(analysis_frame, text='Performing Analysis....', font=('Arial', 16))
    analysis_label.pack(pady=10)
    

    progress_frame = tk.Frame(tab1)
    progress_frame.pack_forget()

    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(progress_frame, variable=progress_var, mode="determinate")
    progress_bar.pack(pady=10)


    tab2 = ttk.Frame(notebook)
    notebook.add(tab2, text="Average Sentiment", state='hidden')

    #Frame for our matplotlib widget
    pie_frame = tk.Frame(tab2)
    pie_frame.pack(fill=tk.BOTH, expand=True)

    pie_def_frame = tk.Frame(tab2)
    pie_def_frame.pack(fill=tk.BOTH, expand=True)

    tab3= ttk.Frame(notebook)
    notebook.add(tab3, text="Negative Distribution", state='hidden')

    histo_frame = tk.Frame(tab3)
    histo_frame.pack(fill=tk.BOTH, expand=True)

    histo_def_frame = tk.Frame(tab3)
    histo_def_frame.pack(fill=tk.BOTH, expand=True)

    tab4 = ttk.Frame(notebook)
    notebook.add(tab4, text='Comments vs Likes vs Sentiment', state='hidden')

    scatter_frame = tk.Frame(tab4)
    scatter_frame.pack(fill=tk.BOTH, expand=True)

    scatter_def_frame = tk.Frame(tab4)
    scatter_def_frame.pack(fill=tk.BOTH, expand=True)

    #Exit and init handling
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()


