# Quiz, Poll, Short Answer 功能与UI设计完整指令

## 概述
本指令详细描述了Flask教学系统中三个核心功能模块（Quiz、Poll、Short Answer）的功能实现、数据库设计、后端路由、前端UI和与AI交互的完整流程。

---

## 第一部分：QUIZ 模块

### 1.1 数据库模型

#### 核心表结构：
- **Quiz**: 测验主表
  - `id`: 主键
  - `course_code`: 课程代码 (FK)
  - `name`: 测验名称
  - `description`: 测验描述
  - `created_by`: 创建者ID (FK to User)
  - `duration`: 时长（分钟）
  - `start_datetime`: 开始时间
  - `end_datetime`: 结束时间
  - `attempt_limit`: 尝试次数限制
  - `point`: 总分
  - `point_in_course`: 课程中的分数权重
  - `created_at`: 创建时间
  - `updated_at`: 更新时间

- **Question**: 题目表
  - `id`: 主键
  - `quiz_id`: 所属测验ID (FK)
  - `type`: 题型 ('mcq' 多选, 'saq' 简答)
  - `content`: 题目内容
  - `points`: 该题分值
  - `order`: 题目顺序
  - 关系: `choices` (一对多), `question_responses` (一对多)

- **Choice**: 选项表（用于MCQ）
  - `id`: 主键
  - `question_id`: 所属题目ID (FK)
  - `content`: 选项内容
  - `is_correct`: 是否正确答案
  - `order`: 选项顺序

- **Submission**: 提交表
  - `id`: 主键
  - `user_id`: 提交学生 (FK)
  - `quiz_id`: 所属测验 (FK)
  - `submitted_at`: 提交时间
  - `grade`: 得分
  - 关系: `question_responses` (一对多, backref='submission')

- **QuestionResponse**: 答案表
  - `id`: 主键
  - `submission_id`: 所属提交 (FK)
  - `question_id`: 所属题目 (FK)
  - `choice_id`: 选择的答案（MCQ用）(FK)
  - `text_answer`: 文本答案（SAQ用）
  - `is_correct`: 是否正确
  - `points`: 该题得分

### 1.2 后端路由

#### 文件位置
`routes/quiz_routes.py`

#### 关键路由

**1. 获取测验信息 (学生视图)**
```
Route: GET /course/<course_code>/quiz/<int:quiz_id>
Function: get_quiz_info()
功能:
  - 验证课程存在
  - 验证用户已登录
  - 验证用户已注册到课程
  - 检查用户是否可以尝试（检查attempt_limit）
  - 返回quiz_info.html模板
数据流:
  - 查询Quiz表获取基本信息
  - 查询Question表获取所有题目
  - 对于MCQ题目，查询Choice表获取选项
  - 准备poll_data字典并返回
```

**2. 获取单个题目数据 (API)**
```
Route: GET /api/quiz/<int:quiz_id>/questions/<int:question_index>
Function: get_quiz_question()
功能:
  - 返回特定题目的JSON数据
  - 包含题目内容、题型、选项等信息
```

**3. 提交答案**
```
Route: POST /course/<course_code>/quiz/<int:quiz_id>/submit
Function: submit_quiz_answer()
功能:
  - 接收答案JSON
  - 验证答案正确性
  - 保存到QuestionResponse表
  - 计算分数
  - 更新Submission表
```

### 1.3 前端界面（quiz_info.html）

#### 页面布局

