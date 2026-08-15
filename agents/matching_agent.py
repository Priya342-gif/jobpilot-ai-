import re

ALIASES = {
    "cpp": "c++",
    "c plus plus": "c++",
    "scikit learn": "scikit-learn",
    "free rtos": "freertos",
}

def norm(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9+#.-]+", " ", value)
    return ALIASES.get(value, value)

def match_job(job: dict, profile: dict) -> dict:
    text = " ".join([
        job.get("title", ""),
        job.get("description", ""),
        " ".join(job.get("required_skills", [])),
    ]).lower()

    profile_skills = {norm(s) for s in profile["skills"]}
    present, missing = [], []

    required = job.get("required_skills", [])

    for skill in required:
        if norm(skill) in profile_skills:
            present.append(skill)
        else:
            missing.append(skill)

    if required:
        skill_score = len(present) / len(required) * 100
    else:
        # If source did not expose structured skills, infer simple mentions.
        hits = sum(1 for s in profile["skills"] if norm(s) in text)
        skill_score = min(100, hits * 8)

    domain_hits = sum(
        1 for domain in profile["target_domains"]
        if domain.lower() in text
    )
    domain_score = min(100, domain_hits * 25)

    score = round(0.8 * skill_score + 0.2 * domain_score, 1)

    return {
        "score": score,
        "present_skills": present,
        "missing_skills": missing,
        "recommendation": "apply" if score >= 70 else "review",
    }
