from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from pydantic import BaseModel, Field
from typing import Literal
from dotenv import load_dotenv

load_dotenv()
model1 = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.1)
model2 = ChatOpenAI(model="gpt-4o")

class Sentiment(BaseModel):
    sentiment: Literal["positive", "negative"] = Field(description="Returns sentiment of the summary either positive or negative")

parser1 = PydanticOutputParser(pydantic_object=Sentiment)
parser2 = StrOutputParser()

# Function to load the news article from a URL
def load_article(url):
    loader = UnstructuredURLLoader(urls=[url])
    documents = loader.load()
    if not documents:
        raise ValueError("No documents found for the provided news article URL.")
    return documents

def news_txt_chunking(news_doc):
    if not news_doc:
        raise ValueError("No news document provided for chunking.")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=100, # maintaining sentence context or context between chunks
        length_function=len
    )
    chunks = text_splitter.split_documents(news_doc)
    return chunks

# summarise the sentiment
def summarise_article(chunk_docs):
    if not chunk_docs:
        raise ValueError("No chunks available for summarization.")
    chain = load_summarize_chain(model1, chain_type="map_reduce")
    summarised_txt = chain.invoke(chunk_docs)
    summary = summarised_txt["output_text"]
    return summary

# find the sentiment of the summary
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
    chain = template | model2 | parser1
    result = chain.invoke({'summary':summary})
    return result.sentiment

# list the sentence that impact the sentiment
def list_sentences_impacting_sentiment(chunk_docs):
    # Create a vector store for the sentences
    if not chunk_docs:
        raise ValueError("No chunks available for sentence extraction.")

    # Extract the text from each document chunk
    chunk_texts = [doc.page_content for doc in chunk_docs]
    
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(chunk_texts, embeddings)
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})

    # Query to retrieve top 5 most impactful sentences for sentiment
    query = "Identify top 5 sentences that have the most impact on the sentiment of the article."
    retrieved = retriever.get_relevant_documents(query)
    impactful_sentences = [doc.page_content for doc in retrieved]

    return [sent.strip() for sent in impactful_sentences if sent.strip()]

# analyse the dominant sentiment of the summarized article
def analyse_dominant_sentiment_statement(summary):
    template = PromptTemplate(
        template="Analyse the given summary and identify which sentence is most reponsible for the overall sentiment of the summary.\n\nSummary:{summary}",
        input_variables=['summary']
    )
    chain = template | model2 | parser2
    result = chain.invoke({'summary':summary})
    return result