import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler,LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Function to make predictions based on user input
def predict_heart_disease(user_input):
    print("hi")
    # Create a DataFrame for the user input
    df = pd.read_csv("C:\\Users\\valan\\Videos\\athish\\athish\\hackathon\\hackathon\\health_care\\Heart_Disease_Prediction.csv")

    # Convert categorical features to numerical values
    df['Sex'] = df['Sex'].astype('category').cat.codes
    df['Chest pain type'] = df['Chest pain type'].astype('category').cat.codes
    df['FBS over 120'] = df['FBS over 120'].astype('category').cat.codes
    df['EKG results'] = df['EKG results'].astype('category').cat.codes
    df['Exercise angina'] = df['Exercise angina'].astype('category').cat.codes
    df['Slope of ST'] = df['Slope of ST'].astype('category').cat.codes
    df['Thallium'] = df['Thallium'].astype('category').cat.codes

    # Encode the target variable as a continuous variable
    df['Heart Disease'] = df['Heart Disease'].apply(lambda x: 1 if x == 'Presence' else 0)

    # Define features and target
    X = df.drop('Heart Disease', axis=1)
    y = df['Heart Disease']

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Standardize features
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Initialize and train the regressor
    regressor = RandomForestRegressor(n_estimators=1000, random_state=42)
    regressor.fit(X_train, y_train)

    # Evaluate the model
    y_pred = regressor.predict(X_test)
    print("Mean Squared Error:", mean_squared_error(y_test, y_pred))
    print("R^2 Score:", r2_score(y_test, y_pred))
    input_df = pd.DataFrame([user_input], columns=X.columns)
    
    # Encode categorical features
    input_df['Sex'] = input_df['Sex'].astype('category').cat.codes
    input_df['Chest pain type'] = input_df['Chest pain type'].astype('category').cat.codes
    input_df['FBS over 120'] = input_df['FBS over 120'].astype('category').cat.codes
    input_df['EKG results'] = input_df['EKG results'].astype('category').cat.codes
    input_df['Exercise angina'] = input_df['Exercise angina'].astype('category').cat.codes
    input_df['Slope of ST'] = input_df['Slope of ST'].astype('category').cat.codes
    input_df['Thallium'] = input_df['Thallium'].astype('category').cat.codes
    
    # Standardize features
    input_df = scaler.transform(input_df)
    
    # Make prediction
    prediction = regressor.predict(input_df)
    
    return prediction[0]

# Load and preprocess data


# Function to make predictions based on user input
def predict_stroke(user_input):
    
    df = pd.read_csv("C:\\Users\\valan\\Videos\\athish\\athish\\hackathon\\hackathon\\health_care\\full_data.csv")

# Convert categorical features to numerical values using LabelEncoder
    label_encoders = {
        'gender': LabelEncoder(),
        'work_type': LabelEncoder(),
        'Residence_type': LabelEncoder(),
        'smoking_status': LabelEncoder(),
        'ever_married': LabelEncoder()
    }

    for column in label_encoders:
        df[column] = label_encoders[column].fit_transform(df[column])

    # Ensure the target variable is numeric for regression (e.g., 'target_variable' is your target)
    df['stroke'] = df['stroke'].astype(float)  # Replace 'target_variable' with your actual target column

    # Define features and target
    X = df.drop('stroke', axis=1)
    y = df['stroke']

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Check if all features are numerical
    print("Data Types Before Scaling:")
    print(X_train.dtypes)

    # Standardize features
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Initialize and train the regressor
    regressor = RandomForestRegressor(n_estimators=1000, random_state=42)
    regressor.fit(X_train, y_train)

    # Make predictions
    y_pred = regressor.predict(X_test)

    # Evaluate the model
    print("Mean Squared Error:", mean_squared_error(y_test, y_pred))
    print("R^2 Score:", r2_score(y_test, y_pred))

    # Create a DataFrame for the user input
    input_df = pd.DataFrame([user_input])
    
    # Encode categorical features
    for column in ['gender', 'work_type', 'Residence_type', 'smoking_status', 'ever_married']:
        input_df[column] = label_encoders[column].transform(input_df[column])
    
    # Ensure all features are numerical before scaling
    print("Data Types for Prediction Input:")
    print(input_df.dtypes)
    
    # Standardize features
    input_df = scaler.transform(input_df)
    
    # Make prediction
    prediction = regressor.predict(input_df)
    
    return prediction[0]

# Function to make predictions based on user input
def predict_lung_cancer(user_input):
    
    df = pd.read_csv("C:\\Users\\valan\\Videos\\athish\\athish\\hackathon\\hackathon\\health_care\\lung cancer survey.csv")

    # Print data types before preprocessing
    print("Data Types Before Preprocessing:")
    print(df.dtypes)

    # Encode categorical features
    label_encoders = {}
    categorical_columns = ['GENDER', 'YELLOW_FINGERS', 'ANXIETY', 'PEER_PRESSURE', 'CHRONIC DISEASE', 
                            'FATIGUE', 'ALLERGY', 'WHEEZING', 'ALCOHOL CONSUMING', 'COUGHING', 
                            'SHORTNESS OF BREATH', 'SWALLOWING DIFFICULTY', 'CHEST PAIN']

    for column in categorical_columns:
        le = LabelEncoder()
        df[column] = le.fit_transform(df[column])
        label_encoders[column] = le

    # Encode the target variable
    df['LUNG_CANCER'] = df['LUNG_CANCER'].apply(lambda x: 1 if x == 'YES' else 0)

    # Define features and target
    X = df.drop('LUNG_CANCER', axis=1)
    y = df['LUNG_CANCER']

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Standardize features
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Initialize and train the regressor
    regressor = RandomForestRegressor(n_estimators=1000, random_state=42)
    regressor.fit(X_train, y_train)

    # Make predictions and evaluate the model
    y_pred = regressor.predict(X_test)
    print("Mean Squared Error:", mean_squared_error(y_test, y_pred))
    print("R^2 Score:", r2_score(y_test, y_pred))

    # Create a DataFrame for the user input
    input_df = pd.DataFrame([user_input])
    
    # Encode categorical features
    for column, le in label_encoders.items():
        if column in input_df.columns:
            input_df[column] = le.transform(input_df[column])
    
    # Standardize features
    input_df = scaler.transform(input_df)
    
    # Make prediction
    prediction = regressor.predict(input_df)
    
    return prediction[0]


