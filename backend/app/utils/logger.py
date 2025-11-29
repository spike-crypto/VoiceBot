"""
Logging configuration and setup
"""
import logging
import os
from datetime import datetime
from pathlib import Path
from flask import Flask


def setup_logging(app: Flask):
    """Configure logging for the Flask application"""
    log_dir = Path(app.config.get('LOG_DIR', 'logs'))
    log_dir.mkdir(exist_ok=True)
    
    log_level = getattr(logging, app.config.get('LOG_LEVEL', 'INFO').upper())
    
    # Create log filename with timestamp
    log_filename = log_dir / f"voicebot_{datetime.now().strftime('%Y%m%d')}.log"
    
    # Configure logging format
    log_format = '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
    
    # File handler
    file_handler = logging.FileHandler(log_filename, encoding='utf-8')
    file_handler.setLevel(log_level)
    file_handler.setFormatter(logging.Formatter(log_format))
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(logging.Formatter(log_format))
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Clear existing handlers to avoid duplicates
    root_logger.handlers.clear()
    
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    # Ensure errors are always visible - set levels appropriately
    root_logger.setLevel(logging.DEBUG)  # Root logger catches all
    file_handler.setLevel(logging.DEBUG)  # File gets everything
    console_handler.setLevel(logging.INFO)  # Console shows INFO and above (including ERROR)
    
    # Make sure ERROR level is always visible
    file_handler.setLevel(logging.DEBUG)
    console_handler.setLevel(logging.INFO)  # ERROR is above INFO, so it will show
    
    # Reduce noise from third-party libraries
    logging.getLogger('werkzeug').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('socketio').setLevel(logging.WARNING)
    logging.getLogger('engineio').setLevel(logging.WARNING)
    
    app.logger.info("="*60)
    app.logger.info("Voice Bot Interview Assistant - Backend Starting")
    app.logger.info(f"Log file: {log_filename}")
    app.logger.info("="*60)

