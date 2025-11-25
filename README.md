# EchoForge - Mini Discord Clone 🚀

A full-stack real-time chat application with user authentication, friend system, channels, and direct messaging - built with Python Flask and React!

## ✨ Features

- **User Authentication** - Secure registration and login with JWT tokens
- **Friend System** - Send/receive friend requests, manage friends list
- **Real-time Messaging** - Instant messaging with Socket.IO
- **Channels** - Create and join public channels
- **Direct Messages** - Private conversations with friends
- **Online Status** - See who's online in real-time
- **Modern UI** - Discord-inspired interface

## 🛠️ Tech Stack

### Backend
- **Python 3.11+**
- **Flask** - Web framework
- **Flask-SocketIO** - Real-time communication
- **SQLAlchemy** - Database ORM
- **JWT** - Authentication
- **PostgreSQL/SQLite** - Database

### Frontend
- **React 18**
- **Vite** - Build tool
- **Socket.IO Client** - Real-time updates
- **React Router** - Navigation
- **Axios** - HTTP client

## 📦 Installation

### Prerequisites
- Python 3.11+
- Node.js 18+
- npm or yarn

### Quick Start

1. **Clone the repository**
```bash
cd /Users/lennyyohannan/Downloads/EchoForge
```

2. **Set up the backend**
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env and set your SECRET_KEY and JWT_SECRET_KEY

# Run the server
python run.py
```

The backend will start on `http://localhost:5000`

3. **Set up the frontend**
```bash
# In a new terminal
cd client

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will start on `http://localhost:3000`

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

This will start:
- Backend API on port 5000
- Frontend on port 3000
- PostgreSQL database on port 5432

## 🌍 Deployment with Custom Domain

### Option 1: Railway (Easy & Free Tier Available)

1. **Install Railway CLI**
```bash
npm install -g @railway/cli
```

2. **Deploy**
```bash
railway login
railway init
railway up
```

3. **Add Custom Domain**
- Go to Railway dashboard
- Select your project
- Settings → Domains → Add custom domain
- Follow DNS configuration instructions

### Option 2: Render (Free Tier Available)

1. **Backend Deployment**
- Create account on Render.com
- New → Web Service
- Connect your GitHub repository
- Build Command: `pip install -r requirements.txt`
- Start Command: `python run.py`
- Add environment variables from `.env.example`

2. **Frontend Deployment**
- New → Static Site
- Build Command: `cd client && npm install && npm run build`
- Publish Directory: `client/dist`

3. **Custom Domain**
- In Render dashboard → Settings → Custom Domains
- Add your domain and configure DNS

### Option 3: DigitalOcean App Platform

1. Create app from GitHub repository
2. Configure components:
   - **Backend**: Python app, port 5000
   - **Frontend**: Static site from `client/dist`
   - **Database**: PostgreSQL
3. Add environment variables
4. Deploy and add custom domain in settings

### DNS Configuration

For custom domain, add these DNS records:

```
Type    Name    Value
A       @       <your-server-ip>
CNAME   www     yourdomain.com
```

## 🔐 Environment Variables

Create a `.env` file in the root directory:

```env
FLASK_APP=app.py
FLASK_ENV=production
SECRET_KEY=your-super-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
DATABASE_URL=postgresql://user:password@host:5432/echoforge
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

## 📱 Usage

1. **Register** a new account
2. **Search for users** and send friend requests
3. **Accept friend requests** from the Pending tab
4. **Create channels** for group discussions
5. **Send direct messages** to friends
6. **Enjoy real-time chatting!**

## 🧪 Development

### Backend Structure
```
├── app.py              # Flask app factory
├── run.py              # Application entry point
├── config.py           # Configuration
├── models.py           # Database models
├── socket_events.py    # Socket.IO event handlers
└── routes/
    ├── auth.py         # Authentication routes
    ├── friends.py      # Friend system routes
    ├── messages.py     # Messaging routes
    └── channels.py     # Channel routes
```

### Frontend Structure
```
client/
├── src/
│   ├── components/     # React components
│   ├── pages/          # Page components
│   ├── context/        # React context (Auth, Socket)
│   └── App.jsx         # Main app component
└── vite.config.js      # Vite configuration
```

## 🚀 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login
- `GET /api/auth/me` - Get current user

### Friends
- `GET /api/friends` - Get friends list
- `GET /api/friends/search?query=username` - Search users
- `POST /api/friends/request/:userId` - Send friend request
- `POST /api/friends/accept/:requestId` - Accept request
- `POST /api/friends/decline/:requestId` - Decline request

### Messages
- `GET /api/messages/dm/:userId` - Get DM history
- `GET /api/messages/channel/:channelId` - Get channel messages

### Channels
- `GET /api/channels` - Get all channels
- `POST /api/channels` - Create channel
- `POST /api/channels/:id/join` - Join channel

## 🎯 Roadmap

- [ ] Voice channels
- [ ] File uploads
- [ ] Message reactions
- [ ] User roles and permissions
- [ ] Push notifications
- [ ] Mobile app

## 📄 License

MIT License - feel free to use this project for learning or commercial purposes!

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## 📧 Support

For issues or questions, please open a GitHub issue.

---

Made with ❤️ by EchoForge Team
