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
import pdfkit as pdf
import sqlite3
import numpy as np

#Select PDF files for upload (max 200MB)
uploaded_files = st.file_uploader("Choose a file", type = "pdf", accept_multiple_files = True)
for uploaded_file in uploaded_files:
    bytes_data = uploaded_file.read()
    st.write("filename:", uploaded_file.name)
    
    parsed_pdf = parser.from_file(pdf)
    st.write(parsed_pdf)
    
    #Split PDF into list
    content = parsed_pdf['content']
    pdf_list = content.split('\n')
    pdf_list = list(filter(lambda a: a != '', pdf_list))

    st.write(pdf_list)

     #Search for keyword to select values from
    r = re.compile("keyword")
    newlist = list(filter(r.match, pdf_list))

    st.write(newlist)

    #Creating array for target_data
    target_data = []
    for i in newlist:
        tmp_list = i.split(' ')
        target_data.append(tmp_list)

    #Manipulating data type
    df = pd.DataFrame(columns = ["Put Columns Here"])
    for i in target_data:
        df = df.append({"Put Rows Here"})

    st.write(df.dtypes.astype(str))

    df["Row"] = df["Row"].convert_dtypes()
    df["Column"]=pd.to_numeric(df["Column"])
    st.write(df.dtypes.astype(str))

    st.dataframe(df)

#Download as PDF
@st.cache
def return_pdfdata(df):
    return df.to_html('f.html')
    final='z.pdf'
    pdf.from_file('f.html', final)

#Download Button
st.download_button(label="Final PDF name",
                data=PDFbyte,
                file_name="test.pdf",
                mime='application/octet-stream')
