# Vercel 部署指南

## 部署前准备

### 1. 安装 Vercel CLI
```bash
npm install -g vercel
```

### 2. 登录 Vercel
```bash
vercel login
```

## 部署步骤

### 方法一：使用 Vercel CLI（推荐）

1. **在项目根目录运行部署命令**
```bash
vercel
```

2. **首次部署会询问一些问题**
   - Set up and deploy? → Yes
   - Which scope? → 选择你的账户
   - Link to existing project? → No
   - What's your project's name? → learning_platform (或自定义名称)
   - In which directory is your code located? → ./ (直接回车)

3. **设置环境变量**
   
   部署后需要在 Vercel Dashboard 设置以下环境变量：
   
   ```
   PG_DB_USER=你的数据库用户名
   PG_DB_PASSWORD=你的数据库密码
   PG_DB_HOST=你的数据库主机地址
   PG_DB_PORT=5432
   PG_DB_NAME=你的数据库名称
   SECRET_KEY=your_secret_key_123456789
   GITHUB_TOKEN=你的GitHub令牌（如果使用AI功能）
   ```

4. **重新部署以应用环境变量**
```bash
vercel --prod
```

### 方法二：通过 GitHub 集成部署

1. **将代码推送到 GitHub**
```bash
git init
git add .
git commit -m "Initial commit for Vercel deployment"
git remote add origin https://github.com/你的用户名/learning_platform.git
git push -u origin main
```

2. **在 Vercel Dashboard 导入项目**
   - 访问 https://vercel.com/dashboard
   - 点击 "Add New Project"
   - 选择 "Import Git Repository"
   - 选择你的 GitHub 仓库
   - 配置项目设置（通常自动检测）
   - 添加环境变量（同上）
   - 点击 "Deploy"

## 环境变量配置

在 Vercel Dashboard 中设置环境变量：

1. 进入你的项目
2. 点击 "Settings"
3. 点击 "Environment Variables"
4. 添加以下变量：

| 变量名 | 说明 | 示例 |
|--------|------|------|
| PG_DB_USER | PostgreSQL 用户名 | postgres.xxx |
| PG_DB_PASSWORD | PostgreSQL 密码 | your_password |
| PG_DB_HOST | PostgreSQL 主机 | aws-0-ap-southeast-1.pooler.supabase.com |
| PG_DB_PORT | PostgreSQL 端口 | 5432 |
| PG_DB_NAME | 数据库名称 | postgres |
| SECRET_KEY | Flask 密钥 | your_secret_key_123456789 |
| GITHUB_TOKEN | GitHub API 令牌 | ghp_xxxxxxxxxxxx |

## 数据库注意事项

1. **确保数据库可从外部访问**
   - Supabase 数据库默认允许外部连接
   - 检查防火墙规则

2. **运行数据库初始化脚本**
   - 确保数据库表已创建
   - 可以在本地运行 `scripts/create_database.sql`

## 验证部署

部署成功后，Vercel 会提供一个 URL，例如：
```
https://learning-platform-xxx.vercel.app
```

访问这个 URL 应该能看到登录页面。

## 常见问题

### 1. 部署后显示 500 错误
- 检查环境变量是否正确设置
- 查看 Vercel 部署日志：Dashboard → Deployments → 点击具体部署 → Runtime Logs

### 2. 数据库连接失败
- 确认数据库允许外部访问
- 检查连接字符串格式是否正确
- 验证数据库凭据

### 3. 静态文件无法加载
- 检查 `vercel.json` 配置
- 确保 static 文件夹路径正确

## 更新部署

### 使用 CLI
```bash
vercel --prod
```

### 使用 GitHub（如果已集成）
```bash
git add .
git commit -m "Update"
git push
```
Vercel 会自动检测推送并重新部署。

## 自定义域名（可选）

1. 在 Vercel Dashboard 进入项目
2. 点击 "Settings" → "Domains"
3. 添加你的自定义域名
4. 按照指示配置 DNS 记录

## 监控和日志

- **访问日志**: Dashboard → 项目 → Deployments → Runtime Logs
- **性能监控**: Dashboard → 项目 → Analytics
- **错误追踪**: 查看 Runtime Logs 中的错误信息

## 回滚部署

如果新部署有问题，可以回滚到之前的版本：

1. Dashboard → 项目 → Deployments
2. 找到之前正常工作的部署
3. 点击三个点 → "Promote to Production"

---

**部署完成！** 🎉

你的学习平台现在已经可以通过互联网访问了。
