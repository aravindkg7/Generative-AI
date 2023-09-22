#This code is based on an online course on Buiding WebApps with Streamlit by Andrei Dumitrescu (Crystal Mind Academy)
import streamlit as st
import pandas as pd

st.title("Hello Streamlit :smile:")

#Writing text on the screen
st.write("We are learning Streamlit")

df = pd.DataFrame({"First_Column":[1, 2, 3, 4, 5],
                   "Second_Column":['a','b','c','d','e']})

#Writing objects on the screen using Magic
df

#Widgets
#Text Input

name = st.text_input('Please enter your name: ')
if name:
    st.write(f'Hello {name}')

st.divider()

#Numerical Input
number = st.number_input('Enter a number:', min_value=1, max_value=100, step=1)
st.write(f'Your entered {number}')

st.divider()

#Buttons
clicked = st.button("Click here")
if clicked:
    st.write("Great!!!!, you did it")

st.divider()

#Checkbox
agree = st.checkbox("I agree")
if agree:
    'Good, that you agreed'

checked = st.checkbox('Continue', value=True)
if checked:
    ":+1:" * 10

df = pd.DataFrame({"First_Column":[1, 2, 3, 4, 5],
                   "Second_Column":['a','b','c','d','e']})

if st.checkbox("Show Data"):
    df

st.divider()

#Radio button
pets = ['cat', 'dog', 'rabbit', 'cows', 'hen']

pet = st.radio("Favourite pet", pets)
st.write(f'Your favourite pet is: {pet}')

st.divider()

#Select 
cities = ['Bengaluru', 'Mumbai', 'Chennai', 'Hyderabad']
city = st.selectbox('Your city:',cities)
st.write(f'You live in {city}')

st.divider()

#Slider
slide = st.slider('x', value=10, min_value=0, max_value=100, step=5)
st.write(f'The value is {slide}')

st.divider()

#File Uploader
file = st.file_uploader("Upload a file:", type=['txt','csv','pdf','xlsx','docx'])
if file:
    st.write(file)
    if file.type == 'text/plain':
      from io import StringIO
      stringIO = StringIO(file.getvalue().decode('utf-8'))
      string_data = stringIO.read()
      st.write(string_data)
    elif file.type == 'text/csv':
        import pandas as pd
        df = pd.read_csv(file)
        df
    elif file.type == 'text/excel':
        import pandas as pd
        df = pd.read_excel(file)
        df
    else:
        pass

#Camera Input
photo = st.camera_input("Take a photo:")
if photo:
    st.image(photo)


#Sidebar

selectbox = st.sidebar.selectbox("Countries:",['IN','NL','FR','RU'])
slider = st.sidebar.slider("Temperature", min_value=0, value=10, max_value=50)

#Columns

left_column, right_column = st.columns(2)

import random
data = [random.random() for _ in range(100)]

with left_column:
    st.subheader("Line chart")
    st.line_chart(data)

right_column.subheader("Data")
right_column.write(data[:10])

col1, col2, col3 = st.columns([0.2, 0.5, 0.3])

col1.markdown(" Streamlit ")
col2.write(data[:5])
col3.write(data[95:])

#Expander

with st.expander("Click to Expand:")
st.bar_chart({'Data':[random.randint(2, 10) for _ in range(25)]})

#Progress bar
import time

st.write("Starting an extensive computation...")
latest_iteration = st.empty()

progress_text = 'Operation in progress!!! Please wait ...'
my_bar = st.progress(0, text=progress_text)
time.sleep(2)

for i in range(100):
    my_bar.progress(i+1)
    latest_iteration.text(f'Iteration {i+1}')
    time.sleep(0.2)

st.write('Done!!!')


#Session State

st.subheader("Session State")
st.write(st.session_state)

if 'counter' not in st.session_state:
    st.session_state['counter'] = 0
else:
    st.session_state['counter'] += 1

st.write(f'Counter value: {st.session_state.counter}')


button = st.button('Update State')
if 'clicks' not in st.session_state:
    st.session_state['clicks'] = 0

if button:
    st.session_state['clicks'] += 1
    st.write(f'After clicking the button {st.session_state}')