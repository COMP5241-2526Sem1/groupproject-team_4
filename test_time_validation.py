from app import app
from datetime import datetime
from models.poll import Poll

with app.app_context():
    poll = Poll.query.first()
    current_time = datetime.now()
    is_available = poll.start_datetime <= current_time <= poll.end_datetime
    
    print(f'Poll: {poll.name}')
    print(f'Current time: {current_time}')
    print(f'Start: {poll.start_datetime}')
    print(f'End: {poll.end_datetime}')
    print(f'Is available: {is_available}')
    
    # Test the logic we added to the routes
    print(f'\nTime validation check:')
    print(f'  Current time <= End time: {current_time <= poll.end_datetime}')
    print(f'  Current time >= Start time: {current_time >= poll.start_datetime}')
    print(f'  Overall available: {poll.start_datetime <= current_time <= poll.end_datetime}')