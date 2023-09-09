
import json 
import requests

url='http://127.0.0.1:8000/diabetes_prediction'  #not fullfilled yet


input_data={
    
    'Pregnancies':6,
    'Glucose':148,
    
    'BloodPressure':72,
    'SkinThickness':35,
    
    'Insulin':0,
    'BMI':33.6,
    
    'DiabetesPedigreeFunction':0.627,
    'Age':50
    
    }
    
input_json=json.dumps(input_data)
response=requests.post(url,data=input_json)

print(response.text)