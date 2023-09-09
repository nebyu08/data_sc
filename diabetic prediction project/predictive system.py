

import pickle 
import numpy as np

#load the model
model=pickle.load(open("C:/Users/dread-miles/Documents/diabetic prediction project/model.pkl","rb"))

#lets check if it works

input_data=(9,89,62,0,0,22.5,0.142,33)

# changing the data type
input_data_as_numpy=np.asarray(input_data)

#chaging the data shape
input_data_reshape=input_data_as_numpy.reshape(1,-1)

prediction=model.predict(input_data_reshape)

#print("the prediciton is:",prediction)

if(prediction[0] == 0):
  print("the patient has not diabetic")
else:
  print("the patient is diabetic")