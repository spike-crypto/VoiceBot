from dotenv import load_dotenv
import os
load_dotenv('backend/.env')
from huggingface_hub import InferenceClient
TOKEN = os.environ.get('HUGGINGFACE_API_TOKEN') or os.environ.get('HF_TOKEN')
print('Have token:', bool(TOKEN))
try:
    c = InferenceClient(api_key=TOKEN, provider='huggingface')
    print('Created client with provider huggingface')
    res = c.automatic_speech_recognition('backend/uploads/test_gtts.mp3', model='openai/whisper-large-v3')
    print('Result type:', type(res))
    print(res)
except Exception as e:
    import traceback
    print('Exception:', repr(e))
    traceback.print_exc()
