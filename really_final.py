#IMPORTS AND DOWNLOADS
import streamlit as st
import requests
import re
import nltk
from nltk import word_tokenize, sent_tokenize
nltk.download('punkt')
nltk.download('stopwords')
import io
from io import StringIO
from nltk.corpus import stopwords 
from string import punctuation

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
        start_ = re.search(r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK.*", text).span()[1]
        end_ = re.search(r"\*\*\* END OF THE PROJECT GUTENBERG EBOOK", text).span()[0]
        text = text[start_:end_]
        clean_text=re.sub("([^A-Za-z])"," ",text)
        #st.write(clean_text)
        st.subheader("Here is your text: ")
        with st.expander("See the full text: "):
            st.write(text)
        
elif option == 'url':
    url_input = st.text_input("Please insert an url")
    response = requests.get(url_input)
    response.encoding = "utf-8"
    text = response.text
    start_ = re.search(r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK.*", text).span()[1]
    end_ = re.search(r"\*\*\* END OF THE PROJECT GUTENBERG EBOOK", text).span()[0]
    text = text[start_:end_]
    clean_text=re.sub("([^A-Za-z])"," ",text)
    #st.write(clean_text)       
    st.subheader("Here is your text: ")
    with st.expander("See the full text: "):
        st.write(text)
    
# PROCESSING
# define punctuation
# puncts = punctuation
# puncts_list = [ s for s in puncts ]
#st.write( puncts_list )


#define stopwords
unwanted_words_list = stopwords.words('english')
#st.write( unwanted_words )

#update unwanted_words_list
#unwanted_words_list.extend(puncts_list)
#st.write(unwanted_words_list)






