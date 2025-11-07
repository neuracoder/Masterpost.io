<<<<<<< HEAD
# 🟢 Masterpost.io - Professional Background Removal SaaS

[![Deploy Status](https://img.shields.io/badge/deploy-vercel-black)](https://vercel.com)
[![Database](https://img.shields.io/badge/database-supabase-green)](https://supabase.com)
[![License](https://img.shields.io/badge/license-proprietary-red)](LICENSE)

Professional background removal for e-commerce. AI-powered bulk processing with credit-based pricing.

**🌐 Website:** [masterpost.io](https://masterpost.io)
**📦 Repository:** [github.com/neuracoder/Masterpost-SaaS](https://github.com/neuracoder/Masterpost-SaaS)

---

## 🚀 Features

- ✅ **Basic Tier** - Local rembg processing ($0.10/image, 1 credit)
- ✅ **Premium Tier** - Qwen AI processing ($0.30/image, 3 credits)
- ✅ **Bulk Processing** - Up to 50 images at once
- ✅ **Multiple Pipelines** - Amazon, eBay, Instagram Ready, Shopify
- ✅ **Credit System** - Flexible pay-as-you-go pricing
- ✅ **User Authentication** - Supabase Auth with JWT tokens
- ✅ **Before/After Gallery** - Showcase slider with 6 example images
- ✅ **Professional Landing** - Green (#10b981) & Yellow (#fbbf24) branding
- 🔜 **Stripe Payments** - Coming in Phase 2

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Frontend** | HTML5, TailwindCSS, Vanilla JavaScript |
| **Backend** | FastAPI (Python 3.11) |
| **Database** | Supabase (PostgreSQL) |
| **Authentication** | Supabase Auth (JWT) |
| **Hosting** | Vercel |
| **AI Processing** | Qwen VL (Alibaba Cloud) |
| **Local Processing** | rembg (Python) |
| **Payments** | Stripe _(Phase 2)_ |

---

## 📦 Quick Start

### Prerequisites

- **Python 3.11+**
- **Supabase account** (free tier works)
- **Qwen API access** (Alibaba Cloud)
- **Node.js** (optional, for frontend development)

### Local Development

```bash
# Clone repository
git clone https://github.com/neuracoder/Masterpost-SaaS.git
cd Masterpost-SaaS

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your credentials

# Run development server
cd backend
uvicorn app.main:app --reload --port 8002

# Open browser
# Frontend: http://localhost:3002
# Backend API Docs: http://localhost:8002/docs
```

---

## 🔧 Environment Setup

### 1. Copy .env.example to .env

```bash
cp .env.example .env
```

### 2. Fill in your credentials

```env
# Supabase (get from https://supabase.com/dashboard)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# Qwen AI (get from https://dashscope.console.aliyun.com/)
QWEN_API_KEY=your-qwen-api-key
QWEN_API_URL=https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation

# URLs
FRONTEND_URL=http://localhost:3002
BACKEND_URL=http://127.0.0.1:8002
ENVIRONMENT=development
```

### 3. Create Supabase tables

Run the SQL from `backend/supabase_setup.sql` in your Supabase SQL Editor.

---

## 📁 Project Structure

```
Masterpost-SaaS/
├── .gitignore              # Git ignore (excludes .env, uploads/, etc.)
├── .env.example            # Environment template (NO real values)
├── README.md               # This file
├── vercel.json             # Vercel deployment configuration
├── backend/
│   ├── requirements.txt    # Python dependencies
│   ├── supabase_setup.sql  # Database schema
│   ├── app/
│   │   ├── main.py         # FastAPI application
│   │   ├── api/            # Credit system endpoints
│   │   │   ├── auth.py     # Signup, login, logout, /me
│   │   │   ├── credits.py  # Balance, use, history
│   │   │   └── payments.py # Stripe checkout (Phase 2)
│   │   ├── core/
│   │   │   ├── config.py   # Settings & environment
│   │   │   ├── supabase.py # Supabase clients
│   │   │   └── stripe_client.py # Stripe client (Phase 2)
│   │   └── routers/        # Legacy/existing routes
│   ├── processing/         # Image processing engines
│   ├── img_original/       # Example gallery images (6 images)
│   └── img_procesada/      # Processed example images (6 images)
└── frontend/
    ├── index.html          # Landing page
    ├── login.html          # Login page (if exists)
    ├── signup.html         # Signup page (if exists)
    ├── css/                # Stylesheets
    └── js/                 # JavaScript files
```

---

## 🎯 API Endpoints

### Authentication (Credit System)

- `POST /api/auth/signup` - Register new user (receives 10 free credits)
- `POST /api/auth/login` - Login user
- `POST /api/auth/logout` - Logout user
- `GET /api/auth/me` - Get current user info

### Credits Management

- `GET /api/credits/balance` - Get credit balance
- `POST /api/credits/use` - Use credits (atomic operation)
- `GET /api/credits/history` - Get transaction history

### Payments (Phase 2 - Coming Soon)

- `GET /api/payments/packs` - List available packs (PRO/BUSINESS)
- `POST /api/payments/create-checkout-session` - Create Stripe checkout
- `POST /api/payments/webhook` - Stripe webhook handler

---

## 🚧 Roadmap

### ✅ **Phase 1 - MVP** (CURRENT)

- [x] Landing page with showcase slider (6 images)
- [x] User authentication (Supabase)
- [x] Credit system database structure
- [x] Before/After gallery with green/yellow branding
- [x] Responsive design (mobile-first)
- [x] Split logo design (green/white with yellow M)
- [x] "Instagram Ready" messaging

### 🔜 **Phase 2 - Payments** (NEXT)

- [ ] Stripe integration
- [ ] Pack purchase (Pro $17.99/200 credits, Business $39.99/500 credits)
- [ ] Webhook handling for automatic credit assignment
- [ ] Payment success/failure pages
- [ ] Stripe test mode → production migration

### 🔜 **Phase 3 - Core Processing** (FUTURE)

- [ ] Image upload & processing
- [ ] Credit deduction on processing
- [ ] Pipeline selection (Amazon, eBay, Instagram, Shopify)
- [ ] Bulk processing (up to 50 images)
- [ ] Download results as ZIP
- [ ] Processing history & analytics

---

## 🌍 Deployment

### Production Deployment on Vercel

**Status:** Ready for deployment
**Target URL:** https://masterpost.io
**Auto-deploy:** ✅ Enabled from `main` branch

#### Deploy Steps:

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: MVP ready for production"
   git remote add origin https://github.com/neuracoder/Masterpost-SaaS.git
   git branch -M main
   git push -u origin main
   ```

2. **Deploy to Vercel**
   - Import repository from GitHub
   - Configure environment variables in Vercel dashboard
   - Deploy

3. **Configure Custom Domain**
   - Point `masterpost.io` to Vercel
   - Enable HTTPS
   - Set CORS for production

---

## 📊 Credit Packs

| Pack | Credits | Price | Cost/Credit | Best For |
|------|---------|-------|-------------|----------|
| **FREE** | 10 | $0.00 | Free | Testing |
| **PRO** | 200 | $17.99 | $0.09 | Small businesses |
| **BUSINESS** | 500 | $39.99 | $0.08 | High-volume sellers |

### Credit Usage

- **Basic Processing**: 1 credit per image (rembg local)
- **Premium Processing**: 3 credits per image (Qwen AI)

---

## 🔐 Security

- ✅ Environment variables excluded from git (`.gitignore`)
- ✅ JWT token authentication via Supabase
- ✅ Row Level Security (RLS) on database tables
- ✅ Input validation on all endpoints
- ✅ CORS properly configured
- ✅ Service role key for admin operations
- ✅ Anon key for client operations

---

## 🛠️ Development

### Backend Development

```bash
cd backend
uvicorn app.main:app --reload --port 8002
```

Access API docs: http://localhost:8002/docs

### Frontend Development

Serve static files with any HTTP server:

```bash
# Option 1: Python
python -m http.server 3002

# Option 2: Node.js
npx serve -p 3002

# Option 3: VS Code Live Server
```

---

## 📝 License

**Proprietary** - All rights reserved © 2025 Neuracoder
Not licensed for distribution or commercial use without permission.

---

## 👤 Author

**Martín Javier Galant**
Senior Python & .NET Developer | IT Systems Specialist

- 🌐 Website: [neuracoder.com](https://neuracoder.com)
- 💼 LinkedIn: [linkedin.com/in/martingalant](https://linkedin.com/in/martingalant)
- 📧 Email: [info@neuracoder.com](mailto:info@neuracoder.com)
- 🐙 GitHub: [@neuracoder](https://github.com/neuracoder)

---

## 📞 Support

- **Documentation:** API docs at `/docs` endpoint
- **Issues:** [GitHub Issues](https://github.com/neuracoder/Masterpost-SaaS/issues)
- **Email:** [info@neuracoder.com](mailto:info@neuracoder.com)

---

<div align="center">

**Built with ❤️ by [Neuracoder](https://neuracoder.com)**

🟢 🟡 ⚪

*Transform backgrounds, transform business*

</div>
=======
---
title: Masterpost Worker
emoji: 🏃
colorFrom: gray
colorTo: indigo
sdk: docker
pinned: false
short_description: rofessional background removal for e-commerce. AI-powered bu
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference
>>>>>>> 1a8ac258323ec51c3de2092b6a5fc8e344625f35
