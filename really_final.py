#IMPORTS AND DOWNLOADS
import streamlit as st
import requests
import re
import nltk
from nltk import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')
import io
from io import StringIO
from nltk.corpus import stopwords 
from string import punctuation
from googletrans import Translator

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
        clean_text = str(clean_text)
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
    clean_text = str(clean_text)
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
st.write(tokens)
st.write(type(tokens))
#token_list = [ token for token in tokens if token not in unwanted_words_list_upper]
#st.write(token_list)

no_double = set(token_list)
#st.write(no_double)

no_double_list = [word for word in no_double]
#st.write(no_double_list)

final_list = [word for word in no_double_list if len(word) >= 3]
st.write(final_list)

# Words translation
#dest = st.text_input('Please choose a language for translation: (for example en, sk, it, de, ur...) ')
# translator = Translator()
# translation = []
# for word in final_list[0]:
#     translword = translator.translate(word, dest='sk')
#     translation.append(translword.text)
# st.write(translation)


#lemmatization
lemmatizer = WordNetLemmatizer()
lemma = []
for token in final_list:
    lem = lemmatizer.lemmatize(token)
    lemma.append(lem)
#st.write(lemma)



