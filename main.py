from flask import Flask, render_template, request
from PyPDF2 import PdfReader
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

SKILLS = [
    "Communication Skills",
    "Teamwork",
    "Basic Computer Knowledge",
    "Customer Handling",
    "Python",
    "Java",
    "JavaScript",
    "HTML",
    "CSS",
    "Excel",
    "Microsoft Office",
    "Leadership",
    "Problem Solving",
    "Time Management"
]

JOB_ROLES = {
    "Customer Support": [
        "Communication Skills",
        "Customer Handling",
        "Basic Computer Knowledge"
    ],
    "Office Assistant": [
        "Communication Skills",
        "Basic Computer Knowledge",
        "Microsoft Office",
        "Excel"
    ],
    "Team Leader": [
        "Communication Skills",
        "Teamwork",
        "Leadership",
        "Problem Solving"
    ],
    "Python Developer": [
        "Python",
        "Problem Solving",
        "Time Management"
    ],
    "Web Developer": [
        "HTML",
        "CSS",
        "JavaScript",
        "Problem Solving"
    ],
    "General Entry Level": [
        "Communication Skills",
        "Teamwork",
        "Time Management"
    ]
}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    file = request.files.get("resume")
    job_description = request.form.get("job_description", "")

    if not file or file.filename == "":
        return "Please select a resume."

    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)

    try:
        reader = PdfReader(path)

        text = ""

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + " "

    except Exception as e:
        return "Unable to read the PDF: " + str(e)

    text = text.lower()
    job_description = job_description.lower()

    # -----------------------------
    # FIND SKILLS IN RESUME
    # -----------------------------

    found_skills = []

    for skill in SKILLS:
        if skill.lower() in text:
            found_skills.append(skill)

    # -----------------------------
    # FIND MISSING SKILLS
    # -----------------------------

    missing_skills = []

    for skill in SKILLS:
        if skill not in found_skills:
            missing_skills.append(skill)

    # -----------------------------
    # RESUME SCORE
    # -----------------------------

    score = int((len(found_skills) / len(SKILLS)) * 100)

    # -----------------------------
    # STRENGTHS
    # -----------------------------

    strengths = found_skills

    # -----------------------------
    # WEAKNESSES
    # -----------------------------

    weaknesses = missing_skills

    # -----------------------------
    # JOB ROLE MATCH
    # -----------------------------

    job_matches = []

    for role, required_skills in JOB_ROLES.items():

        matched = 0

        for skill in required_skills:
            if skill in found_skills:
                matched += 1

        percentage = int(
            (matched / len(required_skills)) * 100
        )

        job_matches.append({
            "role": role,
            "percentage": percentage
        })

    # -----------------------------
    # JOB DESCRIPTION MATCH
    # -----------------------------

    job_match = None
    job_skills = []
    missing_job_skills = []

    if job_description.strip():

        for skill in SKILLS:

            if skill.lower() in job_description:
                job_skills.append(skill)

        if len(job_skills) > 0:

            matched_job_skills = []

            for skill in job_skills:

                if skill in found_skills:
                    matched_job_skills.append(skill)

            missing_job_skills = [
                skill
                for skill in job_skills
                if skill not in found_skills
            ]

            job_match = int(
                (len(matched_job_skills) / len(job_skills)) * 100
            )

        else:
            job_match = 0

    # -----------------------------
    # AI-STYLE SUGGESTIONS
    # -----------------------------

    suggestions = []

    if score < 50:
        suggestions.append(
            "Add more relevant skills to your resume."
        )

    if score >= 50 and score < 80:
        suggestions.append(
            "Your resume is good, but you can improve your skills section."
        )

    if score >= 80:
        suggestions.append(
            "Your resume has a strong skills profile."
        )

    if missing_skills:
        suggestions.append(
            "Consider learning or adding relevant missing skills."
        )

    if job_match is not None:

        if job_match < 50:
            suggestions.append(
                "Your resume has a low match with this job description."
            )

        elif job_match < 80:
            suggestions.append(
                "Your resume has a moderate match with this job."
            )

        else:
            suggestions.append(
                "Your resume is a strong match for this job."
            )

    # -----------------------------
    # RESULT PAGE
    # -----------------------------

    return render_template(
        "result.html",
        filename=file.filename,
        skills=found_skills,
        missing_skills=missing_skills,
        score=score,
        strengths=strengths,
        weaknesses=weaknesses,
        job_matches=job_matches,
        job_match=job_match,
        job_skills=job_skills,
        missing_job_skills=missing_job_skills,
        suggestions=suggestions
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )
