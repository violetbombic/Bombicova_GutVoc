#IMPORTS AND DOWNLOADS
import streamlit as st
import json, requests
import re
#nltk
import nltk
from nltk.corpus import stopwords 
from nltk import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')
#io
import io
from io import StringIO
#googletrans
from googletrans import Translator
#pandas
import pandas as pd

#TITLE AND DESCRIPTION
st.title("GutVoc")
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
        clean_text = str(clean_text[:500])
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
    
#PROCESSES
#define stopwords
unwanted_words_list = stopwords.words('english')
#st.write( unwanted_words_list)

#tokenize
tok = word_tokenize(clean_text)
#st.write(tok)
tokens = [ token for token in tok if token not in unwanted_words_list]
#st.write(tokens)

no_double = set(tokens)
no_double_list = list(no_double)
#st.write(no_double)

final_list = [word for word in no_double_list if len(word) >= 3]
st.write(final_list)

#lemmatization
lemmatizer = WordNetLemmatizer()
lemma = []
for token in final_list:
    lem = lemmatizer.lemmatize(token)
    lemma.append(lem)
st.write(lemma)


# #Words translation
# #dest = st.text_input('Please choose a language for translation: (for example en, sk, it, de, ur...) ')
# translator = Translator()
# translation = []
# for token in final_list:
#     translword = translator.translate(token, dest='sk')
#     translation.append(translword.text)
# st.write(translation)


#pronunciation
pron = []
for token in final_list:
    url = 'https://api.datamuse.com/words?sp=' + token + '&qe=sp&md=r&ipa=1'
    response = requests.get(url)
    dataFromDatamuse = json.loads(response.text)
    datamuse_data = dataFromDatamuse[0]['tags'][-1]
    pronunciation = re.sub("ipa_pron:"," ",datamuse_data)
    pron.append(pronunciation) 
st.write(pron)

#pos-tag
pos_tags = []
for token in final_list:
    url= 'https://api.datamuse.com/words?sp=' + token + '&qe=sp&md=p'
    response = requests.get(url)
    dataFromDatamuse = json.loads(response.text)
    pronunciation = dataFromDatamuse[0]['tags'][-1]
    pos_tags.append(pronunciation)
st.write(pos_tags)

df = pd.DataFrame({"Word" : final_list, "Lema": lemma, "IPA_pron": pron, "Pos-tag": pos_tags})
df1 = df.sort_values("Word")
#st.write(df)

#OUTPUT
st.subheader("Now you can dowload your Vocabulary!")

@st.cache
def convert_df(df1):
   return df.to_csv().encode('utf-8')

csv = convert_df(df)

st.download_button('Click here to dowload it',csv, "your_vocabulary.csv","text/csv",key='download-csv')

with st.spinner('Wait for it...'):
    time.sleep(5)
st.success('Done!')

