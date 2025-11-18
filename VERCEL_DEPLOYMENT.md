# Vercel 部署指南

## 准备工作

项目已经配置好所有必要的文件：
- ✅ `vercel.json` - Vercel配置文件
- ✅ `wsgi.py` - WSGI入口文件
- ✅ `.vercelignore` - 忽略文件配置
- ✅ `requirements.txt` - Python依赖

## 方法1：通过Vercel网站部署（推荐）

### 步骤：

1. **访问 Vercel 网站**
   - 打开 https://vercel.com
   - 使用GitHub账号登录

2. **导入项目**
   - 点击 "Add New..." → "Project"
   - 选择 "Import Git Repository"
   - 找到并选择 `COMP5241-2526Sem1/groupproject-team_4`
   - 选择分支：`DEV-FINAL`

3. **配置项目**
   - Framework Preset: 选择 "Other"
   - Root Directory: `./` (保持默认)
   - Build Command: 留空
   - Output Directory: 留空

4. **设置环境变量**
   点击 "Environment Variables"，添加以下变量：
   
   ```
   DATABASE_URL=你的PostgreSQL数据库URL
   GITHUB_TOKEN=你的GitHub Token (用于AI功能)
   SECRET_KEY=your_secret_key_123456789
   ```

   **数据库URL格式：**
   ```
   postgresql://username:password@host:port/database
   ```

5. **部署**
   - 点击 "Deploy" 按钮
   - 等待构建完成（约2-5分钟）
   - 部署成功后会显示项目URL

## 方法2：使用Vercel CLI（需要先安装Node.js）

### 前置条件：
需要先安装 Node.js：https://nodejs.org/

### 步骤：

1. **安装 Vercel CLI**
   ```powershell
   npm install -g vercel
   ```

2. **登录 Vercel**
   ```powershell
   cd "d:\文档\POST-GRADUATE\SEM1\COMP5241 SOFTWARE ENGINEERING AND DEVELOPMENT\TeamProject\learning_platform"
   vercel login
   ```

3. **部署项目**
   ```powershell
   vercel --prod
   ```

4. **按提示操作**
   - Set up and deploy: Yes
   - Which scope: 选择你的账号
   - Link to existing project: No
   - Project name: learning-platform (或其他名称)
   - In which directory: ./ (按回车)
   - Override settings: No

## 数据库配置

### 推荐使用 Vercel Postgres 或其他云数据库：

**选项1：Vercel Postgres（最简单）**
- 在Vercel项目中点击 "Storage" → "Create Database"
- 选择 "Postgres"
- 数据库创建后，环境变量会自动设置

**选项2：外部PostgreSQL数据库**
- Supabase: https://supabase.com (免费)
- ElephantSQL: https://www.elephantsql.com (免费)
- Render: https://render.com (免费)

### 初始化数据库：

部署后需要初始化数据库表，可以通过以下方式：

1. 连接到数据库
2. 运行 `scripts/create_database.sql` 中的SQL语句
3. 或使用Python shell创建表：
   ```python
   from app import app, db
   with app.app_context():
       db.create_all()
   ```

## 部署后检查

1. **访问部署的URL**
   - 应该能看到登录页面

2. **测试功能**
   - 登录功能
   - 课程管理
   - 活动创建
   - 学生提交

3. **查看日志**
   - 在Vercel Dashboard中点击项目
   - 进入 "Deployments" 
   - 点击最新部署查看运行时日志

## 常见问题

### 1. 数据库连接失败
- 检查 `DATABASE_URL` 环境变量是否正确
- 确认数据库允许外部连接
- Vercel默认使用PostgreSQL，不支持SQLite

### 2. GitHub AI功能不工作
- 确认 `GITHUB_TOKEN` 环境变量已设置
- 检查Token权限是否足够

### 3. 静态文件404
- 确认 `static/` 文件夹已推送到GitHub
- 检查 `vercel.json` 配置是否正确

### 4. 部署超时
- 减小依赖包大小
- 检查 `requirements.txt` 中是否有不必要的包

## 项目信息

- **GitHub仓库**: https://github.com/COMP5241-2526Sem1/groupproject-team_4
- **分支**: DEV-FINAL
- **框架**: Flask 3.0.0
- **Python版本**: 3.9+

## 更新部署

每次推送到GitHub的 `DEV-FINAL` 分支后，Vercel会自动重新部署。

也可以在Vercel Dashboard中手动触发重新部署：
1. 进入项目
2. 点击 "Deployments"
3. 点击 "..." → "Redeploy"

---

**注意**: 确保所有敏感信息（如数据库密码、API密钥）都设置在Vercel的环境变量中，不要提交到代码库！
