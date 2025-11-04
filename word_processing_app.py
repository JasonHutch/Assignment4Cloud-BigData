import streamlit as st

from lib.transformations import Transformations

transformations = Transformations()
st.title("Text Processing Demo")

char_s = st.text_input("Reference String S")
char_t = st.text_input("Input String T")
char_c = st.text_input("Input replacement char C")
if st.button(key='char',label="Perform Word Analysis"):
    num_chars = transformations.Count_num_chars(char_s, char_t)
    freq_chars = transformations.Count_freq_chars(char_t, num_chars)
    replace_chars = transformations.Replace_with_char(char_c,char_t,num_chars)
    
    st.write(num_chars)
    st.write(freq_chars)
    st.write(replace_chars)
    

# word_analysis = st.text_input("Enter String for word analysis")
# if st.button(key='word',label="Perform Word Analysis"):
    

# stop_words = st.text_input("Stop words")
# stop_word_string = st.text_input("Stop word string")
# st.button(
#     key='stop',
#     label="Perform Word Analysis"
# )


