import streamlit as st
from booking_script import main
import sys

class StreamToLogger:
    def __init__(self, text_elem):
        self.text_elem = text_elem

    def write(self, text):
        self.text_elem.text(text)


st.title("Automatic Gym Booking")

# Define input fields
name = st.text_input("Name")
email = st.text_input("Email")
uid = st.text_input("UID")

# Create dropdown menus for date and time
time_options = ['1700-1830', '1845-2015', '2030-2200']
date_options = ['Today','Tomorrow','Day After Tomorrow','2 Days After Tomorrow']

date = st.selectbox("Date", date_options)
time = st.selectbox("Time", time_options)

submit_button = st.button("Submit")


# Create a submit button
if submit_button:
    output_text = st.text("Booking for you now...")
    main(name,email,uid,date,time,output_text)



