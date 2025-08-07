import streamlit as st
from fpdf import FPDF

st.set_page_config(page_title="ATS-Friendly Resume Builder", layout="centered")
st.title("ATS-Friendly Resume Builder")

# ----------------------- Personal Info -----------------------
st.header("Personal Information")
name = st.text_input("Full Name")
job_title = st.text_input("Job Title / Role", placeholder="e.g. Python & Django Developer")
email = st.text_input("Email")
phone = st.text_input("Phone Number")
linkedin = st.text_input("LinkedIn URL")
portfolio = st.text_input("Portfolio URL (Optional)")
github = st.text_input("GitHub URL (Optional)")

# ----------------------- Professional Summary -----------------------
st.header("Professional Summary")
summary = st.text_area("Write your professional summary")

# ----------------------- Education -----------------------
st.header("Education")
edu_degree = st.text_input("Degree")
edu_school = st.text_input("School/College")
edu_year = st.text_input("Year")

# ----------------------- Work Experience -----------------------
st.header("Work Experience (Optional)")
if "experiences" not in st.session_state:
    st.session_state.experiences = []

def add_experience():
    st.session_state.experiences.append({"title": "", "company": "", "duration": "", "desc": ""})

def delete_experience(index):
    if 0 <= index < len(st.session_state.experiences):
        st.session_state.experiences.pop(index)

to_remove_exp = None
for i, exp in enumerate(st.session_state.experiences):
    with st.expander(f"Experience {i+1} (Optional)"):
        exp["title"] = st.text_input("Job Title", value=exp["title"], key=f"exp_title_{i}")
        exp["company"] = st.text_input("Company", value=exp["company"], key=f"exp_company_{i}")
        exp["duration"] = st.text_input("Duration", value=exp["duration"], key=f"exp_duration_{i}")
        exp["desc"] = st.text_area("Job Description", value=exp["desc"], key=f"exp_desc_{i}")
        if st.button("🗑️ Delete", key=f"delete_exp_{i}"):
            to_remove_exp = i
if to_remove_exp is not None:
    delete_experience(to_remove_exp)

st.button("➕ Add Another Experience", on_click=add_experience)

# ----------------------- Projects -----------------------
st.header("Projects (Optional)")
if "projects" not in st.session_state:
    st.session_state.projects = []

def add_project():
    st.session_state.projects.append({"title": "", "desc": "", "link": "", "stack": "", "duration": ""})

def delete_project(index):
    if 0 <= index < len(st.session_state.projects):
        st.session_state.projects.pop(index)

to_remove_proj = None
for i, proj in enumerate(st.session_state.projects):
    with st.expander(f"Project {i+1} (Optional)"):
        proj["title"] = st.text_input("Project Title", value=proj["title"], key=f"project_title_{i}")
        proj["stack"] = st.text_input("Tech Stack", value=proj["stack"], key=f"project_stack_{i}")
        proj["duration"] = st.text_input("Duration", value=proj["duration"], key=f"project_duration_{i}")
        proj["desc"] = st.text_area("Project Description (Use • for bullet points)", value=proj["desc"], key=f"project_desc_{i}")
        proj["link"] = st.text_input("Project Link", value=proj["link"], key=f"project_link_{i}")
        if st.button("🗑️ Delete", key=f"delete_proj_{i}"):
            to_remove_proj = i
if to_remove_proj is not None:
    delete_project(to_remove_proj)

st.button("➕ Add Another Project", on_click=add_project)

# ----------------------- Skills -----------------------
st.header("Skills")
skills = st.text_area("List your skills as bullet points (• Skill A\n• Skill B)")

# ----------------------- Certificates (Optional) -----------------------
st.header("Certificates (Optional)")
if "certificates" not in st.session_state:
    st.session_state.certificates = []

def add_certificate():
    st.session_state.certificates.append({"title": "", "year": ""})

def delete_certificate(index):
    if 0 <= index < len(st.session_state.certificates):
        st.session_state.certificates.pop(index)

to_remove_cert = None
for i, cert in enumerate(st.session_state.certificates):
    with st.expander(f"Certificate {i+1}"):
        cert["title"] = st.text_input("Certificate Title", value=cert["title"], key=f"cert_title_{i}")
        cert["year"] = st.text_input("Year", value=cert["year"], key=f"cert_year_{i}")
        if st.button("🗑️ Delete", key=f"delete_cert_{i}"):
            to_remove_cert = i
if to_remove_cert is not None:
    delete_certificate(to_remove_cert)

st.button("➕ Add Another Certificate", on_click=add_certificate)

