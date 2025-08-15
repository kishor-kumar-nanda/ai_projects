from pypdf import PdfReader
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from typing import List, Optional
from pydantic import BaseModel, Field
import os
import json

load_dotenv()

model = ChatOpenAI(model="gpt-4o", temperature=0.1, max_tokens=1000)

# Function to read PDF and convert it to text
def read_pdf(file_path: str) -> str:
    """Reads a PDF file and extracts its text content."""
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

# schema
class Resume(BaseModel):
    """Pydantic model for a structured resume."""
    name: Optional[str] = Field(default=None, description="The name of the candidate.")
    email: Optional[str] = Field(default=None, description="The email address of the candidate.")
    contact_number: Optional[str] = Field(default=None, description="The phone number of the candidate.")
    github: Optional[str] = Field(default=None, description="The GitHub URL of the candidate.")
    linkedin: Optional[str] = Field(default=None, description="The LinkedIn URL of the candidate.")
    education: Optional[List[str]] = Field(default_factory=list, description="List of educational qualifications.")
    work_experience: Optional[List[str]] = Field(default_factory=list, description="List of work experience details.")
    skills: Optional[List[str]] = Field(default_factory=list, description="List of skills.")
    courses_certifications: Optional[List[str]] = Field(default_factory=list, description="List of courses and certifications.")
    projects: Optional[List[str]] = Field(default_factory=list, description="List of projects.")
    summary: Optional[str] = Field(default=None, description="A brief summary of the resume.")
    achievements: Optional[List[str]] = Field(default_factory=list, description="List of achievements.")

def parse_resume_from_pdf(file_path: str) -> Optional[Resume]:
    """
    Reads a resume from a PDF file, extracts the text, and
    parses it into a structured Pydantic object using a prompt-based approach.
    """
    try:
        # Read text from the PDF file
        resume_text = read_pdf(file_path)
        
        # Use a simple prompt-based approach
        prompt = f"""
        Please parse the following resume text and return a JSON object with the following structure:
        {{
            "name": "candidate name",
            "email": "email address",
            "contact_number": "phone number if available",
            "github": "github url if available",
            "linkedin": "linkedin url if available",
            "education": ["list of educational qualifications"],
            "work_experience": ["list of work experience details"],
            "skills": ["list of skills"],
            "courses_certifications": ["list of courses and certifications"],
            "projects": ["list of projects"],
            "summary": "brief summary",
            "achievements": ["list of achievements"]
        }}
        
        Resume text:
        {resume_text}
        
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
        resume_data = json.loads(response_text)
        
        # Create Resume object
        return Resume(**resume_data)
        
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during parsing: {e}")
        return None

# # Example usage
# if __name__ == "__main__":
#     # Correctly construct the file path using os.path.join
#     file_path = os.path.join(os.getcwd(), "Resume.pdf")
    
#     parsed_resume = parse_resume_from_pdf(file_path)

#     if parsed_resume:
#         # Pydantic's model_dump_json is used to pretty-print the output
#         print(parsed_resume.model_dump_json(indent=2))
        
        
#         print("\nResume parsed successfully.")
#     else:
#         print("Failed to parse resume.")
