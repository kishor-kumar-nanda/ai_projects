import streamlit as st
from generate_resume import generate

# Page config must be the first Streamlit command
st.set_page_config(layout="wide")

st.markdown("<h2 style='text-align:center; color:black;'>AI Resume Generator</h2>",unsafe_allow_html=True)
jd_link = st.text_input("Job Description",placeholder="paste your job description link here..")

st.divider()
st.info("Please upload your resume **OR** fill out the form below.")

resume_col = False
form_col = False
resume_data = None

col1, col2, col3 = st.columns([1,0.2,1])

with col1:
    with st.container():
        st.subheader("Upload Resume")
        uploaded_resume = st.file_uploader("Choose a PDF file", type=['pdf'])

        if uploaded_resume is not None:
            resume_col = True
            st.badge("File uploaded successfully", icon=":material/check:", color="green")
            st.success("Thank you.. Feel free to Generate the resume now..")
            
            with open("Resume.pdf", "wb") as file:
                file.write(uploaded_resume.getbuffer())

with col2:
    with st.container():
        st.markdown("""
                    <div style='width:1px; height:180px; background-color:black;margin:auto'></div>
                    <div style='text-align: center; color: grey;margin:auto'>OR</div>
                    <div style='width:1px; height:180px; background-color:black;margin:auto'></div>
                    """, unsafe_allow_html=True)

with col3:
    with st.container():
        st.subheader("Fill the below details")
        with st.form("Candidate details"):
            name = st.text_input("Name:", placeholder="your name")
            email = st.text_input("Email:", placeholder= "your email")
            skills = st.text_input("Skills:", placeholder="your skills (eg: python,nlp)")
            submitted = st.form_submit_button("Submit",use_container_width=True,type="secondary")
            if submitted:
                if not name or not email or not skills:
                    st.error("All fields are mandatory, please fill them and try submitting again..")
                else:
                    form_col = True
                    resume_data = {
                        'name': name,
                        'email': email,
                        'skills': skills
                    }
                    st.badge("Data Submitted", icon=":material/check:", color="green")
                    st.success("Thank you.. Feel free to Generate the resume now..")

# Generate Resume Button
st.text("")
if st.button("Generate Resume", type="primary", use_container_width=True):
    if not jd_link:
        st.error("Please provide a job description link first.")
    elif not (resume_col or form_col):
        st.error("Please either upload a resume or fill out the form first.")
    else:
        try:
            if resume_col and uploaded_resume:
                # Generate from uploaded resume
                resume_txt = generate(jd_link, uploaded_resume)
            elif form_col and resume_data:
                # Generate from form data
                resume_txt = generate(jd_link, resume_data)
            else:
                st.error("Something went wrong. Please try again.")
                resume_txt = None
                
            if resume_txt and not resume_txt.startswith("Error"):
                st.success("Resume Generated..")
                st.text_area("Your New Resume", resume_txt, height=500)
                st.download_button("Download Resume", resume_txt, file_name="new_resume.txt", type="secondary",use_container_width=True)
            else:
                st.error(resume_txt or "Failed to generate resume.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")