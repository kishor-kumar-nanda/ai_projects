import streamlit as st
import pandas as pd
import numpy as np
import time
from functions import load_article, news_txt_chunking, summarise_article, list_sentences_impacting_sentiment, analyse_dominant_sentiment_statement, find_sentiment_of_summary

st.set_page_config(layout="wide")

st.markdown("<h2 style='text-align:center; color:black;'>News Sentiment Analyser</h2>",unsafe_allow_html=True)
na_link = st.text_input("News Article",placeholder="paste your news article link here..")

sentiment = "None"

if st.button("Proceed", use_container_width=True, type="primary"):
    if not na_link:
        st.warning("Please enter a news article link to proceed.")
    else:
        st.divider()
        with st.status("Processing Article..", expanded=True) as status:
            # Step 1: Load and Chunk the document once
            st.write("1. Loading and chunking article..")
            try:
                news_doc = load_article(str(na_link))
                chunk_docs = news_txt_chunking(news_doc)
                status.update(label="Document Loaded and Chunked!", state="running")
            except Exception as e:
                st.error(f"Error loading article: {e}")
                status.update(label="Failed to process article", state="error")
                st.stop()
            
            # Step 2: Summarize the article
            st.write("2. Summarizing article..")
            na_summary = summarise_article(chunk_docs)
            status.update(label="Summarization Completed!", state="running")

            # Step 3: Find sentences that impact sentiment
            st.write("3. Identifying impactful sentences..")
            impactful_sentences = list_sentences_impacting_sentiment(chunk_docs)
            status.update(label="Identification Completed!", state="running")

            # Step 4: Find sentiment and dominant statement
            st.write("4. Determining dominant sentiment and statement..")
            sentiment = find_sentiment_of_summary(na_summary)
            dom_statement = analyse_dominant_sentiment_statement(na_summary)
            status.update(label="All tasks completed!", state="complete", expanded=False)

        # Display results
        st.divider()
        st.subheader("Summary of New Article")
        st.write(na_summary)

        st.divider()
        st.subheader("Sentiment Analysis")
        if sentiment == "positive":
            st.success(f"The article has a **{sentiment}** sentiment.")
        elif sentiment == "negative":
            st.error(f"The article has a **{sentiment}** sentiment.")

        st.divider()
        st.subheader("Dominant Statement")
        st.write(dom_statement)

        st.divider()
        st.subheader("Sentences That Impact the Sentiment")
        for i, sent in enumerate(impactful_sentences, 1):
            st.write(f"- Sentence {i}: {sent}")
else:
    st.warning("Please enter a news article link to proceed.")
