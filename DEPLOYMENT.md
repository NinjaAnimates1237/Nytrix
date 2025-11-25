# Deploy EchoForge to a Public URL

## Option 1: Deploy to Railway (Recommended - Free)

1. **Create a Railway account**: Go to https://railway.app and sign up with GitHub

2. **Install Railway CLI**:
```bash
npm install -g @railway/cli
railway login
```

3. **Initialize Railway in your project**:
```bash
cd /Users/lennyyohannan/Downloads/EchoForge
railway init
```

4. **Add a Procfile** (already created below)

5. **Deploy**:
```bash
railway up
```

6. **Add a custom domain** (in Railway dashboard):
   - Go to your project → Settings → Domains
   - Click "Generate Domain" for a free railway.app subdomain
   - Or add your own custom domain

---

## Option 2: Deploy to Render (Free)

1. **Create account**: Go to https://render.com and sign up

2. **Create a new Web Service**:
   - Connect your GitHub repository (or upload code)
   - Select "Python" environment
   - Build command: `pip install -r requirements.txt && cd client && npm install && npm run build && cd ..`
   - Start command: `python run.py`
   - Add environment variables from `.env` file

3. **Your app will be live at**: `https://your-app-name.onrender.com`

---

## Option 3: Use Ngrok (Quick Test - Temporary URL)

1. **Install ngrok**:
```bash
brew install ngrok
```

2. **Start your app locally**:
```bash
cd /Users/lennyyohannan/Downloads/EchoForge
source venv/bin/activate
python run.py
```

3. **In another terminal, expose it**:
```bash
ngrok http 6767
```

4. **Copy the public URL** (e.g., `https://abc123.ngrok.io`) and share it!

⚠️ Ngrok URLs expire when you close the terminal

---

## Option 4: Deploy to DigitalOcean App Platform

1. **Create account**: https://cloud.digitalocean.com

2. **Create new App**:
   - Connect GitHub or upload code
   - Select Python as runtime
   - Build command: `pip install -r requirements.txt && cd client && npm install && npm run build`
   - Run command: `python run.py`

3. **Add domain**: Get free .ondigitalocean.app subdomain or use custom domain

---

## Important: Update CORS Settings

After deployment, update your `.env` file:

```env
CORS_ORIGINS=https://your-public-url.com,http://localhost:6767
```

Or set environment variables in your hosting platform dashboard.

---

## Need Help?

- Railway docs: https://docs.railway.app/
- Render docs: https://render.com/docs
- Ngrok docs: https://ngrok.com/docs
