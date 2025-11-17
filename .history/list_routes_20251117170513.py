#!/usr/bin/env python
"""列出所有注册的Flask路由"""

import sys
sys.path.insert(0, '.')

from app import app

print("Flask registered routes:")
print("=" * 80)

routes = []
for rule in app.url_map.iter_rules():
    routes.append((str(rule), rule.endpoint, ','.join(rule.methods - {'HEAD', 'OPTIONS'})))

# Sort by route
routes.sort(key=lambda x: x[0])

for route, endpoint, methods in routes:
    # 只显示相关的路由
    if 'ai' in route.lower() or 'poll' in route.lower() or 'short' in route.lower():
        print(f"{route:50} | {endpoint:30} | {methods}")

print("\n" + "=" * 80)
print("Total routes:", len(routes))
