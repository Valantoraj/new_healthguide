import numpy as np
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Dropout
from sklearn.preprocessing import LabelEncoder
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from tensorflow.keras import models
import json
import random
from healthcare import complex_dis_diagnose
from healthcare import common_dis_diagnose


#Lemmatizer object
lemmatizer = WordNetLemmatizer()

#Opening json file holding the tags,input pattern,response
with open("C:\\Users\\valan\\Videos\\athish\\athish\\hackathon\\hackathon\\health_care\\healthcare\\intents.json") as file:
    data = json.load(file)

with open("C:\\Users\\valan\\Videos\\athish\\athish\\hackathon\\hackathon\\health_care\\healthcare\\required_data_sympt.json",'r') as f:
    d_load=json.load(f)
f.close()
symptom_list=d_load["symptom_list"]
symptom_list_common=d_load["symptom_list_common"]
print("stored")
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
    s
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
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))    
model.add(Dropout(0.5)) #Drops 50%
model.add(Dense(64, activation='relu')) #Adds another 68 neural lines
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
model.fit(train_x, train_y, epochs=200, batch_size=64, verbose=1)

#Saves the model
model.save('C:\\Users\\valan\\Videos\\athish\\athish\\hackathon\\hackathon\\chatbot_model.h5')'''

model=models.load_model('C:\\Users\\valan\\Videos\\athish\\athish\\hackathon\\hackathon\\chatbot_model.h5')
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
        bow_input = bow(sentence, words, show_details=True)
        res = model.predict(np.array([bow_input]),verbose=0)   #predicts the class  ((,),)
        print(res)
        res=res[0]
        ERROR_THRESHOLD = 0.25  #Defining a error threshold (prob.>than 25%)
        results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]    #arranging in encoded class format ,probability
        results.sort(key=lambda x: x[1], reverse=True)
        return_list = []
        for r in results:
            return_list.append({"intent": classes[r[0]], "probability": str(r[1])}) #getting class name and probability and forming a dictionary
        return return_list
    def get_response(intents_list, intents_json, message):
        count_1=0
        count_2=0
        for j in intents_json['intents']:
            if j['tag']=='cannot find':
                cannot_find=random.choice(j['responses'])
            if j['tag']=='wait':
                wait=random.choice(j['responses'])
        tag = intents_list[0]['intent']
        found_symptoms=0
        symptoms_found=[]
        if tag=='yes':
            if common_dis_diagnose.prev!=None:
                common_dis_diagnose.yes_reduction_factor+=0.025
                return common_dis_diagnose.main([common_dis_diagnose.prev])
            if complex_dis_diagnose.prev!=None:
                complex_dis_diagnose.yes_reduction_factor+=0.025
                return complex_dis_diagnose.main([complex_dis_diagnose.prev])
            else:
                return cannot_find
        if tag=='no':
            if common_dis_diagnose.prev_prev!=None:
                common_dis_diagnose.no_reduction_factor+=0.05
                return common_dis_diagnose.main(common_dis_diagnose.prev_prev)
            if complex_dis_diagnose.prev_prev!=None:
                complex_dis_diagnose.no_reduction_factor+=0.025
                return complex_dis_diagnose.main(complex_dis_diagnose.prev_prev)
            else:
                return cannot_find
        
        # If the intent is 'symptoms', check for symptoms in the user's message
        if tag == 'symptoms':
            
            for i in symptom_list_common:
                if i in message:
                    symptoms_found.append(i.lower())
                    count_1+=1
            for j in symptom_list:
                if j in message:
                    symptoms_found.append(j.lower())
                    count_2+=1
            print(count_1,count_2)
            if count_1>=count_2:
                return common_dis_diagnose.main(symptoms_found)
            elif count_1<count_2:
                return complex_dis_diagnose.main(symptoms_found)
        
        # Handle other intents as usual
        for i in intents_json['intents']:
            if i['tag'] == tag:
                return random.choice(i['responses'])
        
        return cannot_find
        

    print("Chatbot is running!")

    while True:
        ints = predict_class(message, model)
        response = get_response(ints, data,message)
        return response
