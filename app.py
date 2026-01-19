import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
import pandas as pd

# Let's get the API Key from the environment
gemini_api_key = os.getenv('GOOGLE_API_KEY1')

# Let's configure the model
model = ChatGoogleGenerativeAI(
    model = 'gemini-2.5-flash-lite',
    api_key = gemini_api_key)

# Design the UI of the application
st.title('🩺 :orange[HealthifyMe:] :blue[Your Personal Health Assistant]')
st.markdown('''This application provides personalized health guidance to help you make better wellness decisions. 
            You can share your health concerns and receive tailored advice based on your needs.''')
tips = '''
Follow these steps:
* Enter your details in the sidebar.
* Rate your Activity & Fitness Level on the scale of 0-5.
* Submit your details.
* Ask your question on the main page.
* Click generate to see your report. 
'''
st.write(f'{tips}')

# Design the sidebar for all the user parameters
st.sidebar.header(':red[ENTER YOUR DETAILS]')
name = st.sidebar.text_input('Enter your name')
gender = st.sidebar.selectbox('Select your gender', ['Male', 'Female'])
age = st.sidebar.text_input('Enter your age')
weight = st.sidebar.text_input('Enter your weight in Kgs')
height = st.sidebar.text_input('Enter your height in cms')
bmi = pd.to_numeric(weight)/((pd.to_numeric(height)/100)**2)
active = st.sidebar.slider('Your daily activity level (0-5)', 0,5, step =1)
fitness = st.sidebar.slider('Your overall fitness level (0-5)', 0,5, step =1)
if st.sidebar.button('Submit'):
    st.sidebar.write(f'{name}, your BMI is {bmi:.2f} Kg/m^2')

# Let's use the Gemini model to generate the report
user_input = st.text_input('Ask me your question.')
prompt = f'''
<Role> You are an expert in health and wellness and have 10+ years experience in guiding people.
<Goal> Generate the customized report addressing the problem the user has asked. 
Here is the question that the user has asked: {user_input}.
<Context> Here are the details that the user has provided.
name = {name}
age = {age}
gender = {gender}
height = {height}
weight = {weight}
bmi = {bmi}
activity rating (0-5) = {active}
fitness rating (0-5) = {fitness}

<Format> Following should be the outline of the report, in the sequence provided.
* Start with the 2-3 line of comment on the details that the user has provided.
* Explain what the real problem could be on the basis of input the user has provided. 
* Suggest the possible reasons for the problem.
* What are the possible solutions.
* Mention the doctor from which specialization can be visited if required.
* Mention any change in the diet which is required.
* In last, create a final summary of all the things that have been discussed
in the report. 

<Instructions> 
* Use bullet points wherever possible.
* Create tables to represent any data wherever possible.
* Strictly do not advise any medicine.
'''

if st.button('Generate'):
    response = model.invoke(prompt)
    st.write(response.content)