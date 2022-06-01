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
user_name = st.text_input("Hello! What is you name?")
st.write("Welcome!", user_name, "ldjhakjshkjahfkjshfkjshfjs")


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
        clean_text=re.sub("([^A-Za-z])"," ",text).upper()
        #st.write(clean_text)
        st.subheader("Here is your text: ")
        with st.expander("Please click here to see the full text"):
            st.write(text)
        
elif option == 'url':
    url_input = st.text_input("Please insert an url")
    response = requests.get(url_input)
    response.encoding = "utf-8"
    text = response.text
    start_ = re.search(r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK.*", text).span()[1]
    end_ = re.search(r"\*\*\* END OF THE PROJECT GUTENBERG EBOOK", text).span()[0]
    text = text[start_:end_]
    clean_text=re.sub("([^A-Za-z])"," ",text).upper()
    #st.write(clean_text)       
    st.subheader("Here is your text: ")
    with st.expander("Please click here to see the full text"):
        st.write(text)
    
# PROCESSING
# define punctuation
# puncts = punctuation
# puncts_list = [ s for s in puncts ]
#st.write( puncts_list )


#define stopwords
unwanted_words_list = stopwords.words('english')
unwanted_words_list_upper = [word.upper() for word in unwanted_words_list]
#st.write( unwanted_words_list_upper)


#update unwanted_words_list
#unwanted_words_list.extend(puncts_list)
#st.write(unwanted_words_list)

#tokenize
tokens = word_tokenize(clean_text)
token_list = [ token for token in tokens if token not in unwanted_words_list_upper]
st.write(token_list)







