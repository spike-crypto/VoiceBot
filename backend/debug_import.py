import sys
import os
print(f"Current working directory: {os.getcwd()}")
print(f"Python path: {sys.path}")
import app
print(f"App package location: {app.__file__}")
from app.config import Config
print(f"Config GROQ_MODEL: {Config.GROQ_MODEL}")
