from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import UnstructuredURLLoader
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import Literal, Optional
import json

load_dotenv()

model = ChatOpenAI()

# Function to fetch job description from a URL
def fetch_jd(jd_url):
    loader = UnstructuredURLLoader(urls=[jd_url])
    documents = loader.load()
    if not documents:
        raise ValueError("No documents found for the provided URL.")
    # print(documents.page_content)
    return documents[0].page_content

# schema for the job description extractor
class JD_Extractor(BaseModel):
    summary: Optional[str] = Field(description="A brief summary of the job description and key things the job decription is looking for.")
    job_role: str = Field(description="Job role of the Job Description")
    company_name: str = Field(description="Company name of the Job Description")
    location: Optional[str] = Field(description="Location the JD is expecting for.")
    tech_skills: list[str] = Field(description="Technical skills required for the Job Description")
    qualifications: list[str] = Field(description="Qualifications required for the Job Description.")
    experience: list[str] = Field(description="Experience required for the JD. Eg: 5+ years of experience in Python, 3+ years of experience in ML etc.")

def extract_jd_from_url(jd_url: str):
    try:
        # Fetch the job description content
        jd_content = fetch_jd(jd_url)
        
        # Use a prompt-based approach
        prompt = f"""
        Please analyze the following job description and return a JSON object with the following structure:
        {{
            "summary": "brief summary of the job description and key requirements",
            "job_role": "job role/title",
            "company_name": "company name",
            "location": "job location if specified",
            "tech_skills": ["list of technical skills required"],
            "qualifications": ["list of qualifications required"],
            "experience": ["list of experience requirements"]
        }}
        
        Job Description:
        {jd_content}
        
        Return only the JSON object, no additional text.
        """
        
        response = model.invoke(prompt)
        response_text = response.content.strip()
        
        # Try to extract JSON from the response
        if response_text.startswith('```json'):
            response_text = response_text[7:-3]  # Remove ```json and ``` markers
        elif response_text.startswith('```'):
            response_text = response_text[3:-3]  # Remove ``` markers
        
        # Parse the JSON response
        jd_data = json.loads(response_text)
        
        # Create JD_Extractor object
        return JD_Extractor(**jd_data)
        
    except Exception as e:
        print(f"Error extracting job description: {e}")
        return None

