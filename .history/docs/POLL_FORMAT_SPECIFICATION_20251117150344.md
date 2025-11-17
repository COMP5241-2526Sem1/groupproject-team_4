# Poll 格式设置文档

## 数据库模型结构

### Poll 表 (poll)
```
字段名                                    类型       默认值      说明
- id                                    Integer    主键
- course_code                           String     外键        关联课程代码
- name                                  String              Poll 名称
- description                           Text               Poll 描述
- created_by                            Integer    外键        创建者 ID
- created_at                            DateTime   当前时间    创建时间
- start_datetime                        DateTime   可为空      开始时间
- end_datetime                          DateTime   可为空      结束时间
- duration                              Integer    30          持续时间（分钟）
- attempt_limit                         Integer    5           尝试限制
- point                                 Integer    0           分数（民调不计分）
- point_in_course                       Integer    0           课程分数
- after_submitted_question_visible      Boolean    True        提交后问题是否可见
- after_submitted_student_response_visible Boolean  True        提交后学生回答是否可见
- after_submitted_sample_response_visible Boolean   True        提交后样本回答是否可见
- after_submitted_class_response_visible Boolean    True        提交后班级回答是否可见
```

### Question 表 (question)
```
字段名           类型          默认值      说明
- id            Integer       主键
- poll_id       Integer       外键        关联 Poll ID
- type          Enum          'mcq'       问题类型（mcq=多选题，saq=短答题）
- content       String                    问题内容（最多1000字符）
- points        Integer       1           问题分数
```

### Choice 表 (choice)
```
字段名           类型          默认值      说明
- id            Integer       主键
- question_id   Integer       外键        关联问题 ID
- content       String                    选项内容（最多500字符）
- is_correct    Boolean       False       是否为正确答案
```

## AI 生成的 Poll JSON 格式

### 标准格式（从 AI 生成）
```json
{
    "poll_name": "Poll name",
    "description": "Brief description",
    "duration": 10,
    "questions": [
        {
            "type": "mcq",
            "content": "Poll question text",
            "points": 0,
            "choices": [
                {"text": "Option A", "correct": false},
                {"text": "Option B", "correct": false},
                {"text": "Option C", "correct": false},
                {"text": "Option D", "correct": false}
            ]
        }
    ]
}
```

## 保存到数据库的映射关系

当保存 AI 生成的 poll 时，映射关系如下：

1. **Poll 表映射**：
   - JSON `poll_name` → 数据库 `Poll.name`
   - JSON `description` → 数据库 `Poll.description`
   - JSON `duration` → 数据库 `Poll.duration`
   - `course_code` 来自 URL 参数
   - `created_by` 来自当前用户 session

2. **Question 表映射**：
   - 对每个 JSON question 创建一条记录
   - JSON `type` → 数据库 `Question.type`（'mcq' 或 'saq'）
   - JSON `content` → 数据库 `Question.content`
   - JSON `points` → 数据库 `Question.points`
   - `poll_id` 来自创建的 Poll 记录

3. **Choice 表映射**（仅限 MCQ）：
   - 对每个 JSON choice 创建一条记录
   - JSON `text` → 数据库 `Choice.content` ⚠️ 注意：JSON 中是 "text"，但数据库字段是 "content"
   - JSON `correct` → 数据库 `Choice.is_correct` ⚠️ 注意：JSON 中是 "correct"，但数据库字段是 "is_correct"
   - `question_id` 来自创建的 Question 记录

## 民调特性

- **分数**：民调问题的分数始终为 0（不计分）
- **正确答案**：民调中所有选项的 `is_correct` 都为 False（因为民调是意见调查，不是评估）
- **可见性**：民调的所有可见性设置默认为 True（民调结果总是可见的）
- **问题类型**：民调通常只包含 MCQ（多选题），不包含 SAQ（短答题）

## 字段名称注意事项

### JSON 格式（AI 生成）vs 数据库字段名
| AI JSON | 数据库字段 | 说明 |
|---------|-----------|------|
| poll_name | Poll.name | 民调名称 |
| description | Poll.description | 民调描述 |
| content | Question.content | 问题内容 |
| type | Question.type | 问题类型 |
| points | Question.points | 问题分数 |
| text (choice) | Choice.content | 选项文本 |
| correct | Choice.is_correct | 是否正确 |

## 保存 Poll 时的数据流

```
前端 (teacher_poll_list.html)
    ↓
JavaScript 发送 JSON 请求到 /api/ai/poll
    ↓
后端 (ai_routes.py) - generate_poll()
    ↓
LLM 生成 JSON 格式的 poll 数据
    ↓
返回 JSON 给前端进行预览
    ↓
用户点击"Save Poll"
    ↓
前端发送保存请求到 /api/ai/save-poll
    ↓
后端 (ai_routes.py) - save_generated_poll()
    ↓
根据映射关系创建 Poll、Question、Choice 记录
    ↓
提交到数据库
    ↓
重定向到 /teacher/course/{course_code}/poll
```

## 常见问题排查

1. **"Topic is required" 错误**
   - 原因：前端发送的字段名错误（使用了 `input` 而不是 `topic`）
   - 解决：确保发送 `topic` 字段名

2. **"'text' is an invalid keyword argument for Choice" 错误**
   - 原因：使用了错误的字段名（`text` 而不是 `content`）
   - 解决：使用 `Choice(question_id=..., content=..., is_correct=...)`

3. **民调保存失败**
   - 检查所有必需字段是否已提供
   - 检查字段名称是否正确
   - 检查数据类型是否匹配
