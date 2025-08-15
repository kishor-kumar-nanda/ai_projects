from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import UnstructuredURLLoader
from dotenv import load_dotenv
from jd_extractor import extract_jd_from_url
from resume_parser import parse_resume_from_pdf
from template import generate_resume, save_resume, get_data
import tempfile
import os
from pydantic import BaseModel, Field
from typing import List, Optional

load_dotenv()

def summary_for_jd(experience, skills, extracted_jd, resume_summary):
    model = ChatOpenAI(model="gpt-4o", temperature=0.1, max_tokens=1000)
    jd_summary = extracted_jd.summary
    jd_tech_skills = extracted_jd.tech_skills
    jd_qualifications = extracted_jd.qualifications
    jd_experience = extracted_jd.experience
    template = PromptTemplate(
        template="""
        Generate a concise resume summary (30-50 words, 2-3 sentences) in a professional, slightly formal tone, highlighting the candidate’s most relevant skills and experiences from {relevant_skills} and {relevant_experience} that align with {jd_summary}, {jd_tech_skills}, {jd_qualifications}, and {jd_experience}. If the resume and job description misalign, tweak the {resume_summary} to emphasize transferable skills or partial matches that align with the job description. Include a mix of technical skills, soft skills, and qualifications, incorporating keywords from the job description where relevant.
        """,
        input_variables=["relevant_skills","relevant_experience","jd_summary","jd_tech_skills","jd_qualifications","jd_experience"]
    )
    prompt = template.invoke({
        'relevant_skills': skills,
        'relevant_experience': experience,
        'jd_summary': jd_summary,
        'jd_tech_skills': jd_tech_skills,
        'jd_qualifications': jd_qualifications,
        'jd_experience': jd_experience,
        'resume_summary': resume_summary
    })
    # prompt_str = prompt.format(jd_summary=jd_summary, experience=experience)
    return model.invoke(prompt).content

# compares the skills and experience of resume with JD
def relevance_resume(resume, jd):
    try:
        jd_skills = set([skill.lower() for skill in (jd.tech_skills or [])])
        
        # Safely get resume skills with fallback
        skills = getattr(resume, 'skills', [])
        filtered_skills = [skill for skill in skills if skill.lower() in jd_skills]
        
        # Safely get resume work experience with fallback
        resume_experience = getattr(resume, 'work_experience', []) or []
        filtered_experience = []
        for exp in resume_experience:
            if any(skill in exp.lower() for skill in jd_skills):
                filtered_experience.append(exp)
        
        # Update resume object safely
        if hasattr(resume, 'skills'):
            resume.skills = filtered_skills or skills
        if hasattr(resume, 'work_experience'):
            resume.work_experience = filtered_experience or resume_experience
            
        return resume
    except Exception as e:
        print(f"Error in relevant_experience: {e}")
        return resume


def generate(url, resume_input):
    try:
        # Validate URL input
        if not url or not url.strip():
            return "Error: Please provide a valid job description URL."

        # jd extraction from url
        extracted_jd = extract_jd_from_url(jd_url=url)
        if not extracted_jd:
            return "Failed to extract job description."

        # Always treat resume_input as a local file path
        parsed_resume = parse_resume_from_pdf(resume_input)
        if not parsed_resume:
            return "Failed to parse resume."

        # jd summary
        jd_summary = extracted_jd.summary

        rel_resume = relevance_resume(parsed_resume, extracted_jd)

        req_exp = ""
        if rel_resume.work_experience:
            for exp in rel_resume.work_experience:
                req_exp += "".join(exp.splitlines())

            tailored_summary = summary_for_jd(req_exp, rel_resume.skills, extracted_jd, parsed_resume.summary)
        else:
            tailored_summary = jd_summary or ""

        result = get_data(parsed_resume, tailored_summary, rel_resume.skills, rel_resume.work_experience)

        return result

    except Exception as e:
        return f"Error during resume generation: {e}"

# url = "https://jobs.apple.com/en-in/details/200600739-1052/aiml-annotation-team-lead-hyderabad?team=MLAI"
# resume_input = os.getcwd() + "/community_projects/Project_1_AI_Resume_Builder/Resume.pdf"
# generate(url, resume_input)