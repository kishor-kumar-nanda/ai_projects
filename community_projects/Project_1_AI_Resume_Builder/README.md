# AI Resume Builder

An intelligent resume builder that uses AI to tailor your resume to specific job descriptions. Built with Streamlit, LangChain, and OpenAI.

## Features

- **Resume Upload**: Upload your existing PDF resume for AI-powered analysis
- **Form Input**: Fill out a simple form with your details if you don't have a resume
- **Job Description Analysis**: Extract and analyze job descriptions from URLs
- **AI-Powered Tailoring**: Automatically rewrite experience and skills to match job requirements
- **Smart Matching**: Identify relevant skills and experience from your background
- **Professional Output**: Generate clean, formatted resume text

## Tech Stack

- **Frontend**: Streamlit
- **AI Framework**: LangChain
- **LLM**: OpenAI GPT models
- **PDF Processing**: PyPDF
- **Data Validation**: Pydantic
- **Web Scraping**: Unstructured

## Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd Project_1_AI_Resume_Builder
   ```

2. **Create and activate virtual environment**
   ```bash
   python3 -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

## Usage

1. **Provide Job Description**: Paste a job description URL in the input field
2. **Choose Input Method**:
   - **Option 1**: Upload your existing PDF resume
   - **Option 2**: Fill out the form with your details
3. **Generate Resume**: Click the "Generate Resume" button
4. **Download**: Download your tailored resume as a text file

## Project Structure

```
Project_1_AI_Resume_Builder/
├── app.py                 # Main Streamlit application
├── generate_resume.py     # Core resume generation logic
├── resume_parser.py       # PDF resume parsing and structuring
├── jd_extractor.py        # Job description extraction from URLs
├── template.py            # Resume template and formatting
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## How It Works

1. **Job Description Analysis**: The system extracts key information from job posting URLs using web scraping and AI analysis
2. **Resume Parsing**: If a resume is uploaded, it's parsed using AI to extract structured information
3. **Smart Matching**: The AI identifies relevant skills and experience from your background
4. **Content Tailoring**: Experience descriptions are rewritten to highlight relevance to the job
5. **Output Generation**: A professionally formatted resume is generated with the tailored content

## Requirements

- Python 3.8+
- OpenAI API key
- Internet connection (for job description scraping)

## Notes

- The application requires an active OpenAI API key
- Job description URLs should be publicly accessible
- PDF resumes should be text-based (not scanned images)
- Generated resumes are saved as text files for easy editing

## Troubleshooting

- **"Failed to extract job description"**: Ensure the URL is accessible and contains job posting content
- **"Failed to parse resume"**: Check that your PDF contains extractable text
- **API errors**: Verify your OpenAI API key is valid and has sufficient credits

## Contributing

Feel free to submit issues and enhancement requests!
