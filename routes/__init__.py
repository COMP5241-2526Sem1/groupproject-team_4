from .course import course_bp  # Import course module blueprint
from .auth import auth_bp      # Import auth module blueprint
from .quiz_routes import quiz_bp  # Import quiz_routes module blueprint
from .poll_routes import poll_bp  # Import poll_routes module blueprint
from .course_registration import course_registration_bp  # Import course_registration module blueprint

# Define __all__ variable to control from routes import * behavior
__all__ = ['course_bp', 'auth_bp', 'quiz_bp', 'poll_bp', 'course_registration_bp']