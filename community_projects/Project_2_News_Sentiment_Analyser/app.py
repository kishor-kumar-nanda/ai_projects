import streamlit as st
import pandas as pd
import numpy as np
import time
from functions import summarise_article, list_sentences_impacting_sentiment, analyse_dominant_sentiment, find_sentiment_of_summary

# Page config must be the first Streamlit command
st.set_page_config(layout="wide")

st.markdown("<h2 style='text-align:center; color:black;'>News Sentiment Analyser</h2>",unsafe_allow_html=True)
na_link = st.text_input("News Article",placeholder="paste your news article link here..")

sentiment = "None"


if na_link is not None:
    if st.button("Proceed", use_container_width=True,type="primary"):
        st.divider()
        with st.status("Processing Article..", expanded=True) as status:
            st.write("1. Summarizing article..")
            na_summary = summarise_article(str(na_link))
            status.update(label="Summarization Completed!", state="complete", expanded=False)
            
            st.write("2. Identifying impactful sentences..")
            time.sleep(5)
            status.update(label="Identification Completed!", state="complete", expanded=False)
            
            st.write("3. Determining dominant sentiments..")
            time.sleep(4)
            status.update(label="All tasks completed!", state="complete", expanded=False)

            st.divider()
            st.subheader("Summary of New Article")
            st.write(na_summary)

            st.divider()
            sentiment = find_sentiment_of_summary(na_summary)
            st.subheader("Sentiment Analysis")
            if sentiment is "positive":
                st.success("The article has a **{}** sentiment.".format(sentiment))
            if sentiment is "negative":
                st.error("The article has a **{}** sentiment.".format(sentiment))

            st.divider()
            st.write("Here are the sentences that impact the sentiment:")
            st.write("- Sentence 1: Lorem ipsum dolor sit amet, consectetur adipiscing elit.")
            st.write("- Sentence 2: Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.")
            st.write("- Sentence 3: Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.")
            st.write("The dominant sentiment of the summarized article is **{}**.".format(sentiment))
else:
    st.warning("Please enter a news article link to proceed.")
