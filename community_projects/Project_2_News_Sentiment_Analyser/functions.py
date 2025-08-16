from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import Literal
from dotenv import load_dotenv

load_dotenv()
model1 = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.1)
model2 = ChatOpenAI(model="gpt-4o")

summary = ""

class Sentiment(BaseModel):
    sentiment: Literal["positive", "negative"] = Field(description="Returns sentiment of the summary either positive or negative")

parser = PydanticOutputParser(pydantic_object=Sentiment)

def load_article(url):
    loader = UnstructuredURLLoader(urls=[url])
    documents = loader.load()
    if not documents:
        raise ValueError("No documents found for the provided news article URL.")
    # print(documents[0].page_content)
    return documents

def news_txt_chunking(news_doc):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=100, # maintaining sentence context or context between chunks
        length_function=len
    )
    return text_splitter.split_documents(news_doc)

# summarise the sentiment
def summarise_article(news_article):
    news_doc = load_article(news_article)
    chunk_docs = news_txt_chunking(news_doc)

    chain = load_summarize_chain(model1, chain_type="map_reduce")
    summarised_txt = chain.invoke(chunk_docs)
    summary = summarised_txt["output_text"]
    return summary

def find_sentiment_of_summary(summary):
    template = PromptTemplate(
        template=(
            "Give me the sentiment of the below given summary as a JSON object with the key 'sentiment' "
            "and value either 'positive' or 'negative'.\n\n"
            "Summary: {summary}\n\n"
            "Respond ONLY with a JSON object, e.g. {{\"sentiment\": \"positive\"}}"
        ),
        input_variables=['summary']
    )
    chain = template | model2 | parser
    result = chain.invoke({'summary':summary})
    return result.sentiment

# list the sentence that impact the sentiment
def list_sentences_impacting_sentiment(news_article):
    pass

# analyse the dominant sentiment of the summarized article
def analyse_dominant_sentiment(news_article):
    pass
