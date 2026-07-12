from models.schemas import TalentProfile


SKILL_LEVEL_WEIGHTS = {
    "Beginner": 0.25,
    "Intermediate": 0.5,
    "Advanced": 0.75,
    "Expert": 1.0
}


def calculate_evidence_multiplier(candidate: TalentProfile) -> float:
    evidence_score = 0
    max_evidence = 4

    if candidate.socialLinks:
        if candidate.socialLinks.github:
            evidence_score += 1
        if candidate.socialLinks.portfolio:
            evidence_score += 1

    projects_with_links = [p for p in candidate.projects if p.link]
    if projects_with_links:
        evidence_score += 1

    if candidate.certifications and len(candidate.certifications) > 0:
        evidence_score += 1

    ratio = evidence_score / max_evidence

    if ratio >= 0.75:
        return 1.0
    elif ratio >= 0.4:
        return 0.85
    else:
        return 0.70


def score_skills(candidate: TalentProfile, job_requirements: dict) -> float:
    required_skills = [s.lower() for s in job_requirements.get("required_skills", [])]
    preferred_skills = [s.lower() for s in job_requirements.get("preferred_skills", [])]

    if not required_skills and not preferred_skills:
        return 22.5

    candidate_skills = {s.name.lower(): s for s in candidate.skills}

    required_score = 0
    required_max = 35

    if required_skills:
        per_skill = required_max / len(required_skills)
        for skill in required_skills:
            if skill in candidate_skills:
                level = candidate_skills[skill].level.value
                weight = SKILL_LEVEL_WEIGHTS.get(level, 0.5)
                years = candidate_skills[skill].yearsOfExperience or 0
                year_bonus = min(years / 10, 0.2)
                required_score += per_skill * (weight + year_bonus)

    preferred_score = 0
    preferred_max = 10

    if preferred_skills:
        per_skill = preferred_max / len(preferred_skills)
        for skill in preferred_skills:
            if skill in candidate_skills:
                level = candidate_skills[skill].level.value
                weight = SKILL_LEVEL_WEIGHTS.get(level, 0.5)
                preferred_score += per_skill * weight

    total = min(required_score + preferred_score, 45)
    return round(total, 2)


def score_projects(candidate: TalentProfile, job_requirements: dict) -> float:
    if not candidate.projects:
        return 0.0

    required_skills = [s.lower() for s in job_requirements.get("required_skills", [])]
    preferred_skills = [s.lower() for s in job_requirements.get("preferred_skills", [])]
    all_relevant_skills = set(required_skills + preferred_skills)

    total_score = 0
    max_per_project = 25 / max(len(candidate.projects), 1)
    max_per_project = min(max_per_project, 10)

    for project in candidate.projects:
        project_score = 0
        project_techs = [t.lower() for t in (project.technologies or [])]

        if all_relevant_skills:
            matches = len(set(project_techs) & all_relevant_skills)
            relevance = min(matches / max(len(all_relevant_skills), 1), 1.0)
            project_score += max_per_project * 0.6 * relevance
        else:
            project_score += max_per_project * 0.3

        if project.link:
            project_score += max_per_project * 0.3

        if project.description and len(project.description) > 30:
            project_score += max_per_project * 0.1

        total_score += project_score

    return round(min(total_score, 25), 2)


def score_experience(candidate: TalentProfile, job_requirements: dict) -> float:
    if not candidate.experience:
        return 0.0

    min_years = job_requirements.get("minimum_experience_years", 0)
    required_skills = [s.lower() for s in job_requirements.get("required_skills", [])]
    seniority = job_requirements.get("seniority_level", "Any").lower()

    total_months = 0
    for exp in candidate.experience:
        try:
            start_parts = exp.startDate.split("-")
            start_year, start_month = int(start_parts[0]), int(start_parts[1])

            if exp.isCurrent or not exp.endDate or exp.endDate.lower() == "present":
                from datetime import datetime
                now = datetime.now()
                end_year, end_month = now.year, now.month
            else:
                end_parts = exp.endDate.split("-")
                end_year, end_month = int(end_parts[0]), int(end_parts[1])

            months = (end_year - start_year) * 12 + (end_month - start_month)
            total_months += max(months, 0)
        except:
            continue

    total_years = total_months / 12

    if min_years > 0:
        experience_ratio = min(total_years / min_years, 1.5)
    else:
        experience_ratio = min(total_years / 3, 1.0)

    experience_score = min(experience_ratio * 10, 12)

    tech_bonus = 0
    if required_skills:
        all_exp_techs = []
        for exp in candidate.experience:
            all_exp_techs.extend([t.lower() for t in (exp.technologies or [])])
        matches = len(set(all_exp_techs) & set(required_skills))
        tech_ratio = min(matches / len(required_skills), 1.0)
        tech_bonus = tech_ratio * 3

    return round(min(experience_score + tech_bonus, 15), 2)


def score_education(candidate: TalentProfile, job_requirements: dict) -> float:
    if not candidate.education:
        return 0.0

    required_fields = [f.lower() for f in job_requirements.get("education_fields", [])]
    required_level = job_requirements.get("education_level", "Any").lower()

    DEGREE_RANK = {
        "high school": 1,
        "associate": 2,
        "bachelor's": 3,
        "master's": 4,
        "phd": 5,
        "any": 0
    }

    best_score = 0

    for edu in candidate.education:
        edu_score = 0
        degree_lower = edu.degree.lower()
        field_lower = edu.fieldOfStudy.lower()

        degree_rank = 0
        for degree_key in DEGREE_RANK:
            if degree_key in degree_lower:
                degree_rank = DEGREE_RANK[degree_key]
                break

        required_rank = DEGREE_RANK.get(required_level, 0)

        if required_rank == 0 or degree_rank >= required_rank:
            edu_score += 5
        elif degree_rank == required_rank - 1:
            edu_score += 3

        if required_fields:
            for field in required_fields:
                if field in field_lower or field_lower in field:
                    edu_score += 5
                    break
        else:
            edu_score += 3

        best_score = max(best_score, edu_score)

    return round(min(best_score, 10), 2)


def score_bonus(candidate: TalentProfile, job_requirements: dict) -> float:
    bonus = 0
    employment_type = job_requirements.get("employment_type", "Any")

    if candidate.certifications and len(candidate.certifications) > 0:
        bonus += min(len(candidate.certifications) * 1.0, 2.0)

    if candidate.socialLinks:
        if candidate.socialLinks.linkedin:
            bonus += 0.5
        if candidate.socialLinks.github:
            bonus += 0.5
        if candidate.socialLinks.portfolio:
            bonus += 0.5

    if employment_type and employment_type != "Any":
        if candidate.availability.type and candidate.availability.type.value == employment_type:
            bonus += 1.0

    if candidate.availability.status.value == "Available":
        bonus += 0.5

    return round(min(bonus, 5), 2)


def score_candidate(candidate: TalentProfile, job_requirements: dict) -> dict:
    skills = score_skills(candidate, job_requirements)
    projects = score_projects(candidate, job_requirements)
    experience = score_experience(candidate, job_requirements)
    education = score_education(candidate, job_requirements)
    bonus = score_bonus(candidate, job_requirements)

    raw_total = skills + projects + experience + education + bonus
    multiplier = calculate_evidence_multiplier(candidate)
    final_total = round(raw_total * multiplier, 2)

    return {
        "skills": skills,
        "projects": projects,
        "experience": experience,
        "education": education,
        "bonus": bonus,
        "total": min(final_total, 100)
    }, multiplier