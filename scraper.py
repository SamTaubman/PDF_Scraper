
'''
Streamlit web application for loading SoloVPE PDF files to extract
control and sample concentrations as a dataframe. The extracted 
dataframe is then downloaded as a CSV for easy LIMS reporting.
'''

#import libraries
import streamlit as st
from tika import parser
import pprint
from collections import defaultdict
import re
import pandas as pd

#key functions
def input_file_processing(file_name):
    ''' Function that cleans PDF by removing empty lines, page breaks, etc. '''
    parsedPDF = parser.from_file(file_name)
    content = parsedPDF['content']
    contentlist = content.split('\n')
    contentlist = list(filter(lambda a: a != '', contentlist)) #Remove empty lines
    return contentlist


#file upload
uploaded_files = st.file_uploader("Select SoloVPE PDFs for upload", type = "pdf", accept_multiple_files = True)
for file in uploaded_files:
    pdf = file
    st.write(pdf)
    st.write('View Raw Parsed PDF')
    parsed_pdf = parser.from_file(pdf)
    st.write(parsed_pdf)
    
    content = parsed_pdf['content']
    pdf_list = content.split('\n')
    pdf_list = list(filter(lambda a: a != '', pdf_list)) #Remove empty lines
    
    st.write("Inspect PDF list with page breaks and white spaces removed")
    st.write(pdf_list)
    
    #bytes_data = file.read()
    #st.write(bytes_data)
    
    #pdf_list = input_file_processing(pdf)
    
    #search for PLXQ expression to collect all concentrations
    st.write("Execute regexp to search for .*[1-2] PLXQ to locate control/sample concentrations")
    r = re.compile(".*[1-2] PLXQ")
    newlist = list(filter(r.match, pdf_list))
    st.write("Show all extracted concentrations before cleaning")
    st.write(newlist)
    
    #split list elements by space
    target_data = []
    for i in newlist:
        tmp_list = i.split(' ')
        target_data.append(tmp_list)
    
    #join control name into one element
    for i in target_data[0:2]:
        i[1:5] = ['-'.join(i[1:5])]
    
    #build dataframe
    extract_df = pd.DataFrame(columns = ["Sample Name", "Concentration"])
    for i in target_data:
        extract_df = extract_df.append({"Sample Name" : i[1], "Concentration" : i[2]}, ignore_index = True)
    
    #return data types
    st.write("Double check data types and update")
    st.write("Original data types from PDF")
    st.write(extract_df.dtypes.astype(str))
    
    #change data types
    extract_df["Sample Name"] = extract_df["Sample Name"].convert_dtypes()
    extract_df["Concentration"]=pd.to_numeric(extract_df["Concentration"])
    st.write("Update data types to string and float")
    st.write(extract_df.dtypes.astype(str))
    
    #st.write(extract_df.dtypes)
    st.write("Sample Name and Concentration Table")
    st.dataframe(extract_df)
    
    #download as csv
@st.cache
def convert_df(df):
    return df.to_csv().encode('utf-8')

csv = convert_df(extract_df)

st.download_button(
    label = "Download SoloVPE Extract as CSV",
    data = csv,
    file_name = "SoloVPE-Extract-Example.csv",
    mime = "text/csv"
)
