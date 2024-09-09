import pandas as pd
import json
import joblib
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import load_model
import random
import numpy as np
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Dropout
from sklearn.preprocessing import LabelEncoder
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.model_selection import train_test_split

string_sug_ask=''
prev_prev=None
prev=None
asked=set()
count_tries=0
user_input=[]
data=pd.read_csv("C:\\Users\\valan\\Videos\\mental_healthcare\\disease_symptom_matrix.csv", encoding='ISO-8859-1')


with open("C:\\Users\\valan\\Videos\\mental_healthcare\\mental_health_data.json",'r') as f:
    old_disease_data=json.load(f)    
f.close()
with open("C:\\Users\\valan\\Videos\\mental_healthcare\\mental_health_questions.json",'r') as f:
    ask_ques=json.load(f)    
f.close()
with open("C:\\Users\\valan\\Videos\\mental_healthcare\\cure.json",'r') as f:
    cure=json.load(f)    
f.close()
with open("C:\\Users\\valan\\Videos\\athish\\athish\\hackathon\\hackathon\\health_care\\mental_healthcare\\suggestion.json") as f:
    suggest=json.load(f)
f.close()
cure_dict={}
for k,v in cure.items():
    cure_dict[k.lower()]=v
d={}
for k,v in ask_ques['symptoms'].items():
    d[k.lower()]=v
ask_ques['symptoms']=d
with open("C:\\Users\\valan\\Videos\\mental_healthcare\\intents_mental_health.json",'r') as f:
    intents=json.load(f)    
f.close()


disease_data={}
for k,v in old_disease_data.items():
    k_new=k.lower()
    v_new=[]
    for i in v:
        v_new.append(i.lower())
    disease_data[k_new]=v_new
    
#Independent-X
X=data.drop(columns=['Disease'], axis='columns')
symptoms=list(X.columns)


rf_classifier = joblib.load('C:\\Users\\valan\\Videos\\mental_healthcare\\rf_classifier_model_mental_health.pkl')
scaler = joblib.load('C:\\Users\\valan\\Videos\\mental_healthcare\\scaler_mental_health.pkl')



nltk.download('punkt')
nltk.download('wordnet')

try:
    with open("C:\\Users\\valan\\Videos\\mental_healthcare\\symptom_response.json", 'r') as f:
        data = json.load(f)
except FileNotFoundError:
    print("Error: The file was not found.")
    data = {}
except json.JSONDecodeError as e:
    print(f"Error: Failed to decode JSON. {e}")
    data = {}

if not data:
    print("Error: No data to process.")
    exit()

lemmatizer = WordNetLemmatizer()

def preprocess(sentence):
    tokens = word_tokenize(sentence.lower())
    lemmatized_words = [lemmatizer.lemmatize(token) for token in tokens if token.isalnum()]
    return ' '.join(lemmatized_words)
sentences = []
labels = []
for label, texts in data.items():
    for text in texts:
        sentences.append(preprocess(text))
        labels.append(label)

label_encoder = LabelEncoder()
y = label_encoder.fit_transform(labels)
d_required={}
with open("C:\\Users\\valan\\Videos\\v\\v\\website\\mental_healthcare\\required_mental_health_classify.json") as f:
    d_required=json.load(f)
words=d_required["words"]
word_index = {word: i for i, word in enumerate(words)}
def sentence_to_vector(sentence):
    vector = np.zeros(len(word_index))
    for word in sentence.split():
        if word in word_index:
            vector[word_index[word]] = 1
    return vector




string_ret="I think you are alright.But here are some steps to main good mental health, \n\n"
count=1
for i in cure_dict["generalmentalhealthtips"]:
    string_ret+=f"{count}. {i}"
    count+=1

def sympt_vect(user_input, symptoms):
    symptom_dict = {symptom.lower(): 0 for symptom in symptoms}
    for symptom in user_input:
        symptom = symptom.strip().lower()
        if symptom in symptom_dict:
            symptom_dict[symptom] = 1
    return [symptom_dict[symptom] for symptom in symptoms]

def prob_format(probabilities, class_labels):
    disease_prob = {disease: prob for disease, prob in zip(class_labels, probabilities) if prob > 0}
    disease_prob=dict(sorted(disease_prob.items(), key=lambda item: item[1], reverse=True))
    print(disease_prob)
    return disease_prob

