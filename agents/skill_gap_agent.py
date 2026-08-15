from agents.matching_agent import match_job

def analyze_skill_gap(job: dict, profile: dict) -> dict:
    result = match_job(job, profile)

    return {
        "job_title": job.get("title", ""),
        "company": job.get("company", ""),
        "match_score": result["score"],
        "skills_you_have": result["present_skills"],
        "skills_missing": result["missing_skills"],
        "learning_priority": (
            "HIGH" if result["missing_skills"] else "LOW"
        ),
    }

def build_learning_message(skill_gap: dict) -> str:
    missing = skill_gap["skills_missing"]
    if not missing:
        return "No major skill gap detected."
    return (
        f"{skill_gap['job_title']} at {skill_gap['company']} matches "
        f"{skill_gap['match_score']}%. Missing skills: {', '.join(missing)}."
    )
