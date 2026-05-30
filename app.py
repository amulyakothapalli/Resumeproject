import streamlit as st
import PyPDF2
from docx import Document
import pandas as pd
import plotly.express as px

# ---------------- PAGE SETTINGS ----------------
st.set_page_config(
    page_title="ResumeIQ",
    page_icon="📄",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to right, #0f172a, #1e293b);
    color: white;
}

h1, h2, h3 {
    color: #38bdf8;
}

.score-box {
    padding: 20px;
    border-radius: 15px;
    background-color: #1e293b;
    text-align: center;
    font-size: 30px;
    font-weight: bold;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.title("📄 ResumeIQ - Smart ATS Resume Analyzer")
st.write("Upload your resume and get ATS score, career suggestions, and improvement tips.")

# ---------------- SKILLS DATABASE ----------------
skills_db = {
    "Python": ["python", "flask", "django", "pandas", "numpy"],
    "Web Development": ["html", "css", "javascript", "react", "node"],
    "Machine Learning": ["machine learning", "tensorflow", "keras", "scikit"],
    "Data Science": ["data science", "matplotlib", "seaborn"],
    "Java": ["java", "spring"],
    "Database": ["sql", "mysql", "mongodb"],
    "Cybersecurity": ["cybersecurity", "ethical hacking", "network security"],
    "Cloud": ["aws", "azure", "gcp", "cloud"]
}

# ---------------- DOMAIN MAP ----------------
domain_map = {
    "Python": "Backend Developer",
    "Web Development": "Frontend Developer",
    "Machine Learning": "AI/ML Engineer",
    "Data Science": "Data Analyst",
    "Java": "Java Developer",
    "Database": "Database Engineer",
    "Cybersecurity": "Security Analyst",
    "Cloud": "Cloud Engineer"
}

# ---------------- PDF TEXT EXTRACTOR ----------------
def extract_pdf_text(file):
    text = ""
    pdf_reader = PyPDF2.PdfReader(file)

    for page in pdf_reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted

    return text

# ---------------- DOCX TEXT EXTRACTOR ----------------
def extract_docx_text(file):
    doc = Document(file)
    text = ""

    for para in doc.paragraphs:
        text += para.text + "\n"

    return text

# ---------------- SKILL DETECTION ----------------
def detect_skills(text):
    detected_skills = []
    text = text.lower()

    for category, skills in skills_db.items():
        for skill in skills:
            if skill in text:
                detected_skills.append(category)
                break

    return list(set(detected_skills))

# ---------------- ATS SCORE ----------------
def calculate_ats_score(text, skills):
    score = 0
    suggestions = []

    text_lower = text.lower()

    # Resume Length
    if len(text) > 1000:
        score += 20
    else:
        suggestions.append("Add more content to improve your resume.")

    # Skills
    skill_score = min(len(skills) * 10, 30)
    score += skill_score

    if len(skills) < 3:
        suggestions.append("Add more technical skills.")

    # Projects
    if "project" in text_lower:
        score += 20
    else:
        suggestions.append("Add a projects section.")

    # Education
    if "education" in text_lower:
        score += 10
    else:
        suggestions.append("Include education details clearly.")

    # Experience
    if "experience" in text_lower or "internship" in text_lower:
        score += 20
    else:
        suggestions.append("Add internship or experience section.")

    return min(score, 100), suggestions

# ---------------- COMPANY SUGGESTIONS ----------------
def suggest_companies(skills):
    companies = []

    if "Machine Learning" in skills:
        companies.extend(["Google", "Microsoft", "NVIDIA"])

    if "Web Development" in skills:
        companies.extend(["Infosys", "TCS", "Zoho"])

    if "Cloud" in skills:
        companies.extend(["Amazon", "IBM", "Accenture"])

    if "Cybersecurity" in skills:
        companies.extend(["Cisco", "Palo Alto Networks"])

    return list(set(companies))

# ---------------- FILE UPLOADER ----------------
uploaded_file = st.file_uploader(
    "Upload Your Resume",
    type=["pdf", "docx"]
)

# ---------------- MAIN APP ----------------
if uploaded_file:

    resume_text = ""

    # PDF
    if uploaded_file.name.endswith(".pdf"):
        resume_text = extract_pdf_text(uploaded_file)

    # DOCX
    elif uploaded_file.name.endswith(".docx"):
        resume_text = extract_docx_text(uploaded_file)

    # Display Resume Text
    st.subheader("📜 Extracted Resume Text")

    st.text_area(
        "Resume Content",
        resume_text,
        height=250
    )

    # Detect Skills
    detected_skills = detect_skills(resume_text)

    # ATS Score
    ats_score, suggestions = calculate_ats_score(
        resume_text,
        detected_skills
    )

    # Score Section
    st.subheader("🎯 ATS Score")

    st.markdown(f"""
    <div class='score-box'>
        {ats_score} / 100
    </div>
    """, unsafe_allow_html=True)

    st.progress(ats_score / 100)

    # Resume Strength
    if ats_score >= 80:
        st.success("Strong Resume")
    elif ats_score >= 60:
        st.warning("Average Resume")
    else:
        st.error("Weak Resume")

    # Skills Section
    st.subheader("🛠 Detected Skills")

    if detected_skills:
        for skill in detected_skills:
            st.markdown(f"✅ {skill}")
    else:
        st.warning("No technical skills detected.")

    # Recommended Domains
    st.subheader("💼 Recommended Career Domains")

    recommended_domains = []

    for skill in detected_skills:
        if skill in domain_map:
            recommended_domains.append(domain_map[skill])

    recommended_domains = list(set(recommended_domains))

    if recommended_domains:
        for domain in recommended_domains:
            st.markdown(f"🚀 {domain}")

    # Company Suggestions
    st.subheader("🏢 Suitable Companies")

    companies = suggest_companies(detected_skills)

    if companies:
        for company in companies:
            st.markdown(f"⭐ {company}")
    else:
        st.write("Add more technical skills for company recommendations.")

    # Suggestions
    st.subheader("📌 Resume Improvement Suggestions")

    if suggestions:
        for suggestion in suggestions:
            st.markdown(f"🔹 {suggestion}")
    else:
        st.success("Your resume looks excellent!")

    # Analytics Chart
    st.subheader("📊 Resume Analytics")

    chart_data = pd.DataFrame({
        "Category": ["ATS Score", "Skills"],
        "Value": [ats_score, len(detected_skills) * 10]
    })

    fig = px.bar(
        chart_data,
        x="Category",
        y="Value",
        title="Resume Performance"
    )

    st.plotly_chart(fig)

# ---------------- FOOTER ----------------
st.markdown("---")
st.write("Made with ❤️ using Python & Streamlit")