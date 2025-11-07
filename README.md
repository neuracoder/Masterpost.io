---
title: Masterpost Worker
emoji: 🎨
colorFrom: green
colorTo: yellow
sdk: docker
pinned: false
app_port: 8002
---

# 🟢 Masterpost.io - Professional Background Removal Worker

Professional background removal service for e-commerce. AI-powered bulk processing with credit-based pricing.

**🌐 Main Website:** [masterpost.io](https://masterpost.io)
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

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Frontend** | HTML5, TailwindCSS, Vanilla JavaScript |
| **Backend** | FastAPI (Python 3.11) |
| **Database** | Supabase (PostgreSQL) |
| **Authentication** | Supabase Auth (JWT) |
| **Hosting** | Hugging Face Spaces |
| **AI Processing** | Qwen VL (Alibaba Cloud) |
| **Local Processing** | rembg (Python) |
| **Payments** | Stripe |

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

### Payments

- `GET /api/payments/packs` - List available packs (PRO/BUSINESS)
- `POST /api/payments/create-checkout-session` - Create Stripe checkout
- `POST /api/payments/webhook` - Stripe webhook handler

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

- ✅ Environment variables properly configured
- ✅ JWT token authentication via Supabase
- ✅ Row Level Security (RLS) on database tables
- ✅ Input validation on all endpoints
- ✅ CORS properly configured
- ✅ Service role key for admin operations
- ✅ Anon key for client operations

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

<div align="center">

**Built with ❤️ by [Neuracoder](https://neuracoder.com)**

🟢 🟡 ⚪

*Transform backgrounds, transform business*

</div>
