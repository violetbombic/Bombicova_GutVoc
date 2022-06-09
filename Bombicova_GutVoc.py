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
#image
from PIL import Image
#wordcloud
from wordcloud import WordCloud, STOPWORDS
#matplotlib
import matplotlib.pyplot as plt
#openpyxl
import openpyxl


#TITLE
st.title("GutVoc")
st.write("A project by Violeta Bombicova, for the course of Computer Programing, MS Applied Linguistics, at unibz, Brixen, Italy")

#IMAGE
img = 'https://aretepiattaforma.it/pluginfile.php/1/local_simplified_news/newscontent/255/Project%20Gutenberg.jpg'
st.image(img)

#DESCRIPTION
st.write("""You're learning English and you've decided to read books from the Gutenberg digital library. However, you don't understand some of the words and you don't have time to translate word by word. Here's a solution for you! Just a few clicks and you get your vocabulary, that you can download and print. """)

with st.expander("Instructions for use. Please click here > "):
     st.write("""
     - Go to https://gutenberg.org/, 
     - choose a book that interests you, 
     - now you have two options: in case you have dowloaded the book, upload a file; otherwise find Plain Text UTF-8 format and insert an URL, for example: https://gutenberg.org/cache/epub/68261/pg68261.txt,
     - choose the language into which you want to translate the words,
     - wait a minute :)
     - dowload the vocabulary and wordcloud. 
     """) 
ready2go = False

#INPUT
st.subheader("What type of file you want to upload?")
option = st.selectbox("Please, select an option.", ('Text file', 'url'))
if option == 'Text file':
     st.subheader("File selection")
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
          ready2go = True
            
     
elif option == 'url':
     url_input = st.text_input("Please insert an url")
     response = requests.get(url_input)
     response.encoding = "utf-8"
     text = response.text
     start_ = re.search(r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK.*", text).span()[1]
     end_ = re.search(r"\*\*\* END OF THE PROJECT GUTENBERG EBOOK", text).span()[0]
     text = text[start_:end_]
     clean_text=re.sub("([^A-Za-z])"," ",text).upper()
     clean_text = str(clean_text[:500])
     #st.write(clean_text)       
     st.subheader("Here is your text: ")
     with st.expander("Please click here to see the full text"):
          st.write(text)
     ready2go = True
     
if ready2go is True:
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
     #st.write(no_double_liste)

     final_list = [word for word in no_double_list if len(word) >= 3]
     st.write(final_list)

     #lemmatization
     lemmatizer = WordNetLemmatizer()
     lemma = []
     for word in final_list:
          lem = lemmatizer.lemmatize(word)
          lemma.append(lem)
     st.write(lemma)


     # #Words translation
     st.subheader("Please, choose the language into which you want to translate the words from the text")
     language_option = st.radio(
     "Choose a language from the following:",
     ('Slovak', 'Italian', 'German', 'Czech', 'Urdu'))
     #st.write('You selected:', language_option)

     lang = ' '
     if language_option.lower() == 'Slovak':
          lang = 'sk'
     elif language_option.lower() == 'Italian':
          lang = 'it'
     elif language_option.lower() == 'German':
          lang = 'de'
     elif language_option.lower() == 'Czech':
          lang = 'cz'
     elif language_option.lower() == 'Urdu':
          lang = 'ur'
     else:
          pass

     translator = Translator()
     translation = []
     
     if lang is not ' ':
          for word in final_list:
               translword = translator.translate(word, lang)
               translation.append(translword.text)
          st.write(translation)
          st.write(len(translation))


     #pronunciation
     pron = []
     for word in final_list:
          url = 'https://api.datamuse.com/words?sp=' + word + '&qe=sp&md=r&ipa=1'
          response = requests.get(url)
          dataFromDatamuse = json.loads(response.text)
          datamuse_data = dataFromDatamuse[0]['tags'][-1]
          pronunciation = re.sub("ipa_pron:"," ",datamuse_data)
          pron.append(pronunciation) 
     st.write(pron)

     #pos-tag
     pos_tags = []
     for word in final_list:
          url= 'https://api.datamuse.com/words?sp=' + word + '&qe=sp&md=p'
          response = requests.get(url)
          dataFromDatamuse = json.loads(response.text)
          pronunciation = dataFromDatamuse[0]['tags'][-1]
          pos_tags.append(pronunciation)
     st.write(pos_tags)

     df = pd.DataFrame({"Word" : final_list, "Lema": lemma, "IPA_pron": pron, "Pos-tag": pos_tags})
     df1 = df.sort_values("Word")
     #df2 = df1.reset_index(inplace = True) 
     #st.write(df)
     st.dataframe(df1)

     #OUTPUT
     st.subheader("Now you can dowload your Vocabulary!")

     @st.cache
     def convert_df(df1):
          return df.to_excel('pandas_to_excel.xlsx', sheet_name='new_sheet_name').encode('utf-8')  #df.to_excel('pandas_to_excel.xlsx', sheet_name='new_sheet_name')


     csv = convert_df(df1)

     st.download_button('Click here to download it',csv, "your_vocabulary.csv","text/csv",key='download-csv')
     
     
     st.balloons()

     comment_words = ''
     stopwords = set(STOPWORDS)
 
     for val in df1.iloc[:, 0]:
          val = str(val)
          slova = val.split()
          for i in range(len(slova)):
               slova[i] = slova[i].lower()
          comment_words += " ".join(slova)+" "
 
     wordcloud = WordCloud(width = 800, height = 800,
                    background_color ='white',
                    stopwords = stopwords,
                    min_font_size = 10).generate(comment_words)
 
     st.set_option('deprecation.showPyplotGlobalUse', False)                    
     plt.figure(figsize = (8, 8), facecolor = None)
     plt.imshow(wordcloud)
     plt.axis("off")
     plt.tight_layout(pad = 0)
 
     #fig = plt.show()
     wcloud = st.pyplot()


     #st.download_button('Download your corrected text', wcloud, file_name='word_cloud.png')

     st.markdown("""---""")

     #SOURCES
     with st. expander("Sources:"):
          st.write(""" - Image: https://aretepiattaforma.it/news/255/Project-Gutenberg-e-digitalizzazione-del-sapere #https://educationsupporthub.co.uk/news-improving-your-childs-vocabulary """)
          st.write(""" - Tutorials: https://docs.streamlit.io/ , https://www.geeksforgeeks.org/generating-word-cloud-python/, https://docs.streamlit.io/knowledge-base/using-streamlit/how-download-pandas-dataframe-csv, https://docs.streamlit.io/library/api-reference/widgets/st.file_uploader""")
 
