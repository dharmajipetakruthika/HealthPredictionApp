import pandas as pd 
from sklearn.ensemble import RandomForestClassifier
import pickle

#read dataset
data=pd.read_csv("dataset.csv")

#input features
x=data[["Glucose","Haemoglobin","Cholesterol"]]

#target
y=data["Disease"]

#train model
model=RandomForestClassifier()
model.fit(x,y)

#save model
with open("Health_model.pkl","wb") as file:
    pickle.dump(model,file)

print("Model trained successfully!")
