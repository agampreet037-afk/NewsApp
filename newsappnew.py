import requests
import tkinter as tk
from PIL import Image,ImageTk
import webbrowser
import smtplib
from email.mime.text import MIMEText
from email.message import EmailMessage



API_KEY = "b95386fb765044798d036eddbff1b314"


root = tk.Tk()
root.title("News App")
root.geometry("600x750")
root.configure(bg="#0F172A")

current_articles = []
current_page = 0

ARTICLES_PER_PAGE = 10

active_category = None
category_labels = {}
underline_frames = {}


title_label = tk.Label(root,text="Welcome to MyNews App",font=("Calibri", 21,"bold"), bg = "#0F172A",
    fg="white")
title_label.pack()

topic_frame = tk.Frame(root,bg="#0F172A")
topic_frame.pack(pady=10)

topic_label = tk.Label(topic_frame,text="Search for any topic:",font=("Calibri",11,"bold"),fg="white",bg="#0F172A")
topic_label.grid(row=0,column=0,sticky="w")

topic_var = tk.StringVar()

topic_entry = tk.Entry(topic_frame,width=55,textvariable=topic_var)
topic_entry.grid(row=1,column=0,padx=5)

scrollbar_y = tk.Scrollbar(root)
scrollbar_y.pack(side="right", fill="y")

category_frame = tk.Frame(root,bg=root["bg"])
category_frame.pack(pady=10)



categories = [
    "Business",
    "Entertainment",
    "Health",
    "Science",
    "Sports",
    "Technology"
]

def make_click_function(category):

    def on_click(event):
        select_category(category)

    return on_click

for category in categories:
    container = tk.Frame(category_frame,bg=root["bg"])
    container.pack(side="left",padx=8)

    label = tk.Label(container,text=category,font=("Calibri",11,"bold"),cursor="hand2",fg="white",bg=root["bg"])
    label.pack()

    underline = tk.Frame(container,height=2,bg=root["bg"])
    underline.pack(fill="x")

    category_labels[category] = label
    underline_frames[category] = underline


    label.bind(
    "<Button-1>",
    make_click_function(category)
)


results_text = tk.Text(root, width=70, height=20,wrap="word",font="Arial",bg="#0F172A",fg="white",yscrollcommand=scrollbar_y.set)
results_text.pack(fill="both",expand=True,padx=10,pady=10)
results_text.config(state="disabled")

scrollbar_y.config(command=results_text.yview)

def update_buttons():
    max_page = (len(current_articles) - 1) // ARTICLES_PER_PAGE

    if current_page == 0:
        prev_btn.config(state = "disabled")

    else:
        prev_btn.config(state = "normal")

    if current_page >= max_page:
        next_btn.config(state = "disabled")
    else:
        next_btn.config(state = "normal")

    page_label.config(text=f"Page {current_page + 1} of {max_page + 1}")            

def display_page():
    results_text.config(state="normal")
    results_text.delete("1.0",tk.END)

    start = current_page * ARTICLES_PER_PAGE
    end = start + ARTICLES_PER_PAGE
    global article_text
    article_text = []
    for i,article in enumerate(current_articles[start:end],start=1):
       article_text.append(
        f"{i}. {article['title']}\n\n"
        f"Source: {article['source']['name']}\n\n"
        f"Click to view Full Article: {article['url']}\n\n"
        f"{'-' * 50}\n\n")
    results_text.insert(tk.END,"".join(article_text))
    results_text.config(state="disabled")

    update_buttons()

def previous_page():
    global current_page

    if current_page > 0:
        current_page = current_page - 1
        display_page()

def next_page():
    global current_page

    max_page = (len(current_articles) - 1) // ARTICLES_PER_PAGE   #Find the index of the page containing the last article

    if current_page < max_page:
        current_page = current_page + 1
        display_page()      


def search_category(category):
    url = (
        "https://newsapi.org/v2/top-headlines?"
        f"country=us&category={category.lower()}"
        f"&apiKey={API_KEY}"
    )

    response = requests.get(url)
    data = response.json()

    global current_articles, current_page

    current_articles = data["articles"]
    current_page = 0

    display_page()         

def select_category(category):
    global active_category

    if active_category is not None:
        underline_frames[active_category].config(
            bg=root["bg"]
        )

    active_category = category

    underline_frames[category].config(
        bg="white"
    )

    search_category(category)

def search():
    url = (
    f"https://newsapi.org/v2/everything?"
    f"q={topic_var.get().strip()}&sortBy=publishedAt&apiKey={API_KEY}"
)
    response = requests.get(url)
    data = response.json()
    global current_articles,current_page

    current_articles = data["articles"]
    current_page = 0

    display_page()

def send_email():
    msg = EmailMessage()
    msg["Subject"] = "Your Daily Newsletter"
    msg["From"] = "agampreet037@gmail.com"
    msg["To"] = "agampreet037@gmail.com"

    msg.set_content(f"Good Morning! Here is your daily newsletter\n{''.join(article_text)}")

    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()  # Encrypt the connection
        smtp.login("agampreet037@gmail.com", "bpie navd qsia bvzq")  # Hide password before uploading anywhere
        smtp.send_message(msg)    

def open_link(url):
    webbrowser.open(url)    
    


search_btn = tk.Button(topic_frame,text="Search",width=15,command=search)
search_btn.grid(row=1,column=1,sticky="e",padx=5)

nav_frame = tk.Frame(root,bg="#0F172A")
nav_frame.pack(pady = 5)
email_button = tk.Button(nav_frame,text="Send Email",command=send_email)
email_button.grid(row=0,column=3,padx=20)

page_label = tk.Label(nav_frame,text="",bg="#0F172A",fg="white")
page_label.grid(row=0,column=1,padx=10)


prev_btn = tk.Button(nav_frame,text="◀ Previous",command=previous_page)
prev_btn.grid(row= 0,column=0,padx=20)

next_btn = tk.Button(nav_frame,text="Next ▶",command=next_page)
next_btn.grid(row= 0,column=2,padx=20)



root.mainloop()


#Features:
# 1. More button
# 2. Enter means search
# 3. Click to open URL


# Design: 