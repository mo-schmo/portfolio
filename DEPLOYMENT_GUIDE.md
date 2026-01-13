# Portfolio Deployment Guide

This guide will walk you through deploying your backend to **Northflank** (Free Tier) and your frontend to **Vercel**.

## Backend Deployment (Northflank)

Northflank is recommended because it offers a generous free tier (Developer Sandbox) that supports Docker, WebSockets, and persistent volumes for SQLite.

### 1. Create a Project
- Log in to [Northflank](https://northflank.com/).
- Create a new project (e.g., `portfolio-prod`).

### 2. Deployment Service
- Click **"Create New"** -> **"Service"** -> **"Combined Service"**.
- Select **"GitHub"** as your source and pick your `portfolio` repository.
- **Build Settings**:
    - **Build Type**: Dockerfile.
    - **Context Path**: `/backend` (Select the backend folder).
- **Environment Variables**:
    - `PORT`: `8080`
    - `DB_PATH`: `/app/data/portfolio.db`

### 3. Add Persistent Storage (Volume)
Since SQLite needs to keep your data between restarts:
- In your Service settings, go to **"Volumes"**.
- Click **"Add Volume"**.
- Set the mount path to: `/app/data`
- Give it a name (e.g., `sqlite-data`) and select a size (1GB is plenty for the free tier).

### 4. Network and Ports
- Go to the **"Networking"** tab.
- Add a port: `8080`.
- Set it to **"Public"** and **"HTTP"** (Northflank handles SSL/HTTPS for you automatically).

---

## Frontend Deployment (Vercel)

Vercel is the best home for SvelteKit applications.

### 1. Connect Project
- Log in to your [Vercel Dashboard](https://vercel.com/).
- Click **"Add New"** -> **"Project"**.
- Select your `portfolio` repository.

### 2. Project Settings
- **Root Directory**: Select the `frontend` folder.
- **Framework Preset**: SvelteKit.

### 3. Environment Variables
Add the following variables to connect to your live backend (get your Northflank URL from your service dashboard):
- `PUBLIC_API_URL`: `https://your-service-id.northflank.app/api`
- `PUBLIC_WS_URL`: `wss://your-service-id.northflank.app/ws`

### 4. Deploy
Click **Deploy**. SvelteKit will build the static/node assets and your app will be live!

> [!TIP]
> Make sure to update your `PUBLIC_API_URL` and `PUBLIC_WS_URL` once Northflank gives you your stable `.northflank.app` domain.
