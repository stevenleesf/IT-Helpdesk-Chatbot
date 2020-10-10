#!/usr/bin/env python
# coding: utf-8

# In[1]:


import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
from tensorflow import keras
import numpy as np
import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="feedback_db"
)
mycursor = mydb.cursor()
import tensorflow as tf

config = tf.compat.v1.ConfigProto(gpu_options = 
                         tf.compat.v1.GPUOptions(per_process_gpu_memory_fraction=0.8)
# device_count = {'GPU': 1}
)
config.gpu_options.allow_growth = True
session = tf.compat.v1.Session(config=config)
tf.compat.v1.keras.backend.set_session(session)
model = tf.keras.models.load_model('chatbot_model.h5')
import json
import random
intents = json.loads(open('intents.json', encoding='utf-8').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))


# In[4]:


from tkinter import *
from tkinter import ttk
from tkinter import messagebox


class Feedback:
    def __init__(self, mainframe):
        mainframe.title('Add Your Comment')
        mainframe.resizable(False, False)
        mainframe.configure(background='#f7f7f7')

        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f7f7f7')
        self.style.configure('TButton', background='#e1d8b9')
        self.style.configure('TLabel', background='#f7f7f7', font=('Arial', 12))
        self.style.configure('Header.TLabel', font=('Arial', 18, 'bold'))

        self.header_frame = ttk.Frame(mainframe)
        self.header_frame.pack()

       
        ttk.Label(self.header_frame, text='Comment App', style='Header.TLabel').grid(row=0, column=1)
        ttk.Label(self.header_frame, wraplength=300,
                      text=(
                          'Add your name, email, and comment, then click submit to add your comment.  Click clear if you make a mistake.')).grid(
                row=1, column=1)

        self.content_in_frame = ttk.Frame(mainframe)
        self.content_in_frame.pack()

        ttk.Label(self.content_in_frame, text='Name:').grid(row=0, column=0, padx=5, sticky='sw')
        ttk.Label(self.content_in_frame, text='Email:').grid(row=0, column=1, padx=5, sticky='sw')
        ttk.Label(self.content_in_frame, text='Comments:').grid(row=2, column=0, padx=5, sticky='sw')

        self.comment_name = ttk.Entry(self.content_in_frame, width=24, font=('Arial', 10))
        self.comment_email = ttk.Entry(self.content_in_frame, width=24, font=('Arial', 10))
        self.comments = Text(self.content_in_frame, width=50, height=10, font=('Arial', 10))

        self.comment_name.grid(row=1, column=0, padx=5)
        self.comment_email.grid(row=1, column=1, padx=5)
        self.comments.grid(row=3, column=0, columnspan=2, padx=5)

        ttk.Button(self.content_in_frame, text='Submit',
                       command=self.submit).grid(row=4, column=0, padx=5, pady=5, sticky='e')
        ttk.Button(self.content_in_frame, text='Clear',
                       command=self.clear).grid(row=4, column=1, padx=5, pady=5, sticky='w')



    def submit(self):
            print(f'Name: {self.comment_name.get()}')
            print(f'Email: {self.comment_email.get()}')
            print(f'Comments: {self.comments.get(1.0, "end")}')
            sql = "INSERT INTO `feedback`(`name`, `email`, `info`) VALUES (%s,%s,%s)"
            val= (self.comment_name.get(), self.comment_email.get(), self.comments.get(1.0, "end"))
            mycursor.execute(sql, val)
            mydb.commit()
            self.clear()
            messagebox.showinfo(title='Comment info', message='Thanks for your comment!')
           
            

    def clear(self):
            self.comment_name.delete(0, 'end')
            self.comment_email.delete(0, 'end')
            self.comments.delete(1.0, 'end')
            
            
    


if __name__ == '__main__':
        root = Tk()
        root.geometry('500x400')
        feedback = Feedback(root)
        root.mainloop()


# In[ ]:




