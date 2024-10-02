from dotenv import load_dotenv
import os

# Load biến môi trường từ file .env
load_dotenv()

class Settings:
    # Cấu hình server
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", 8000))

settings = Settings()