#!/usr/bin/env python
"""验证恢复的功能是否正常工作"""

import sys
sys.path.insert(0, '.')

from app import app
from database import db
from models.poll import Poll
from models.short_answer import ShortAnswer

with app.app_context():
    # 检查poll数据
    polls = Poll.query.all()
    print(f"✓ Polls in database: {len(polls)}")
    for poll in polls:
        print(f"  - Poll {poll.id}: {poll.name} ({len(poll.questions)} questions)")
    
    # 检查短答题数据
    short_answers = ShortAnswer.query.all()
    print(f"\n✓ Short Answers in database: {len(short_answers)}")
    for sa in short_answers:
        print(f"  - Short Answer {sa.id}: {sa.name} ({len(sa.questions)} questions)")
    
    print("\n✓ 所有恢复的文件和数据库状态验证完成！")
