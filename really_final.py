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

#TITLE
st.title("GutVoc")

#IMAGE
img = 'https://aretepiattaforma.it/pluginfile.php/1/local_simplified_news/newscontent/255/Project%20Gutenberg.jpg'
#img ='https://educationsupporthub.co.uk/wp-content/uploads/2020/09/vocabulary-1536x1024.jpg' 
st.image(img)

#DESCRIPTION

# user_name = st.text_input("Hello! What is you name?")
# st.write("Welcome!", user_name, "ldjhakjshkjahfkjshfkjshfjs")


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
#df2 = df1.reset_index(inplace = True) 
#st.write(df)
st.dataframe(df1)

#OUTPUT
st.subheader("Now you can dowload your Vocabulary!")

@st.cache
def convert_df(df1):
   return df.to_csv().encode('utf-8')

csv = convert_df(df)

st.download_button('Click here to download it',csv, "your_vocabulary.csv","text/csv",key='download-csv')

st.balloons()

comment_words = ''
stopwords = set(STOPWORDS)
 
for val in df1.CONTENT:
    val = str(val)
    slova = val.split()
    for i in range(len(slova)):
        slova[i] = slova[i].lower()
    comment_words += " ".join(slova)+" "
 
wordcloud = WordCloud(width = 800, height = 800,
                background_color ='white',
                stopwords = stopwords,
                min_font_size = 10).generate(comment_words)
 
                    
plt.figure(figsize = (8, 8), facecolor = None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad = 0)
 
plt.show()

st.markdown("""---""")

#SOURCES
with st. expander("Sources:"):
    st.write(""" - Image: https://aretepiattaforma.it/news/255/Project-Gutenberg-e-digitalizzazione-del-sapere #https://educationsupporthub.co.uk/news-improving-your-childs-vocabulary """)
    st.write(""" - Documentation: https://docs.streamlit.io/ """)
 
