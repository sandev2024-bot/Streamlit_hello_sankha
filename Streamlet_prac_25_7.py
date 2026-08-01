import pandas as pd
import streamlit as st
st.title("My first streamlit app")


import pandas as pd
data = pd.DataFrame({'Col1':[1,2],'Col2':[3,4]})
st.write("Here's a DataFrame")
st.dataframe(data)

if st.button('Press Now'):
    st.write('Hello!')

if st.checkbox('Show text'):
    st.write('This text is visible')    

choice = st.radio("Pick one:", ["A", "B", "C"])
st.write(f"You picked {choice}")

option = st.selectbox("Choose an option", ["X", "Y", "Z"])
st.write(f"Option: {option}")

level = st.slider("Select a value", 1, 10)
st.write(f"Selected: {level}")

name = st.text_input("What's your name?")
st.write(f"Hello, {name}!")
age = st.number_input("What's your age?")
st.write(f"Your age is: {age}")
