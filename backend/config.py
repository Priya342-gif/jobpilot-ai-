from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "JobPilot AI"
    database_url: str = "sqlite:///./data/jobpilot.db"

    scan_interval_minutes: int = 20
    min_match_score: float = 70
    auto_apply: bool = False

    smtp_host: str = ""
    smtp_port: int = 587
    smtp_username: str = ""
    smtp_password: str = ""
    notify_email_to: str = ""

    whatsapp_access_token: str = ""
    whatsapp_phone_number_id: str = ""
    whatsapp_to: str = ""

    remotive_api_url: str = "https://remotive.com/api/remote-jobs"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
