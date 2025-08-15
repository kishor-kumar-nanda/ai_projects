import streamlit as st
import pandas as pd
import numpy as np
import time

# Page config must be the first Streamlit command
st.set_page_config(layout="wide")

st.markdown("<h2 style='text-align:center; color:black;'>AI Resume Generator</h2>",unsafe_allow_html=True)
na_link = st.text_input("News Article",placeholder="paste your news article link here..")

sentiment = "positive"

_LOREM_IPSUM = (
    "lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
)


if na_link is not None:
    if st.button("Proceed", use_container_width=True,type="primary"):
        st.divider()
        with st.spinner("Processing...", show_time=True):
            time.sleep(2)
            st.subheader("Summary of New Article")
            st.write(_LOREM_IPSUM)
            st.divider()
            st.subheader("Sentiment Analysis")
            if sentiment is "positive":
                st.success("The article has a **{}** sentiment.".format(sentiment))
            if sentiment is "negative":
                st.error("The article has a **{}** sentiment.".format(sentiment))
            # st.write("The article has a **{}** sentiment.".format(sentiment))
            st.write("Here are the sentences that impact the sentiment:")
            st.write("- Sentence 1: Lorem ipsum dolor sit amet, consectetur adipiscing elit.")
            st.write("- Sentence 2: Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.")
            st.write("- Sentence 3: Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.")
            st.write("The dominant sentiment of the summarized article is **{}**.".format(sentiment))
else:
    st.warning("Please enter a news article link to proceed.")
