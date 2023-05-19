from newspaper import Article
import random
import string
import numpy as np
import warnings
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


#ignore the warnings
warnings.filterwarnings('ignore')
     

#download package from nltk
nltk.download('punkt',quiet=True) # punkt has resource includes data needed for tokenization
nltk.download('wordnet',quiet=True) # resource includes lexical data such as synonyms, antonyms, and word definitions


#get artical url
article= Article('https://www.britannica.com/science/physics-science') # object creation
article.download() # downnloads contents of HTML file
article.parse() # removes ads,navigation bar etc.. that are present in the HTML file
article.nlp() #it performs tokenization, part-of-speech tagging, and named entity recognition to identify important words and phrases in the text.
corpus=article.text # assigns the processed text content of the article
#print
#print(corpus)


#tokenization
text=corpus
sentence_tokens=nltk.sent_tokenize(text) #This function breaks up the text into individual sentences by identifying common sentence-ending punctuation marks such as periods, question marks, and exclamation points.
#print(sent_tokens)


#creating a dictionary to remove the punctuation
remove_punct_dict=dict( (ord(punct),None) for punct in string.punctuation) # string.punctuation is a predefined python string contains  !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
# ord(punct) function is called to get the Unicode code point for that character
#print(string.punctuation)
#print(remove_punct_dict)
     
#create a function to return lower case words 
def LemNormalize(text):
  return nltk.word_tokenize(text.lower().translate(remove_punct_dict))  #word_tokenize function helps to convert the text into individual words
#print(LemNormalize(text))


#keywords for greetings
greeting_input=["hi","hello","hey","hola"]
greeting_response=["howdy","hey there","hi","hello :)"]
def greeting(sentence):
  for word in sentence.split():
    if word.lower() in greeting_input:
      return random.choice(greeting_response)
     
def response(user_response):
 #user response and robo responce
  #user_response="What is chronic disease"
  user_response=user_response.lower()
  #print(user_response)
  #robo response
  robo_response=''
  sentence_tokens.append(user_response)
  #print(sent_tokens)
  tfidfvec=TfidfVectorizer(tokenizer=LemNormalize , stop_words='english')
  tfidf=tfidfvec.fit_transform(sentence_tokens)
  #print(tfidf)
  #get similarity score
  val=cosine_similarity(tfidf[-1],tfidf)
  #print(val)
  idx=val.argsort()[0][-2]
  flat=val.flatten()
  flat.sort()
  score=flat[-2]
  #print(score)
  if score==0:
    robo_response=robo_response+"sorry,i dont understand"
  else:
    robo_response=robo_response+sentence_tokens[idx]

  sentence_tokens.remove(user_response)
  return robo_response

###############################################################################################################################################
flag=True
print("hello!!! this is Zoe,i can answer your queris related to light ,type bye to exit")
while(flag==True):
  user_response=input("User : ")
  #user_response=user_response.lower()
  if(user_response!='bye'):
    if(user_response=='thanks' or user_response=='thank you'):
      flag=False
      print("Zoe : anytime :)")
    else:
       if( greeting(user_response) != None):
         print("Zoe : "+ greeting(user_response))
       else:
         print("Zoe :"+response(user_response))
  else:
    flag=False
    print("Zoe: see you later :)")