# Load the data from the CSV file


# Function to make predictions based on user input
def predict_diabetes(user_input):
    df = pd.read_csv("C:\\Users\\valan\\Videos\\athish\\athish\\hackathon\\hackathon\\health_care\\Diabetes_prediction.csv")

    # Print data types before preprocessing
    print("Data Types Before Preprocessing:")
    print(df.dtypes)

    # Define features and target
    X = df.drop('Diagnosis', axis=1)
    y = df['Diagnosis']

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Standardize features
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Initialize and train the regressor
    regressor = RandomForestRegressor(n_estimators=1000, random_state=42)
    regressor.fit(X_train, y_train)

    # Make predictions and evaluate the model
    y_pred = regressor.predict(X_test)
    print("Mean Squared Error:", mean_squared_error(y_test, y_pred))
    print("R^2 Score:", r2_score(y_test, y_pred))
    # Create a DataFrame for the user input
    input_df = pd.DataFrame([user_input])
    
    # Standardize features
    input_df = scaler.transform(input_df)
    
    # Make prediction
    prediction = regressor.predict(input_df)
    
    # Return prediction (since it's a regression model, the result is continuous)
    return prediction[0]

def predict_kidney_stone(user_input):
    df = pd.read_csv("C:\\Users\\valan\\Videos\\athish\\athish\\hackathon\\hackathon\\health_care\\kindey stone urine analysis.csv")


    # Ensure target is numeric
    df['target'] = df['target'].astype(float)

    # Define features and target
    X = df.drop('target', axis=1)
    y = df['target']

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Standardize features
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Initialize and train the regressor
    regressor = RandomForestRegressor(n_estimators=1000, random_state=42)
    regressor.fit(X_train, y_train)

    # Make predictions
    y_pred = regressor.predict(X_test)

    # Evaluate the model
    print("Mean Squared Error:", mean_squared_error(y_test, y_pred))
    print("R^2 Score:", r2_score(y_test, y_pred))

    # Create a DataFrame for the user input
    input_df = pd.DataFrame([user_input])
    
    # Standardize features
    input_df = scaler.transform(input_df)
    
    # Make prediction
    prediction = regressor.predict(input_df)
    
    return prediction[0]
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

def predict_liver_disease(user_input):
    df = pd.read_csv("C:\\Users\\valan\\Videos\\athish\\athish\\hackathon\\hackathon\\health_care\\Liver_disease_data.csv")

    # Convert categorical features to numerical values
    label_encoders = {
        'Gender': LabelEncoder(),
        'Smoking': LabelEncoder(),
        'GeneticRisk': LabelEncoder(),
        'Diabetes': LabelEncoder(),
        'Hypertension': LabelEncoder()
    }

    for column, encoder in label_encoders.items():
        df[column] = encoder.fit_transform(df[column])

    # Define features and target
    df['Age'] = df['Age'].astype(float)
    df['BMI'] = df['BMI'].astype(float)
    df['AlcoholConsumption'] = df['AlcoholConsumption'].astype(float)
    df['Smoking'] = df['Smoking'].astype(float)
    df['GeneticRisk'] = df['GeneticRisk'].astype(float)
    df['PhysicalActivity'] = df['PhysicalActivity'].astype(float)
    df['Diabetes'] = df['Diabetes'].astype(float)
    df['Hypertension'] = df['Hypertension'].astype(float)
    df['LiverFunctionTest'] = df['LiverFunctionTest'].astype(float)
    df['Diagnosis'] = df['Diagnosis'].astype(float)

    X = df.drop('Diagnosis', axis=1)
    y = df['Diagnosis']

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Standardize features
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Initialize and train the regressor
    regressor = RandomForestRegressor(n_estimators=1000, random_state=42)
    regressor.fit(X_train, y_train)

    # Make predictions
    y_pred = regressor.predict(X_test)

    # Evaluate the model
    print("Mean Squared Error:", mean_squared_error(y_test, y_pred))
    print("R^2 Score:", r2_score(y_test, y_pred))

    # Create a DataFrame for the user input
    input_df = pd.DataFrame([user_input])

    # Encode categorical features
    for column in ['Gender', 'Smoking', 'GeneticRisk', 'Diabetes', 'Hypertension']:
        input_df[column] = label_encoders[column].transform(input_df[column])

    # Ensure all features are numerical before scaling
    input_df = scaler.transform(input_df)

    # Make prediction
    prediction = regressor.predict(input_df)

    return prediction[0]  # Return the single prediction value