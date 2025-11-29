
import os
import sys
from app import create_app
from app.services import tts_service, stt_service

def test_elevenlabs_services():
    print("Initializing Flask App...")
    app = create_app()
    
    with app.app_context():
        print("\n" + "="*50)
        print("  ELEVENLABS INTEGRATION TEST")
        print("="*50)
        
        # 1. Test TTS
        print("\n1. Testing ElevenLabs TTS...")
        text = "This is a test of the Eleven Labs Scribe transcription service."
        audio_path = None
        try:
            # Disable cache to force API call
            audio_path, cache_hit = tts_service.text_to_speech(text, use_cache=False)
            print(f"✅ TTS Success: Generated audio file at")
            print(f"   {audio_path}")
            print(f"   Size: {os.path.getsize(audio_path)} bytes")
        except Exception as e:
            print(f"❌ TTS Failed: {e}")
            return

        # 2. Test STT
        print("\n2. Testing ElevenLabs Scribe STT...")
        try:
            # Verify config
            provider = app.config.get('STT_PROVIDER')
            print(f"   Current STT_PROVIDER: {provider}")
            if provider != 'elevenlabs':
                print("   ⚠️ WARNING: STT_PROVIDER is not 'elevenlabs'. Test might use another provider.")
            
            # Transcribe
            transcription, cache_hit = stt_service.transcribe_audio(audio_path, use_cache=False)
            print(f"✅ STT Success!")
            print(f"   Original: '{text}'")
            print(f"   Result:   '{transcription}'")
            
            # Simple verification
            # Normalize for comparison
            t1 = text.lower().replace('.', '').replace(',', '')
            t2 = transcription.lower().replace('.', '').replace(',', '')
            
            # Calculate simple overlap or just check key words
            if "scribe" in t2 or "eleven" in t2:
                 print("✅ Content Verified (Keywords found)")
            else:
                 print(f"⚠️ Content mismatch. Please check manually.")

        except Exception as e:
            print(f"❌ STT Failed: {e}")

if __name__ == "__main__":
    test_elevenlabs_services()
