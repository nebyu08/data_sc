
import pickle 
import numpy as np
import streamlit as st

#load the model
model=pickle.load(open("C:/Users/dread-miles/Documents/diabetic prediction project/model.pkl","rb"))


def diabities_prediction(input_data):
    # changing the data type
    input_data_as_numpy=np.asarray(input_data)

    #chaging the data shape
    input_data_reshape=input_data_as_numpy.reshape(1,-1)

    prediction=model.predict(input_data_reshape)

    #print("the prediciton is:",prediction)

    if(prediction[0] == 0):
      return "the patient has not diabetic"
    else:
      return "the patient is diabetic"
    

def main():
    
    #give a title to the streamlit app
    st.title("Diabeties prediction web app")
     
    #lets take input from the user    
    Pregnancies=st.text_input("Number of pregnancies")
    Glucose=st.text_input("Glucose level")
    
    BloodPressure=st.text_input("Blood pressure level")
    SkinThickness=st.text_input("Skin Thick Ness")
    Insulin=st.text_input("Insulin level")
    
    BMI=st.text_input("BMI Number")
    DiabetesPedigreeFunction=st.text_input("Diabetes Pedigree Function ")
    age=st.text_input("Age")
    
    #diagnosis value
    diagnosis=''
    
    #creating a value for prediction
    if st.button('Diabetes Test Result'):
        diagnosis=diabities_prediction([Pregnancies,Glucose,BloodPressure,SkinThickness,Insulin,BMI,DiabetesPedigreeFunction,age])
    
    st.success(diagnosis)

if __name__== '__main__':
    main()