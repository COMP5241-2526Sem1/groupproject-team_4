from app import app
from database import db
from models.picture import Picture

with app.app_context():
    pictures = Picture.query.all()
    print(f'Total pictures: {len(pictures)}')
    for p in pictures:
        print(f'ID: {p.id}, Minigame: {p.minigame_id}, User: {p.user_id}, Type: {p.file_type}, Size: {p.file_size}')