**顶部：标题和描述**
- 标题：使用紫色渐变背景 (#667eea → #764ba2)
- 描述文本

**中间：进度条**
- 显示"Progress: X / Y"
- 进度条用蓝色表示 (#2196F3 → #1976D2)
- 百分比计算: (currentQuestion + 1) / totalQuestions * 100

**主内容：单问题卡片**
- 每次只显示一个题目
- 其他题目隐藏 (display: none)
- 卡片包含:
  - 题号徽章: "Question X of Y"
  - 题目内容
  - 选项列表（MCQ）或文本框（SAQ）

**MCQ选项样式**
```css
.poll-option {
  padding: 15px 18px;
  background: #f9f9f9;
  border: 2px solid #ddd;
  border-radius: 6px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.poll-option:hover {
  background: #f0f8ff;
  border-color: #2196F3;
  box-shadow: 0 2px 6px rgba(33, 150, 243, 0.15);
}

.poll-option.selected {
  background: #e3f2fd;
  border-color: #2196F3;
  box-shadow: 0 2px 8px rgba(33, 150, 243, 0.25);
}
```

**底部：导航和提交按钮**
- 上一页/下一页按钮 (#6c757d)
- 提交按钮 (#2196F3)
- 返回按钮

#### JavaScript交互
```javascript
// 全局变量
let currentQuestion = 0;
const totalQuestions = {{ quiz.questions|length }};

// 导航函数
function nextQuestion() { ... }
function previousQuestion() { ... }
function showQuestion(index) { ... }
function hideQuestion(index) { ... }

// UI更新
function updateProgressBar() {
  const progress = ((currentQuestion + 1) / totalQuestions) * 100;
  document.getElementById('progress-bar').style.width = progress + '%';
  document.getElementById('current-question').textContent = currentQuestion + 1;
}

// 选项交互
function selectOption(element) {
  const siblings = element.parentNode.querySelectorAll('.poll-option');
  siblings.forEach(el => el.classList.remove('selected'));
  element.classList.add('selected');
}
```

### 1.4 AI集成（生成测验题目）

#### 文件位置
`routes/ai_routes.py`

#### 路由
```
Route: POST /api/ai/quiz
Function: generate_quiz_with_ai()
请求JSON:
{
  "topic": "string",
  "num_questions": int,
  "question_types": ["mcq", "saq"],
  "difficulty": "easy|medium|hard"
}
响应JSON:
{
  "success": boolean,
  "quiz_id": int,
  "questions": [
    {
      "content": "string",
      "type": "mcq|saq",
      "points": int,
      "choices": [
        {
          "content": "string",
          "is_correct": boolean
        }
      ]
    }
  ]
}
```

---

## 第二部分：POLL 模块

### 2.1 数据库模型

#### 核心表结构
- **Poll**: 投票主表
  - `id`: 主键
  - `course_code`: 课程代码 (FK)
  - `name`: 投票名称
  - `description`: 投票描述
  - `created_by`: 创建者ID (FK)
  - `attempt_limit`: 每学生投票次数限制
  - `start_datetime`: 开始时间
  - `end_datetime`: 结束时间
  - `created_at`: 创建时间
  - `updated_at`: 更新时间

- **Question**: 题目表（同Quiz）
  - 关键字段: `poll_id`, `type`, `content`
  - 关系: `choices` (一对多)

- **Choice**: 选项表
  - `id`: 主键
  - `question_id`: 所属题目 (FK)
  - `content`: 选项内容

- **Submission** & **QuestionResponse**: 同Quiz模型
  - poll_id替代quiz_id
  - 存储学生的投票选择

### 2.2 后端路由

#### 文件位置
`routes/poll_routes.py`

#### 关键路由

**1. 获取投票信息 (学生视图)**
```
Route: GET /course/<course_code>/poll/<int:poll_id>
Function: get_poll_info()
功能:
  - 验证课程存在（使用filter_by(code=course_code)）
  - 验证用户登录和注册
  - 获取投票基本信息
  - 获取所有题目及选项
  - 计算每个选项的投票数（从QuestionResponse表统计）
```

**关键代码示例**
```python
@poll_bp.route('/course/<course_code>/poll/<int:poll_id>', methods=['GET'])
def get_poll_info(course_code, poll_id):
    # 重要：使用filter_by而不是get()
    course = Course.query.filter_by(code=course_code).first()
    if not course:
        return render_template('course_home.html', 
                             error_message="Course not found"), 404
    
    # 验证登录和注册...
    
    # 构建poll_data
    poll_data = {
        'id': poll.id,
        'name': poll.name,
        'description': poll.description,
        'questions': []
    }
    
    for question in questions:
        q_data = {
            'id': question.id,
            'content': question.content,
            'type': question.type
        }
        
        if question.type == 'mcq':
            choices = Choice.query.filter_by(question_id=question.id).all()
            choices_data = []
            for choice in choices:
                # 计算每个选项的投票数
                vote_count = QuestionResponse.query.filter_by(
                    question_id=question.id,
                    choice_id=choice.id
                ).count()
                choices_data.append({
                    'id': choice.id,
                    'content': choice.content,
                    'vote_count': vote_count
                })
            q_data['choices'] = choices_data
        
        poll_data['questions'].append(q_data)
    
    return render_template('poll_info.html', course=course, poll=poll_data)
```

### 2.3 前端界面（poll_info.html）

#### 页面布局与样式

**与Quiz相同的基本布局，区别如下：**

**标题区域**
- 紫色渐变背景 (#667eea → #764ba2)
- 投票名称（标题）
- 投票描述文本

**投票选项显示 - 关键区别**
```html
<ul class="poll-options">
  {% for choice in question.choices %}
  <li class="poll-option" onclick="selectOption(this)">
    <span class="option-text">{{ choice.content }}</span>
    <span class="option-count">
      <i class="fas fa-user"></i>
      <span class="option-count-number" data-choice-id="{{ choice.id }}">
        {{ choice.vote_count }}
      </span>
    </span>
  </li>
  {% endfor %}
</ul>
```

**投票计数显示**
- 每个选项右侧显示: "👤 数字"
- 数字表示已投票的人数
- 从后端直接传入vote_count，不需要实时计算
- 颜色: #2196F3（蓝色）

#### CSS样式
```css
.option-count {
  margin-left: 15px;
  padding-left: 15px;
  border-left: 1px solid #ddd;
  color: #999;
  font-size: 0.9rem;
  white-space: nowrap;
  display: flex;
  align-items: center;
  gap: 8px;
}

.option-count-number {
  font-weight: 700;
  color: #2196F3;
  font-size: 1.1rem;
}

.option-count i {
  font-size: 1rem;
}
```

### 2.4 投票提交

#### 路由
```
Route: POST /course/<course_code>/poll/<int:poll_id>/submit
Function: submit_poll_vote()
```

#### 功能
- 接收学生的投票选择
- 检查是否超过attempt_limit
- 保存到Submission和QuestionResponse表
- 返回成功消息

### 2.5 AI集成（生成投票题目）

#### 路由
```
Route: POST /api/ai/poll
Function: generate_poll_with_ai()
```

#### 请求/响应格式
类似Quiz，但无difficulty参数，questions通常只有1个，type固定为'mcq'

---

## 第三部分：SHORT ANSWER 模块

### 3.1 数据库模型

#### 核心表结构
- **ShortAnswer**: 简答主表
  - `id`: 主键
  - `course_code`: 课程代码 (FK)
  - `name`: 活动名称
  - `description`: 活动描述
  - `created_by`: 创建者ID (FK)
  - `duration`: 时长
  - `start_datetime`: 开始时间
  - `end_datetime`: 结束时间
  - `attempt_limit`: 尝试次数限制
  - `point`: 总分
  - `point_in_course`: 课程权重
  - 关系: `questions` (一对多)

- **Question**: 题目表
  - `id`: 主键
  - `short_answer_id`: 所属简答ID (FK)
  - `type`: 固定为 'saq'
  - `content`: 题目内容
  - `points`: 该题分值
  - 关系: `question_responses` (一对多, backref='question')

- **Submission**: 提交表
  - 同quiz/poll，但关键字段是 `short_answer_id`
  - 关系: `question_responses` (一对多, backref='submission')

- **QuestionResponse**: 答案表
  - `id`: 主键
  - `submission_id`: 所属提交 (FK)
  - `question_id`: 所属题目 (FK)
  - `text_answer`: 文本答案
  - `points`: 该题得分
  - `is_correct`: 是否正确（可选）

### 3.2 后端路由

#### 文件位置
`routes/short_answer_routes.py`

#### 关键路由

**1. 学生查看简答详情（查看所有学生答案）**
```
Route: GET /course/<course_code>/short-answer/<int:short_answer_id>
Function: short_answer_detail()
功能:
  - 验证课程和登录
  - 获取简答活动信息
  - 获取所有题目
  - 获取该简答的所有学生提交（ALL submissions，不限当前用户）
  - 每个提交关联其对应的question_responses
  - 返回short_answer_detail.html
```

**2. 学生开始回答**
```
Route: GET /course/<course_code>/short-answer/<int:short_answer_id>/start
Function: short_answer_start()
功能:
  - 显示问卷开始页面
  - 准备student_submission_form.html
```

**3. 学生提交答案**
```
Route: POST /course/<course_code>/short-answer/<int:short_answer_id>/submit
Function: submit_short_answer()
功能:
  - 接收所有题目的文本答案
  - 创建Submission记录
  - 创建QuestionResponse记录
  - 保存答案
```

**4. 教师查看结果（概览）**
```
Route: GET /teacher/course/<course_code>/short-answer/<int:short_answer_id>/results
Function: short_answer_results()
功能:
  - 显示简答结果统计
  - 显示所有学生的提交列表
```

### 3.3 前端界面（short_answer_detail.html）

#### 页面布局

**顶部标题区域**
```html
<div class="detail-header">
  <h1>{{ short_answer.name }}</h1>
  {% if short_answer.description %}
    <p class="description">{{ short_answer.description }}</p>
  {% endif %}
</div>
```

样式:
```css
.detail-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 30px;
  border-radius: 10px;
  margin-bottom: 25px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.detail-header h1 {
  margin: 0 0 10px 0;
  font-size: 28px;
}

.detail-header .description {
  margin: 0;
  font-size: 16px;
  opacity: 0.95;
}
```

**题目区域**
```html
<div class="questions-container">
  {% for question in short_answer.questions %}
  <div class="question-section">
    <!-- 题目头 -->
    <div class="question-header">
      <h2>Q{{ loop.index }}: {{ question.content }}</h2>
      <div class="question-meta">
        Points: {{ question.points }} | 
        Total Responses: {{ question.question_responses|length }}
      </div>
    </div>

    <!-- 答案区 -->
    <div class="answers-container">
      <div class="answers-summary">
        {{ question.question_responses|length }} student(s) answered this question
      </div>

      {% for response in question.question_responses %}
      <div class="student-answer-item">
        <div class="student-header">
          <div>
            <div class="student-name">
              {{ response.submission.student.username if response.submission.student else 'Unknown User' }}
              {% if response.submission.submitted_at %}
                <span style="color: #999; font-weight: normal; font-size: 12px;">
                  (Submitted: {{ response.submission.submitted_at.strftime('%Y-%m-%d %H:%M') }})
                </span>
              {% endif %}
            </div>
          </div>
          {% if response.points %}
            <div class="student-points">
              {{ response.points }} / {{ question.points }} pts
            </div>
          {% endif %}
        </div>

        <div class="answer-text">
          {{ response.text_answer or 'No answer provided' }}
        </div>
      </div>
      {% endfor %}
    </div>
  </div>
  {% endfor %}
</div>
```

**关键CSS**
```css
.questions-container {
  display: flex;
  flex-direction: column;
  gap: 40px;
  margin: 30px 0;
}

.question-section {
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.question-header {
  background: #f5f5f5;
  padding: 20px;
  border-bottom: 2px solid #e0e0e0;
}

.question-header h2 {
  margin: 0;
  color: #333;
  font-size: 18px;
  line-height: 1.6;
}

.question-meta {
  margin-top: 10px;
  color: #999;
  font-size: 13px;
}

.answers-container {
  padding: 20px;
}

.answers-summary {
  margin-bottom: 20px;
  padding: 12px;
  background: #e3f2fd;
  border-left: 4px solid #2196F3;
  border-radius: 4px;
  color: #1565c0;
  font-weight: 500;
}

.student-answer-item {
  background: #f9f9f9;
  border: 1px solid #e8e8e8;
  border-radius: 6px;
  padding: 15px;
  margin-bottom: 12px;
}

.student-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 10px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

.student-name {
  font-weight: 600;
  color: #333;
  font-size: 14px;
}

.student-points {
  background: #e8f5e9;
  color: #2e7d32;
  padding: 4px 8px;
  border-radius: 3px;
  font-size: 12px;
  font-weight: 600;
}

.answer-text {
  color: #555;
  line-height: 1.7;
  font-size: 14px;
  white-space: pre-wrap;
  word-break: break-word;
  margin: 10px 0 0 0;
}
```

### 3.4 关键实现细节

**数据库关系配置**
```python
# 在Submission模型中
from sqlalchemy.orm import relationship

question_responses = db.relationship('QuestionResponse', backref='submission', cascade='all, delete-orphan')

# 在Question模型中
question_responses = relationship('QuestionResponse', backref='question', cascade='all, delete-orphan')
```

**路由中的关键查询**
```python
# 获取所有提交（NOT限制为当前用户）
submissions = Submission.query.filter_by(
    short_answer_id=short_answer_id
).all()

# 获取题目和对应的所有答案
questions = Question.query.filter_by(
    short_answer_id=short_answer_id
).all()

# 每个question的question_responses会通过relationship自动加载
for question in questions:
    for response in question.question_responses:
        # response.submission.student 获取学生信息
        # response.submission.submitted_at 获取提交时间
        # response.text_answer 获取答案文本
        # response.points 获取该题得分
```

### 3.5 AI集成

#### 路由
```
Route: POST /api/ai/short-answer
Function: generate_short_answer_with_ai()
请求JSON:
{
  "topic": "string",
  "num_questions": int
}
响应JSON:
{
  "success": boolean,
  "questions": [
    {
      "content": "string",
      "points": int
    }
  ]
}
```

---

## 第四部分：通用功能

### 4.1 教师管理页面

#### Quiz列表 `/teacher/course/<course_code>/quiz`
- 显示所有测验
- 操作按钮: View, Edit, Delete
- AI生成按钮

#### Poll列表 `/teacher/course/<course_code>/poll`
- 显示所有投票
- 操作按钮: View, Results, Edit, Delete

#### Short Answer列表 `/teacher/course/<course_code>/short-answer`
- 显示所有简答活动
- 操作按钮: View, Edit, Delete

### 4.2 共通样式

#### 按钮样式
```css
/* 蓝色按钮 */
.btn-edit { background: #4a90e2; color: white; }

/* 红色删除按钮 */
.btn-delete { background: #e85d4f; color: white; }

/* 文本按钮 */
.btn-view { background: #7d3d3d; color: white; }

/* 所有按钮通用 */
padding: 12px 24px;
border-radius: 4px;
font-weight: 600;
font-size: 15px;
border: none;
cursor: pointer;
transition: all 0.3s ease;

&:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
```

#### 渐变背景（所有标题）
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
color: white;
```

### 4.3 关键路径

#### 学生操作流程
1. 登录 → 课程页面 → Quiz/Poll/ShortAnswer列表
2. 点击具体项目 → 查看描述和基本信息（quiz_info.html / poll_info.html / short_answer_detail.html）
3. 点击"Participate"/"Start" → 开始作答
4. 提交答案 → 返回列表或查看结果

#### 教师操作流程
1. 登录 → 课程 → Quiz/Poll/ShortAnswer管理页面
2. 创建新项目（支持AI生成或手动创建）
3. 编辑/删除/查看结果
4. 查看学生提交情况

---

## 第五部分：数据一致性和验证

### 5.1 必需的字段验证

- 课程代码必须存在
- 用户必须已登录
- 用户必须注册到课程
- 测验/投票/简答必须属于该课程
- 提交前必须验证attempt_limit

### 5.2 错误处理

```python
# 课程不存在
return render_template('course_home.html', 
                     error_message="Course not found"), 404

# 未登录
return redirect(url_for('auth.login'))

# 未注册到课程
return render_template('course_home.html', 
                     error_message="You are not enrolled in this course"), 403

# 超过尝试次数
return jsonify({
    'success': False,
    'message': 'You have reached the maximum number of attempts'
}), 403
```

---

## 总结表格

| 功能 | Quiz | Poll | Short Answer |
|------|------|------|--------------|
| 主表 | Quiz | Poll | ShortAnswer |
| 题型 | MCQ + SAQ | MCQ | SAQ |
| 单题显示 | 是 | 是 | 否（所有题目+答案列表） |
| 投票计数显示 | 否 | 是 | 否 |
| 学生提交后可见 | 否 | 否 | 是（所有答案） |
| AI集成 | 是 | 是 | 是 |
| 主要差异 | 评分系统 | 计票显示 | 集体答案展示 |

---

## 文件清单

### 路由文件
- `routes/quiz_routes.py`
- `routes/poll_routes.py`
- `routes/short_answer_routes.py`
- `routes/ai_routes.py`

### 模板文件
- `templates/quiz_info.html`
- `templates/quiz_start.html`
- `templates/poll_info.html`
- `templates/poll_start.html`
- `templates/short_answer_detail.html`
- `templates/short_answer_start.html`
- `templates/teacher_quiz_list.html`
- `templates/teacher_poll_list.html`
- `templates/teacher_short_answer_list.html`

### 模型文件
- `models/quiz.py`
- `models/poll.py`
- `models/short_answer.py`
- `models/question.py`
- `models/choice.py`
- `models/submission.py`
- `models/question_response.py`

---

**最后更新**: 2025年11月17日
