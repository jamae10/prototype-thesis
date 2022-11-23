# --- IMPROVED GRADIENT BOOSTING ALGORITHM --- 

# Importing libraries
import os
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import mode
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from .models import *


# Remove warnings from terminal
import warnings
warnings.filterwarnings('ignore')

BASE_DIR = Path(__file__).resolve().parent.parent

# Reading the train data by removing the last column since it's an empty column
DATA_PATH = os.path.join(BASE_DIR, 'static/datasets/Train.csv')
data = pd.read_csv(DATA_PATH).dropna(axis = 1)

# Checking whether the dataset is balanced or not
disease_counts = data["prognosis"].value_counts()
temp_df = pd.DataFrame({
    "Disease": disease_counts.index,
    "Counts": disease_counts.values
})

# Encoding the target value into numerical value using LabelEncoder
encoder = LabelEncoder()
data["prognosis"] = encoder.fit_transform(data["prognosis"])

# Splitting the data set into train and test 
X = data.iloc[:,:-1]
y = data.iloc[:, -1]
X_train, X_test, y_train, y_test =train_test_split(
X, y, test_size = 0.2, random_state = 24)

# Training and testing GB Classifier and other models
final_lr_model = LogisticRegression()
final_rf_model = RandomForestClassifier(random_state=18)
final_gb_model = GradientBoostingClassifier(n_estimators=20,learning_rate=0.1,random_state=10,max_features=5)
final_lr_model.fit(X, y)
final_gb_model.fit(X, y)
final_rf_model.fit(X, y)

# Creating a function that can take symptoms as input and generate predictions for disease 
symptoms = X.columns.values

# Creating a symptom index dictionary to encode the input symptoms into numerical form
symptom_index = {}
for index, value in enumerate(symptoms):
    symptom = " ".join([i.capitalize() for i in value.split("_")])
    symptom_index[symptom] = index

data_dict = {
    "symptom_index":symptom_index,
    "predictions_classes":encoder.classes_
}

# Defining the Function
# Input: string containing symptoms separated by commmas
# Output: Generated predictions by models
def predictDisease(symptoms):
    symptoms = symptoms.split(",")
    symptoms_list = (','.join(symptoms))

    # Creating input data for the models
    input_data = [0] * len(data_dict["symptom_index"])
    for symptom in symptoms:
        index = data_dict["symptom_index"][symptom]
        input_data[index] = 1

    # Reshaping the input data and converting it
    # Into suitable format for model predictions
    input_data = np.array(input_data).reshape(1,-1)

    # Generating individual outputs
    lr_prediction = data_dict["predictions_classes"][final_lr_model.predict(input_data)[0]]
    rf_prediction = data_dict["predictions_classes"][final_rf_model.predict(input_data)[0]]
    gb_prediction = data_dict["predictions_classes"][final_gb_model.predict(input_data)[0]]
     
    
    # Making final prediction with combined models
    final_prediction = mode([lr_prediction, rf_prediction, gb_prediction])[0][0]
    predictions = {
        "logistic_regression_prediction": lr_prediction,
        "random_forest_prediction": rf_prediction,
        "gradient_boosting_prediction": gb_prediction,
        "final_prediction": final_prediction,
        "symptoms": symptoms_list,
    }
    return predictions