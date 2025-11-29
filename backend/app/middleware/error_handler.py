"""
Error handling middleware
"""
from flask import jsonify
from app.utils.logger import setup_logging
import logging

logger = logging.getLogger(__name__)


def register_error_handlers(app):
    """Register error handlers for the Flask app"""
    
    @app.errorhandler(400)
    def bad_request(error):
        logger.warning(f"Bad request: {str(error)}")
        return jsonify({
            'error': 'Bad Request',
            'message': str(error),
            'status_code': 400
        }), 400
    
    @app.errorhandler(404)
    def not_found(error):
        from flask import request
        logger.warning(f"Not found: {request.method} {request.url} - {str(error)}")
        return jsonify({
            'error': 'Not Found',
            'message': 'The requested resource was not found',
            'status_code': 404
        }), 404
    
    @app.errorhandler(413)
    def request_entity_too_large(error):
        logger.warning(f"File too large: {str(error)}")
        return jsonify({
            'error': 'File Too Large',
            'message': 'The uploaded file exceeds the maximum size limit',
            'status_code': 413
        }), 413
    
    @app.errorhandler(429)
    def rate_limit_exceeded(error):
        logger.warning(f"Rate limit exceeded: {str(error)}")
        return jsonify({
            'error': 'Rate Limit Exceeded',
            'message': 'Too many requests. Please try again later.',
            'status_code': 429
        }), 429
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Internal server error: {str(error)}", exc_info=True)
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred',
            'status_code': 500
        }), 500
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        logger.error(f"Unhandled exception: {str(error)}", exc_info=True)
        return jsonify({
            'error': 'Internal Server Error',
            'message': str(error),
            'status_code': 500
        }), 500

