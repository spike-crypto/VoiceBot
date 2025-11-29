import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Add backend directory to path so we can import app modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.services.tts_service import text_to_speech

class TestTTSFallback(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.ctx = self.app.app_context()
        self.ctx.push()
        
        # Mock configuration with primary and backup keys
        self.app.config['ELEVENLABS_API_KEY'] = 'primary_key'
        self.app.config['ELEVENLABS_API_KEY_BACKUP_1'] = 'backup_key_1'
        self.app.config['ELEVENLABS_API_KEY_BACKUP_2'] = 'backup_key_2'
        self.app.config['ELEVENLABS_VOICE_ID'] = 'voice_id'
        self.app.config['UPLOAD_FOLDER'] = 'uploads'

    def tearDown(self):
        self.ctx.pop()

    @patch('app.services.tts_service.requests.post')
    @patch('app.services.tts_service.open')
    @patch('app.services.tts_service.os.path.exists')
    @patch('app.services.tts_service.os.getsize')
    def test_fallback_logic(self, mock_getsize, mock_exists, mock_open, mock_post):
        # Setup mocks
        mock_exists.return_value = True
        mock_getsize.return_value = 1024  # Fake file size
        
        # Scenario: Primary key fails with 429, Backup 1 succeeds
        
        # Mock response for Primary Key (429 Quota Exceeded)
        resp_primary = MagicMock()
        resp_primary.status_code = 429
        resp_primary.text = "Quota exceeded"
        
        # Mock response for Backup Key 1 (200 OK)
        resp_backup = MagicMock()
        resp_backup.status_code = 200
        resp_backup.iter_content.return_value = [b'audio_data']
        
        # Configure side_effect to return primary failure first, then backup success
        mock_post.side_effect = [resp_primary, resp_backup]
        
        # Run TTS
        try:
            audio_path, cache_hit = text_to_speech("Test text", use_cache=False)
            print("\n✅ Test Passed: Fallback to Backup Key 1 successful")
        except Exception as e:
            self.fail(f"TTS failed: {e}")
            
        # Verify calls
        self.assertEqual(mock_post.call_count, 2)
        
        # Verify first call used primary key
        args1, kwargs1 = mock_post.call_args_list[0]
        self.assertEqual(kwargs1['headers']['xi-api-key'], 'primary_key')
        print("   - Attempt 1 used Primary Key (got 429)")
        
        # Verify second call used backup key 1
        args2, kwargs2 = mock_post.call_args_list[1]
        self.assertEqual(kwargs2['headers']['xi-api-key'], 'backup_key_1')
        print("   - Attempt 2 used Backup Key 1 (Success)")

    @patch('app.services.tts_service.requests.post')
    def test_all_keys_fail(self, mock_post):
        # Scenario: All keys fail
        
        resp_fail = MagicMock()
        resp_fail.status_code = 429
        
        mock_post.return_value = resp_fail
        
        with self.assertRaises(Exception) as cm:
            text_to_speech("Test text", use_cache=False)
            
        print("\n✅ Test Passed: Correctly raised exception when all keys failed")
        self.assertEqual(mock_post.call_count, 3) # Should try all 3 keys
        print("   - Tried Primary, Backup 1, and Backup 2")

if __name__ == '__main__':
    unittest.main()
