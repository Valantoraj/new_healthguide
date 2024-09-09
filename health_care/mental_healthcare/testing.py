import numpy as np
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Dropout
from sklearn.preprocessing import LabelEncoder
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import json
import random
from mental_healthcare import chatbot


with open("C:\\Users\\valan\\Videos\\athish\\athish\\hackathon\\hackathon\\health_care\\mental_healthcare\\symptom_response.json", 'r') as f:
    d = json.load(f)

resp_data={}
for k,v in d.items():
    resp_data[k.lower()]=v
lemmatizer = WordNetLemmatizer()

#Opening json file holding the tags,input pattern,response
with open("C:\\Users\\valan\\Videos\\athish\\athish\\hackathon\\hackathon\\health_care\\mental_healthcare\\intents_mental_health.json") as file:
    data = json.load(file)

with open("C:\\Users\\valan\\Videos\\athish\\athish\\hackathon\\hackathon\\health_care\\mental_healthcare\\required_mental_health_bot.json") as f:
    dict_required=json.load(f)
f.close()
words=dict_required["words"]
classes=dict_required["classes"]

import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import json
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

model = load_model('C:\\Users\\valan\\Videos\\athish\\athish\\hackathon\\hackathon\\health_care\\mental_healthcare\\chatbot_model_mental_health.h5')


# Load the intents file to get class labels
with open("C:\\Users\\valan\\Videos\\athish\\athish\\hackathon\\hackathon\\health_care\\mental_healthcare\\intents_mental_health.json") as file:
    data = json.load(file)
def predictor(message):    
    def clean_up_sentence(sentence):    #Clean up input
        sentence_words = word_tokenize(sentence)
        sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
        return sentence_words

    def bow(sentence, words, show_details=True):    #BoW generator
        sentence_words = clean_up_sentence(sentence)    #Calls up sentence_words that createes a list of words
        bag = [0] * len(words)  #Creates a BoW and initializes each index to 0
        for s in sentence_words:    #Iterates through words list and creates bag of words
            for i, w in enumerate(words):   
                if w == s:
                    bag[i] = 1
                    if show_details:
                        print(f"Found in bag: {w}")
        return np.array(bag)    #Converts to numpy array

    def predict_class(sentence, model):
        bow_input = bow(sentence, words, show_details=False)
        res = model.predict(np.array([bow_input]),verbose=0)[0]   #predicts the class
        ERROR_THRESHOLD = 0.25  #Defining a error threshold (prob.>than 25%)
        results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]    #arranging in encoded class format ,probabbility
        results.sort(key=lambda x: x[1], reverse=True)
        return_list = []
        for r in results:
            return_list.append({"intent": classes[r[0]], "probability": str(r[1])}) #getting class name and probability and forming a dictionary
        return return_list
    def get_response(intents_list, intents_json, message):
        for j in intents_json['intents']:
            if j['tag']=='cannot find':
                cannot_find=random.choice(j['responses'])
            if j['tag']=="odd":
                odd=random.choice(j['responses'])
            if j['tag']=='wait':
                wait=random.choice(j['responses'])
        tag = intents_list[0]['intent']
        # Handle other intents as usual
        if tag=='yes':
            if chatbot.prev!=None:
                print("YES:",chatbot.prev)
                return chatbot.chat(random.choice(resp_data[chatbot.prev]))
            else:
                return odd
        elif tag=='no':
            if chatbot.prev_prev!=None:
                print("NO: ",chatbot.prev_prev)
                return chatbot.chat(random.choice(resp_data[chatbot.prev_prev]))
            else:
                return odd
        elif tag=='symptoms':
            return chatbot.chat(message)
        
        for i in intents_json['intents']:
            if i['tag'] == tag:
                return random.choice(i['responses'])
        
        return cannot_find
        

    print("Chatbot is running!")

    while True:
        ints = predict_class(message, model)
        response = get_response(ints, data,message)
        return response
#Train
'''

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
model.save('chatbot_model_mental_health.h5')'''