import re
from backend.profile import PROFILE

def normalize_skill(skill: str) -> str:
    return re.sub(r"\s+", " ", skill.strip().lower())

def get_verified_profile() -> dict:
    # The MVP uses a manually verified profile generated from the uploaded resume.
    # Replace this with PDF/DOCX extraction later.
    return PROFILE

def extract_skill_candidates(text: str, known_skills: list[str]) -> list[str]:
    text_lower = text.lower()
    return [s for s in known_skills if s.lower() in text_lower]
