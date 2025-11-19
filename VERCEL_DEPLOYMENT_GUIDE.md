# Vercel Deployment Guide

## Prerequisites
- Vercel account (free)
- Git repository (GitHub, GitLab, or Bitbucket)
- Vercel CLI installed (optional, for local deployment)

## Step 1: Prepare Your Project

### 1.1 Update Database Configuration
The project has been configured to work with both local PostgreSQL and Vercel Postgres:
- Local: Uses environment variables from `.env` file
- Vercel: Uses `POSTGRES_URL` environment variable

### 1.2 Required Files Created
- `vercel.json` - Vercel configuration
- `wsgi.py` - WSGI entry point
- Updated `requirements.txt` with specific versions
- Updated `config.py` for Vercel compatibility
- Updated `app.py` to use environment variables

## Step 2: Set Up Vercel Postgres

### 2.1 Create Vercel Postgres Database
1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "Storage" → "Create Database"
3. Select "Postgres" and create your database
4. Note down the connection string

### 2.2 Configure Environment Variables
In your Vercel project settings, add these environment variables:
```
POSTGRES_URL=your_vercel_postgres_connection_string
SECRET_KEY=your_secret_key_here
FLASK_APP=app.py
FLASK_ENV=production
VERCEL=true
```

## Step 3: Deploy to Vercel

### Option A: Git Integration (Recommended)
1. Push your code to GitHub/GitLab/Bitbucket
2. Go to [Vercel Dashboard](https://vercel.com/dashboard)
3. Click "New Project"
4. Import your Git repository
5. Configure environment variables
6. Deploy

### Option B: Vercel CLI
```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy
vercel --prod
```

## Step 4: Database Setup

### 4.1 Initialize Database Schema
After deployment, you need to run the database initialization:

```bash
# Connect to Vercel Postgres using the connection string
# Run your SQL schema files to create tables
```

### 4.2 Alternative: Use Vercel Functions for Schema Setup
Create a deployment script that runs once to set up your database schema.

## Step 5: Post-Deployment Configuration

### 5.1 Update Application URLs
Update any hardcoded URLs in your application to use your Vercel deployment URL.

### 5.2 Configure CORS (if needed)
Add CORS configuration for any external API calls.

## Step 6: Verify Deployment

### 6.1 Test Core Functionality
- User registration/login
- Course creation/management
- Quiz/poll functionality
- Database operations

### 6.2 Monitor Logs
Check Vercel function logs for any errors or warnings.

## Troubleshooting

### Common Issues

#### 1. Database Connection Errors
- Verify `POSTGRES_URL` environment variable is set correctly
- Check Vercel Postgres is properly configured
- Ensure database schema is initialized

#### 2. Template Not Found Errors
- Verify all template files are in the `templates/` directory
- Check template references in route files
- Ensure static files are properly served

#### 3. Import Errors
- Check all dependencies are listed in `requirements.txt`
- Verify import paths are correct
- Ensure all model files are properly imported

#### 4. Static Files Not Loading
- Check static file paths in templates
- Verify static files are in the `static/` directory
- Check Vercel configuration for static file serving

### Performance Optimization
- Enable caching for static assets
- Optimize database queries
- Use connection pooling for database connections
- Consider using Vercel Edge Functions for API routes

## Environment-Specific Configuration

### Development (Local)
Create a `.env` file:
```
PG_DB_USER=your_local_user
PG_DB_PASSWORD=your_local_password
PG_DB_HOST=localhost
PG_DB_PORT=5432
PG_DB_NAME=your_local_db
SECRET_KEY=your_local_secret_key
```

### Production (Vercel)
Set these in Vercel project settings:
```
POSTGRES_URL=your_vercel_postgres_connection_string
SECRET_KEY=your_production_secret_key
FLASK_APP=app.py
FLASK_ENV=production
VERCEL=true
```

## Additional Notes
- Vercel has a 10-second timeout for serverless functions
- Consider splitting large operations into smaller chunks
- Use Vercel's built-in analytics for monitoring
- Set up proper error handling and logging
- Consider implementing rate limiting for API endpoints

## Support
For issues specific to this deployment, check:
- Vercel documentation: https://vercel.com/docs
- Flask documentation: https://flask.palletsprojects.com/
- PostgreSQL documentation: https://www.postgresql.org/docs/