#This file is for predicting the note of the team mebers based on the average score they have,
#This mnodel will make use of already existing data to cretae the respective parameters

#Library import
import json 

def get_params(path) :
    with open(path, 'r') as file:
        data = json.load(file)

    b, m = [data['data']['b'], data['data']['m']]

    return b, m

#Prediction function, it just return a basic linear funnction prediction on x as a output
def get_prediction(b, m, x):
    return b + m*x

def get_score(x):
    b, m = get_params('Data_proccess/dataset.json')
    score = get_prediction(b, m, x)

    return round(score, 2)

