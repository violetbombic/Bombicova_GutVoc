import streamlit as st
import PyPDF2
from PyPDF2 import PdfFileReader
import nltk
from nltk import word_tokenize, sent_tokenize
nltk.download('punkt')
import io
from io import StringIO


st.title("Project_Name")
st.write("Please insert a relative path of the PDF file. Note that the PDF file has to be saved in and copied from the same folder in GitHub, where  the .py file is. Try for example: CORE_INTENTIONAL_FEATURES_IN_THE_SYNTACT.pdf")

relative_path = st.file_uploader("Please choose a file")

if relative_path is not None:  

    # creating a pdf reader object 
    pdfReader = PdfFileReader(relative_path) 

    # printing number of pages in pdf file 
    num_pages = pdfReader.numPages

    page_content=""
    number_of_pages = pdfReader.getNumPages()

    for page_number in range(number_of_pages):
        page = pdfReader.getPage(page_number)
        page_content += page.extract_text()
    st.write(page_content)


