#IMPORTS AND DOWNLOADS
import streamlit as st
import PyPDF2
from PyPDF2 import PdfFileReader
import nltk
from nltk import word_tokenize, sent_tokenize
nltk.download('punkt')
import io
from io import StringIO

#TITLE AND DESCRIPTION
st.title("Project_Name")
st.write("Please insert a relative path of the PDF file. Note that the PDF file has to be saved in and copied from the same folder in GitHub, where  the .py file is. Try for example: CORE_INTENTIONAL_FEATURES_IN_THE_SYNTACT.pdf")


#INPUT
option = st.selectbox("What type of file you want to upload?", ('Text file', 'url'))
if option == 'Text file':
    uploaded_file = st.file_uploader("Please choose a file")
    if uploaded_file is not None:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        string_data = stringio.read()
        text = string_data
        st.subheader("Here is your text: ")
        st.write(text)

    

elif option == 'url':
    st.text_input("Please insert an url")

# if updated_file is not None:  
#     pdfReader = PdfFileReader(uploaded_file) 
#     num_pages = pdfReader.numPages

#     page_content=""
#     number_of_pages = pdfReader.getNumPages()
#     for page_number in range(number_of_pages):
#         page = pdfReader.getPage(page_number)
#         page_content += page.extract_text()
#     st.write(page_content)


