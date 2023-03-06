'''
Streamlit web application that takes PDF file and breaks it down into tables based on input names then exports table as PDF file
'''

#import libraries
import streamlit as st
from tika import parser
import pprint
from collections import defaultdict
import re
import pandas as pd

#Select PDF files for upload (max 200MB)
uploaded_files = st.file_uploader("Choose a file", type = "pdf", accept_multiple_files = True)
for uploaded_file in uploaded_files:
    bytes_data = uploaded_file.read()
    st.write("filename:", uploaded_file.name)
    
    parsed_pdf = parser.from_file(pdf)
    st.write(parsed_pdf)
    
    content = parsed_pdf['content']
    pdf_list = content.split('\n')
    pdf_list = list(filter(lambda a: a != '', pdf_list))

     st.write(pdf_list)

     #Search for keyword to select values from
    r = re.compile("keyword")
    newlist = list(filter(r.match, pdf_list))