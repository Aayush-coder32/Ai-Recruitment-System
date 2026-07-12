import json
from utils.gemini import ask_gemini
from models.schemas import JobDescription


def parse_job_description(job: JobDescription) -> dict:
    prompt = f"""
You are an expert technical recruiter. Analyze the job description below and extract the requirements into a structured JSON format.

Job Title: {job.title}
Job Description: {job.description}

Return ONLY a valid JSON object with exactly this structure (no extra text, no markdown, no explanation):
{{
    "required_skills": ["skill1", "skill2"],
    "preferred_skills": ["skill1", "skill2"],
    "minimum_experience_years": 0,
    "education_fields": ["Computer Science", "Engineering"],
    "education_level": "Bachelor's",
    "employment_type": "Full-time",
    "seniority_level": "Mid",
    "key_responsibilities": ["responsibility1", "responsibility2"]
}}

Rules:
- required_skills: skills explicitly stated as required or must-have
- preferred_skills: skills stated as nice-to-have, bonus, or preferred
- minimum_experience_years: the minimum number of years of experience required (use 0 if not mentioned)
- education_fields: relevant fields of study (use empty list if not mentioned)
- education_level: one of "High School", "Bachelor's", "Master's", "PhD", or "Any"
- employment_type: one of "Full-time", "Part-time", "Contract", or "Any"
- seniority_level: one of "Junior", "Mid", "Senior", "Lead", or "Any"
- key_responsibilities: main responsibilities listed in the job description
"""

    response = ask_gemini(prompt)

    try:
        response = response.strip()
        if response.startswith("```"):
            response = response.split("```")[1]
            if response.startswith("json"):
                response = response[4:]
        parsed = json.loads(response)
        return parsed
    except json.JSONDecodeError:
        return {
            "required_skills": [],
            "preferred_skills": [],
            "minimum_experience_years": 0,
            "education_fields": [],
            "education_level": "Any",
            "employment_type": "Any",
            "seniority_level": "Any",
            "key_responsibilities": []
        }