# 📰 News Sentiment Analyzer

A powerful web application that analyzes news articles to determine their sentiment and extract key insights using NLP techniques including OpenAI embeddings for RAG operations and summarization.

## 🚀 Features

- **Article Loading**: Automatically loads and processes news articles from URLs
- **Chunking**: Breaks down articles into manageable chunks while preserving context
- **AI-Powered Summarization**: Generates concise summaries using GPT-3.5-turbo
- **Sentiment Analysis**: Determines whether articles have positive or negative sentiment
- **Impactful Sentence Extraction**: Identifies the top 5 sentences that most influence the article's sentiment
- **Dominant Statement Analysis**: Pinpoints the sentence most responsible for the overall sentiment
- **Modern Web Interface**: Built with Streamlit for an intuitive user experience

## 🛠️ Technology Stack

- **Backend**: Python 3.x
- **AI/ML**: OpenAI GPT models (GPT-3.5-turbo, GPT-4o)
- **Framework**: LangChain for AI workflow orchestration
- **Frontend**: Streamlit for web interface
- **Vector Database**: FAISS for semantic search
- **Text Processing**: UnstructuredURLLoader for document loading
- **Environment**: Python-dotenv for configuration management

## 📋 Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Internet connection for API calls

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/kishor-kumar-nanda/ai_projects.git
   cd community_projects/Project_2_News_Sentiment_Analyser
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root and add your OpenAI API key:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## 🎯 Usage

1. **Start the application**
   ```bash
   streamlit run app.py
   ```

2. **Open your browser** and navigate to the provided local URL (usually `http://localhost:8501`)

3. **Enter a news article URL** in the text input field (used article to test: https://www.empireonline.com/tv/hardware/best-soundbars/)

4. **Click "Proceed"** to analyze the article

5. **View the results**:
   - Article summary
   - Sentiment analysis (positive/negative)
   - Dominant statement
   - Top 5 impactful sentences

## 🔧 How It Works

1. **Document Loading**: Uses `UnstructuredURLLoader` to fetch and parse news articles
2. **Text Chunking**: Splits articles into 1500-character chunks with 100-character overlap
3. **Summarization**: Employs LangChain's map-reduce chain with GPT-3.5-turbo
4. **Sentiment Analysis**: Uses GPT-4o to classify sentiment as positive or negative
5. **Impact Analysis**: Leverages FAISS vector database to find semantically relevant sentences
6. **Dominant Statement**: Identifies the most sentiment-influential sentence

## 📁 Project Structure

```
Project_2_News_Sentiment_Analyser/
├── app.py              # Main Streamlit application
├── functions.py        # Core AI and processing functions
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (create this)
└── README.md          # This file
```

## 🔑 API Requirements

- **OpenAI API Key**: Required for GPT model access
- **Rate Limits**: Be aware of OpenAI's rate limiting policies
- **Costs**: API usage incurs costs based on token consumption

## 🚧 Limitations

- Requires valid news article URLs
- Processing time depends on article length and API response times
- Sentiment analysis accuracy depends on the quality of the source content
- Internet connection required for both article fetching and API calls


## 🙏 Acknowledgments

- OpenAI for providing the GPT models
- LangChain team for the excellent framework
- Streamlit for the web application framework
- FAISS for efficient similarity search

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/kishor-kumar-nanda/ai_projects/issues) page
2. Create a new issue with detailed information
3. Ensure you've followed the installation and setup steps


**Made with ❤️ using AI and NLP technologies**
