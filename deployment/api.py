from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import json

app=FastAPI()


class model_input(BaseModel):
    
    #declare the types of input data
    
    Pregnancies:int
    Glucose: int
    
    BloodPressure: int
    SkinThickness: int
    
    Insulin: int
    BMI: float
    
    DiabetesPedigreeFunction: float
    Age: int
    

#load our trained machine learning model
diabetes_model=pickle.load(open('model.pkl','rb'))

@app.post('/diabetes_prediction')
def diabetes_prediction(input_param : model_input):
    
    input_data=input_param.json() #load the data in the form of json
    input_dictionary=json.loads(input_data) #turn the loaded json string into dictionary
    
    preg=input_dictionary['Pregnancies']
    glu=input_dictionary['Glucose']
    bp=input_dictionary['BloodPressure']
    
    skin=input_dictionary['SkinThickness']
    ins=input_dictionary['Insulin']
    bmi=input_dictionary['BMI']
    
    dpf=input_dictionary['DiabetesPedigreeFunction']
    age=input_dictionary['Age']
    
    #the list form of our input
    input_list=[preg,glu,bp,skin,ins,bmi,dpf,age]
    
    prediction=diabetes_model.predict([input_list])  #i included another bracket as a form of preprocessing
    
    if prediction[0] == 0:
        return "the person is non diabetic"
    else:
        return "the person is diabetic"
    