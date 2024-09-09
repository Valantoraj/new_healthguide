'''import numpy as np
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Dropout
from sklearn.preprocessing import LabelEncoder
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import json
import random
#Opening json file holding the tags,input pattern,response
with open("C:\\Users\\valan\\Videos\\athish\\athish\\hackathon\\hackathon\\health_care\\mental_healthcare\\intents_mental_health.json") as file:
    data = json.load(file)
lemmatizer = WordNetLemmatizer()
lemmatizer = WordNetLemmatizer()

#Opening json file holding the tags,input pattern,response
with open("C:\\Users\\valan\\Videos\\athish\\athish\\hackathon\\hackathon\\health_care\\mental_healthcare\\intents_mental_health.json") as file:
    data = json.load(file)

#Initialization
words = []      #Hold all words in patterns
classes = []    #Hold all tags
documents = []  #Holds (word,tag)
ignore_letters = ['?', '!', '.', ',']   #Holds characters to be ingnored
    
for intent in data['intents']:  #Iterates through each intent
    for pattern in intent['patterns']:  #iterates through specific intent's patterns
        word_list = word_tokenize(pattern)  #Tokenizes the sentences(patterns)
        words.extend(word_list) #Appends the tokenized words to word list
        documents.append((word_list, intent['tag']))    #Appends both tokenized words and tags to document
        if intent['tag'] not in classes:    #If and only if tag is not already present in classes appends the tags to it
            classes.append(intent['tag'])

#Clip to root form
words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_letters] #['I','am','cat','dog'] 
#[(['I','am','dog'],dog),(['I','am','cat'],'cat')] [1,1,1,0]  [1,1,0,1]  #['dog','cat']  #[1,0] ['i','love','petting','dogs']  [1,0,0,1]
words = sorted(set(words)) #Only unique words

classes = sorted(set(classes))  #Only unique classes

dict_required={}
dict_required["words"]=words
dict_required["classes"]=classes
with open("C:\\Users\\valan\\Videos\\athish\\athish\\hackathon\\hackathon\\health_care\\mental_healthcare\\required_mental_health_bot.json",'w')as f:
    json.dump(dict_required,f,indent=4)
f.close()
with open("C:\\Users\\valan\\Videos\\athish\\athish\\hackathon\\hackathon\\health_care\\mental_healthcare\\required_mental_health_bot.json") as f:
    dict_required=json.load(f)
f.close()
words=dict_required["words"]
classes=dict_required["classes"]
#Training 
training = []   #Training List
output_empty = [0] * len(classes)   #numerically encoded class list

for document in documents:  #Iterates through documents list
    bag = []    #Bag of words
    word_patterns = document[0] #Words of a particular class
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]  #Converts to root form
    for word in words:  #Creates a BoW with 1 if a word is present and 0 if not
        bag.append(1) if word in word_patterns else bag.append(0)
    
    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1  #Assigns 1 to the class the words/patterns belong
    training.append([bag, output_row])  #Appends nested list bag and output_row(class)

random.shuffle(training)    #Shuffling the training data
training = np.array(training, dtype=object) #Converts to array for effocient access and coompatibility with tensorflow

train_x = np.array(list(training[:, 0]))    #BoW
train_y = np.array(list(training[:, 1]))    #Class

model =Sequential()    #Creates an object of Sequential model

#128 neural lines,
#input shape - len of BoW,
#activation - Rectified Linear Unit
model.add(Dense(1080, input_shape=(len(train_x[0]),), activation='relu'))    
model.add(Dropout(0.5)) #Drops 50%
model.add(Dense(512, activation='relu')) #Adds another 68 neural lines
model.add(Dropout(0.5)) #Again drop 50%

#len of tags,
#activation - Best possible outcome
model.add(Dense(len(train_y[0]), activation='softmax')) 

#adam - Adaptive learning rate optimization algo.,
#evaluating metrics is accuracy,
#loss function - used for multiclass classification problem involving a one hot encoded target.
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])  

#epochs - no of times the model goes through the entire dataset,
#batch - no of samplles processed at a time,
#verbose - shows process output
model.fit(train_x, train_y, epochs=200, batch_size=1080, verbose=1)

#Saves the model
model.save('C:\\Users\\valan\\Videos\\athish\\athish\\hackathon\\hackathon\\health_care\\mental_healthcare\\chatbot_model_mental_health.h5')'''
import json
with open("C:\\Users\\valan\\Videos\\athish\\athish\\hackathon\\hackathon\\health_care\\mental_healthcare\\mental_health_data.json") as f:
    data=json.load(f)
l=set()
for k,v in data.items():
    for val in v:
        l.add(val.lower())
print(len(l))
f.close()
with open("C:\\Users\\valan\\Videos\\athish\\athish\\hackathon\\hackathon\\health_care\\mental_healthcare\\suggestion.json") as f:
    data1=json.load(f)
f.close()
l1=set()
d={}
for k,v in data1.items():
    d[k.lower()]=v
with open("C:\\Users\\valan\\Videos\\athish\\athish\\hackathon\\hackathon\\health_care\\mental_healthcare\\suggestion.json",'w') as f:
    json.dump(d,f,indent=4)