def disease_conclude(disease, probability):
    string_cure=f"I found that you have {disease},\n"
    string_cure+='Follow these to reduce/overcome this issue,\n\n'
    temp_cure=''
    count=1
    for i in cure_dict[disease]:
        temp_cure+=f'{count}. {i}\n'
        count+=1
    string_cure+=temp_cure
    string_cure+='I hope it helped you, make sure you follow these steps.\n'
    return string_cure
def pred(symptoms):
    global asked
    global user_input
    global prev
    global prev_prev
    global count_tries
    global string_sug_ask
    count_tries+=1
    
    # Vectorize the user input
    user_input_vector = sympt_vect(user_input, symptoms)
    
    # Create a DataFrame for the user input
    user_input_df = pd.DataFrame([user_input_vector], columns=symptoms)
    
    # Scale the user input
    user_input_scaled = scaler.transform(user_input_df)
    
    # Get predictions and class labels
    probabilities = rf_classifier.predict_proba(user_input_scaled)[0]
    class_labels = rf_classifier.classes_
    
    # Format and sort the probabilities
    disease_prob = prob_format(probabilities, class_labels)
    if count_tries>20:
        return string_ret
    if not disease_prob:
        return "Bot: Sorry, we can't conclude..."

    # Conclude the disease if the probability is above the threshold
    for disease, probability in disease_prob.items():
        if probability > 0.3:    
            asked=set()
            prev=None
            prev_prev=None
            return disease_conclude(disease,probability)
        else:
            for i in disease_data[disease]:
                if i not in asked:
                    prev=i
                    asked.add(i)
                    string_sug_ask+= f"{random.choice(ask_ques['symptoms'][i])}"
                    return string_sug_ask
                
    asked=set()
    prev=None
    prev_prev=None
    return string_ret




def chat(message):
    model = load_model('C:\\Users\\valan\\Videos\\mental_healthcare\\chatbot_model_mental_health_sympt.h5')
    # Function to predict symptom based on user input
    def predict_symptom(first_inp):
        processed_input = preprocess(first_inp)
        input_vector = sentence_to_vector(processed_input).reshape(1, -1)
        prediction = model.predict(input_vector).flatten()
        
        
        max_probability = np.max(prediction)
        if max_probability > 0.1:
            global prev_prev
            global user_input
            global string_sug_ask
            predicted_label_index = np.argmax(prediction)
            predicted_label = label_encoder.classes_[predicted_label_index]
            user_input.append(predicted_label)            
            temp=prev_prev
            prev_prev=predicted_label.lower()
            if temp==prev_prev:
                string_sug_ask=''
            else:
                string_sug_ask=f"{suggest[prev_prev]["Response"]}\n"
                count_num=1
                for i in suggest[prev_prev]["Suggestions"]:
                    string_sug_ask+=f"{count_num}. {i}\n"
                    count_num+=1
                string_sug_ask+="\n\n"
            return pred(symptoms)
        else:
            return "Cant understand"

    global user_input
    decide=predict_symptom(message)
    if decide=="Cant understand":
        return "I cant understand could you try say it more clearly"
    elif decide=="Bot: Sorry, we can't conclude...":
        return decide
    else:
        return decide

#Train

    '''
    # Prepare the dataset
    sentences = []
    labels = []
    for label, texts in data.items():
        for text in texts:
            sentences.append(preprocess(text))
            labels.append(label)

    # Encode labels
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(labels)

    # Create a list of unique words
    words = sorted(set(word for sentence in sentences for word in sentence.split()))
    word_index = {word: i for i, word in enumerate(words)}

    # Convert sentences to feature vectors
    def sentence_to_vector(sentence):
        vector = np.zeros(len(word_index))
        for word in sentence.split():
            if word in word_index:
                vector[word_index[word]] = 1
        return vector

    X = np.array([sentence_to_vector(sentence) for sentence in sentences])

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Define the neural network model
    model = Sequential([
        Dense(1080, input_shape=(len(word_index),), activation='relu'),
        Dropout(0.5),
        Dense(512, activation='relu'),
        Dropout(0.5),
        Dense(256, activation='relu'),
        Dense(len(label_encoder.classes_), activation='softmax')
    ])

    # Compile the model
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    # Train the model
    model.fit(X_train, y_train, epochs=250, batch_size=1080, verbose=1)

    # Evaluate the model
    loss, accuracy = model.evaluate(X_test, y_test)
    print(f"Test Accuracy: {accuracy:.4f}")
    model.save('chatbot_model_mental_health_sympt.h5')
    '''
