"""
Diagnostic script to check current configuration
"""
import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 60)
print("CONFIGURATION DIAGNOSTIC")
print("=" * 60)

# ElevenLabs Keys
print("\n📢 ELEVENLABS CONFIGURATION:")
primary = os.environ.get('ELEVENLABS_API_KEY')
backup1 = os.environ.get('ELEVENLABS_API_KEY_BACKUP_1')
backup2 = os.environ.get('ELEVENLABS_API_KEY_BACKUP_2')
voice_id = os.environ.get('ELEVENLABS_VOICE_ID')

print(f"Primary Key: {'✅ SET' if primary else '❌ NOT SET'} ({primary[:20] + '...' if primary else 'None'})")
print(f"Backup Key 1: {'✅ SET' if backup1 else '❌ NOT SET'} ({backup1[:20] + '...' if backup1 else 'None'})")
print(f"Backup Key 2: {'✅ SET' if backup2 else '❌ NOT SET'} ({backup2[:20] + '...' if backup2 else 'None'})")
print(f"Voice ID: {voice_id or 'NOT SET (will use default)'}")

# Check voice ID
if voice_id == 'ErXwobaYiN019PkySvjV':
    print("✅ Voice is set to Antoni (MALE)")
elif voice_id == '21m00Tcm4TlvDq8ikWAM':
    print("❌ Voice is set to Rachel (FEMALE) - WRONG!")
else:
    print(f"⚠️ Unknown voice ID: {voice_id}")

# Mistral Keys
print("\n🤖 MISTRAL CONFIGURATION:")
mistral_key = os.environ.get('MISTRAL_API_KEY')
mistral_base = os.environ.get('MISTRAL_API_BASE')
mistral_model = os.environ.get('MISTRAL_MODEL')

print(f"Mistral Key: {'✅ SET' if mistral_key else '❌ NOT SET'} ({mistral_key[:20] + '...' if mistral_key else 'None'})")
print(f"Mistral Base: {mistral_base or 'NOT SET (will use default: https://api.mistral.ai)'}")
print(f"Mistral Model: {mistral_model or 'NOT SET (will use default: mistral-large-latest)'}")

# Groq (should not be used)
print("\n⚠️ GROQ CONFIGURATION (should be ignored):")
groq_key = os.environ.get('GROQ_API_KEY')
groq_model = os.environ.get('GROQ_MODEL')
print(f"Groq Key: {'SET (but ignored)' if groq_key else 'NOT SET'}")
print(f"Groq Model: {groq_model or 'NOT SET'}")

print("\n" + "=" * 60)
print("RECOMMENDATIONS:")
print("=" * 60)

if not backup1:
    print("❌ Add ELEVENLABS_API_KEY_BACKUP_1 to .env")
if not backup2:
    print("❌ Add ELEVENLABS_API_KEY_BACKUP_2 to .env")
if voice_id != 'ErXwobaYiN019PkySvjV':
    print("❌ Set ELEVENLABS_VOICE_ID=ErXwobaYiN019PkySvjV in .env for male voice")
if not mistral_key:
    print("❌ Add MISTRAL_API_KEY to .env")

print("\n✅ All checks complete!")