# ----------------------- Generate PDF -----------------------
if st.button("Generate Resume (PDF)"):
    pdf = FPDF()
    
    pdf.add_page()

    # 🔤 Add DejaVu font for Unicode support
    pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
    pdf.add_font("DejaVu", "B", "DejaVuSans.ttf", uni=True)
    pdf.add_font("DejaVu", "I", "DejaVuSans.ttf", uni=True)

    # Header
    pdf.set_font("DejaVu", "B", 16)
    pdf.cell(0, 10, name, ln=True)

    pdf.set_font("DejaVu", "I", 13)
    pdf.cell(0, 10, job_title, ln=True)

    pdf.set_font("DejaVu", "", 11)
    contact_line = f"{email} | {phone}"
    pdf.cell(0, 10, contact_line, ln=True)
    links_line = " | ".join(filter(None, [linkedin, portfolio, github]))
    if links_line:
        pdf.multi_cell(0, 10, links_line)
        pdf.ln(2)
        y = pdf.get_y()
        pdf.set_draw_color(0, 0, 0)
        pdf.line(10, y, 200, y)
        pdf.ln(6)


    # Summary
    if summary:
        pdf.set_font("DejaVu", "B", 12)
        pdf.cell(0, 10, "Professional Summary", ln=True)
        pdf.set_font("DejaVu", "", 11)
        pdf.multi_cell(0, 10, summary)
        pdf.ln(4)

    # Education
    if edu_degree or edu_school or edu_year:
        pdf.set_font("DejaVu", "B", 12)
        pdf.cell(0, 10, "Education", ln=True)
        pdf.set_font("DejaVu", "", 11)
        line = f"{edu_degree} – {edu_school}"
        pdf.cell(0, 10, line, ln=False)
        if edu_year:
            pdf.cell(0, 10, f"   {edu_year}", align="R")
        pdf.ln(10)

    # Experience
    if st.session_state.experiences:
        pdf.set_font("DejaVu", "B", 12)
        pdf.cell(0, 10, "Work Experience", ln=True)
        pdf.set_font("DejaVu", "", 11)
        for exp in st.session_state.experiences:
            pdf.set_font("DejaVu", "B", 11)
            header = f"{exp['title']} – {exp['company']}"
            pdf.cell(0, 10, header, ln=False)
            if exp["duration"]:
                pdf.cell(0, 10, f"   {exp['duration']}", align="R")
            pdf.ln(8)
            pdf.set_font("DejaVu", "", 11)
            pdf.multi_cell(0, 10, exp["desc"])
            pdf.ln(2)

   
# Projects
    if st.session_state.projects:
        pdf.set_font("DejaVu", "B", 12)
        pdf.cell(0, 10, "Projects", ln=True)
        pdf.ln(2)
        for proj in st.session_state.projects:
            pdf.set_font("DejaVu", "B", 11)
            if proj['link']:
                pdf.set_text_color(0, 0, 255)
                pdf.cell(0, 10, proj['title'], ln=False, link=proj['link'])
                pdf.ln(2)
            else:
                pdf.set_text_color(0, 0, 0)
                pdf.cell(0, 10, proj['title'], ln=False)
                pdf.ln(2)


        # Stack and duration (aligned)
            pdf.set_text_color(0, 0, 0)
            if proj['stack']:
                pdf.cell(0, 10, f" - {proj['stack']}", ln=False)
            if proj['duration']:
               pdf.cell(0, 10, f"   {proj['duration']}", align="R")

            pdf.ln(8)

        # 📝 Description with bullets
            pdf.set_font("DejaVu", "", 12)
            bullets = proj['desc'].split("•")
            for b in bullets:
                if b.strip():
                    pdf.multi_cell(0, 10, f"• {b.strip()}")

            pdf.ln(4)  # space after each project

    # Skills
    if skills:
        pdf.set_font("DejaVu", "B", 12)
        pdf.cell(0, 10, "Skills", ln=True)
        pdf.set_font("DejaVu", "", 11)
        for line in skills.split("\n"):
            if line.strip():
                pdf.cell(0, 10, line.strip(), ln=True)

        pdf.ln(4) 

    # Certificates
    if st.session_state.certificates:
        pdf.set_font("DejaVu", "B", 12)
        pdf.cell(0, 10, "Certificates", ln=True)
        pdf.set_font("DejaVu", "", 11)
        for cert in st.session_state.certificates:
            line = cert['title']
            if cert['year']:
                line += f" ({cert['year']})"
            pdf.cell(0, 10, line, ln=True)

    pdf.output("resume.pdf")

    with open("resume.pdf", "rb") as file:
        st.download_button("Download Resume", file, "ATS_Resume.pdf", "application/pdf")
