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
    

word_analysis = st.text_input("Enter String for word analysis")
word_analysis_2 = st.text_input("Enter Reference string")
if st.button(key='word',label="Perform Word Analysis"):
    tokens, length = transformations.List_all_words(word_analysis)
    all_words_starting_with = transformations.List_all_starting_with(word_analysis_2, tokens)

    st.write(tokens)
    st.write(length)
    st.write(all_words_starting_with)
    

stop_words = st.multiselect(
    "Select stop words to remove (up to 10)",
    options=["the", "and", "or", "but", "is", "are", "was", "were", "in", "on",
             "at", "by", "for", "with", "about", "of", "to", "from", "as", "it",
             "a", "an", "if", "while", "i", "you", "he", "she", "they", "we"],
    max_selections=10
)
stop_word_string = st.text_input("Enter text to remove stop words from")

if st.button(key='stop', label="Remove Stop Words"):
    if stop_words and stop_word_string:
        result = transformations.Remove_stop_words_custom(stop_words, stop_word_string)

        st.write("**Original Text:**", result['original_text'])
        st.write("**Resulting Text:**", result['resulting_text'])
        st.write("**Stop Words Removed:**", ", ".join(result['stop_words_used']))
        st.write("**Total Occurrences Removed:**", result['removed_count'])
    elif not stop_words:
        st.warning("Please select at least one stop word")
    elif not stop_word_string:
        st.warning("Please enter text to process")


