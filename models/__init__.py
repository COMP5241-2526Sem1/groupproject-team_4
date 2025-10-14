from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .course import Course
from .course_enrollment import CourseEnrollment
from .activity import Activity
from .submission import Submission
from .grade import Grade
from .notification import Notification
from .system_log import SystemLog
