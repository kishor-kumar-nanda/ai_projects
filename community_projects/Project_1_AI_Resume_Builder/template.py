import textwrap
from pydantic import BaseModel, Field
from typing import List, Optional

class ContactInfo(BaseModel):
    phone: str
    email: str
    linkedin: Optional[str] = Field(default=None)
    github: Optional[str] = Field(default=None)
    website: Optional[str] = Field(default=None)

class JobExperience(BaseModel):
    title: str
    company: str
    location: str
    dates: str
    description: List[str] = Field(description="A list of bullet points describing responsibilites and achievements.")

class Education(BaseModel):
    degree: str
    university: str
    location: str
    dates: Optional[str]
    gpa: Optional[str]

class Resume(BaseModel):
    name: str
    contact: ContactInfo
    summary: str
    skills: List[str]
    experience: List[JobExperience]
    education: List[Education]

def generate_resume(resume_data: Resume) -> str:
    lines = []

    # Header
    lines.append(f"{resume_data.name.upper():^80}")
    lines.append("-" * 80)
    contact_line = f"{resume_data.contact.phone} | {resume_data.contact.email}"
    if resume_data.contact.linkedin:
        contact_line += f" | LinkedIn: {resume_data.contact.linkedin}"
    if resume_data.contact.github:
        contact_line += f" | Github: {resume_data.contact.github}"
    lines.append(f"{contact_line:^80}")
    lines.append("-" * 80)
    lines.append("")

    # Summary
    lines.append("Summary")
    lines.append("=" * 7)
    lines.append(textwrap.fill(resume_data.summary, width=80))
    lines.append("")
    
    # Skills
    lines.append("Skills")
    lines.append("=" * 6)
    lines.append(textwrap.fill(", ".join(resume_data.skills)))
    lines.append("")

    # Experience
    lines.append("Experience")
    lines.append("=" * 9)
    # lines.append(textwrap.fill(resume_data.experience, width=80))
    for job in resume_data.experience:
        lines.append(f"{job.title:<60}{job.dates:>20}")
        lines.append(f"{job.company}, {job.location}")
        for bullet in job.description:
            lines.append(f" - {textwrap.fill(bullet, width=78, subsequent_indent='  ')}")
        lines.append("")

    # Education
    lines.append("Education")
    lines.append("=" * 9)
    for edu in resume_data.education:
        lines.append(f"{edu.degree:<60}{edu.dates:>20}")
        lines.append(f"{edu.university}, {edu.location}")
        if edu.gpa:
            lines.append(f"GPA: {edu.gpa}")
        lines.append("")

    return "\n".join(lines)

def save_resume(resume_content: str, filename: str):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(resume_content)
    print(f"Resume saved to {filename}")

def get_data(resume, new_summary, skills, experience):
    # Convert experience (list of strings) to list of JobExperience objects (basic stub)
    job_experiences = []
    if experience:
        for exp in experience:
            if isinstance(exp, str) and exp.strip():
                job_experiences.append(JobExperience(
                    title="Relevant Experience",
                    company="Company",
                    location="Location",
                    dates="Present",
                    description=[exp]
                ))
    
    # If no experience provided, create a placeholder
    if not job_experiences:
        job_experiences.append(JobExperience(
            title="Experience",
            company="Company",
            location="Location",
            dates="Present",
            description=["Experience details will be tailored based on job description."]
        ))

    # Convert education (list of strings) to list of Education objects (basic stub)
    educations = []
    if hasattr(resume, 'education') and resume.education:
        for edu in resume.education:
            if isinstance(edu, str) and edu.strip():
                educations.append(Education(
                    degree=edu,
                    university="University",
                    location="Location",
                    dates="Present",
                    gpa=None
                ))
    
    # If no education provided, create a placeholder
    # if not educations:
    #     educations.append(Education(
    #         degree="Education",
    #         university="University",
    #         location="Location",
    #         dates="Present",
    #         gpa=None
    #     ))

    name = getattr(resume, 'name', 'N/A')
    contact_number = getattr(resume, 'contact_number', 'N/A')
    email = getattr(resume, 'email', 'N/A')
    linkedin = getattr(resume, 'linkedin', None)
    github = getattr(resume, 'github', None)

    # Ensure skills is a list
    if isinstance(skills, str):
        skills = [skill.strip() for skill in skills.split(',') if skill.strip()]
    elif not skills:
        skills = ["Skills will be tailored based on job description."]

    resume_data = Resume(
        name=name,
        contact=ContactInfo(
            phone=contact_number,
            email=email,
            linkedin=linkedin,
            github=github
        ),
        summary=new_summary,
        skills=skills,
        experience=job_experiences,
        education=educations
    )
    content = generate_resume(resume_data)
    save_resume(content, "generated_resume.txt")
    return content


