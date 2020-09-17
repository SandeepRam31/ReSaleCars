import streamlit as st
import sklearn
import pandas as pd
import numpy as np
import requests
from PIL import Image
from io import BytesIO
import pickle as pkl
import matplotlib.pyplot as plt


st.title('Resale Price Detector')
st.header("Fill the details given below: ")

@st.cache(allow_output_mutation=True)
def load_model():
  with open('./PklFiles/model_2.pkl', 'rb') as f:
    model = pkl.load(f)

  with open('./PklFiles/companies.pkl', 'rb') as f:
    companies = pkl.load(f)

  with open('./PklFiles/color_transform.pkl', 'rb') as f:
    color_transforms = pkl.load(f)

  with open('./PklFiles/model_transform.pkl', 'rb') as f:
    model_transform = pkl.load(f)

  with open('./PklFiles/model_names.pkl', 'rb') as f:
    model_names = pkl.load(f)

  with open('./PklFiles/img_dict.pkl', 'rb') as f:
    image_list = pkl.load(f)

  return model, companies, color_transforms, model_transform, model_names, image_list

with st.spinner('Loading Files....'):
  model, companies, color_transforms, model_transform, model_names, image_list = load_model()

comps = tuple(companies.keys())
model_company = st.selectbox('Which car do you own? ', comps)

model_cars = model_transform[model_company]

model_car_s = []

for i in model_cars:
   model_car_s.append(str(model_company) + ' '+ i)

model_h = st.selectbox('Which model do you own? ', 
                          model_car_s)
                          
mileage = st.slider('Miles Driven: ', min_value = 500, max_value = 100000, step = 500, value = 20000)
mileage = float(mileage)**(1/3)

cols = tuple(color_transforms.keys())
color = st.selectbox('Color: ', cols)

year = st.number_input('Year of Purchase', min_value=1990, max_value=2020, value= 2017, step=1)
age = 2020 - int(year)

model_owned = model_h.split(' ')
name = ''

for i in model_owned[1:]:
  name += i 

name = name.rstrip()

model_owned = model_names.index(name)
encode_company = companies[model_company]
encode_color = color_transforms[color]

encode_company = [int(i) for i in encode_company]
encode_color = [int(i) for i in encode_color]

X = [model_owned, age, mileage]

X += encode_company
X += encode_color

cols = ['model', 'year', 'mileage', 'Audi', 'Chevrolet', 'Chrysler', 'Dodge', 'Ford',
        'Honda', 'Hyundai', 'Kia', 'Mitsubishi',
        'Nissan', 'Tesla', 'Toyota', 'Volvo', 'Beige', 'Black', 'Blue',
        'Brilliant Silver', 'Brown', 'Burgundy', 'Gray', 'Green', 'Metallic',
        'N/A', 'Orange', 'Other', 'Red', 'Silver', 'White']

X = pd.DataFrame(np.array([X]), columns = cols)

with st.spinner('Predicting....'):
  label = model.predict(X)[0]

st.markdown('**Price of your car is **' ) 
st.write('$ ', np.floor(np.exp(label)))

st.write('')

try:
  model_x = model_h.split(' ')[1:]
  string = ''
  for part in model_x:
    string += part

  inde = model_names.index(string)
  url = image_list['image'][inde]
  response = requests.get(url)
  img = Image.open(BytesIO(response.content))
  with st.spinner('Getting image...'):
    st.image(img, caption = string, width = 320)
   
except:
  with st.spinner('Fining image...'):
    pass

