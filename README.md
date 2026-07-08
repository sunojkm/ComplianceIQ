# ComplianceIQ

**Automated ISO 27001 Annex A Security Risk Assessment Tool for Small and Micro Businesses**

[![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.x-black?logo=flask)](https://flask.palletsprojects.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Live%20%E2%9C%85-brightgreen)]()
[![Live Demo](https://img.shields.io/badge/Live%20Demo-complianceiq--dsgi.onrender.com-yellow)](https://complianceiq-dsgi.onrender.com)
[![GitHub](https://img.shields.io/badge/GitHub-sunojkm%2FComplianceIQ-lightgrey?logo=github)](https://github.com/sunojkm/ComplianceIQ)

---

## 🔗 Live Demo

**[https://complianceiq-dsgi.onrender.com](https://complianceiq-dsgi.onrender.com)**

---

## What is ComplianceIQ?

ComplianceIQ is a free, open-source, web-based security risk assessment tool designed for small and micro businesses (1–50 employees). It guides organisations through a structured 43-question assessment mapped directly to **ISO/IEC 27001:2022 Annex A** controls — covering all four control themes:

- **Organisational** — 15 questions (A.5.x controls)
- **People** — 5 questions (A.6.x controls)
- **Physical** — 8 questions (A.7.x controls)
- **Technological** — 15 questions (A.8.x controls)

No compliance expertise required. Any business owner who understands English can complete a full ISO 27001 gap assessment and receive a prioritised action plan — for free.

---

## The Problem It Solves

ISO 27001 is the world's most adopted information security management standard — yet small businesses rarely implement its controls. The barrier is not cost (ISO 27001 is publicly available) but **accessibility**.

Conducting a proper gap assessment traditionally requires:
- A qualified information security consultant
- The ability to interpret 93 technical controls across four themes
- Hours of structured audit work

Enterprise GRC platforms (ServiceNow GRC, OneTrust) cost thousands per year and are built for large teams. ComplianceIQ makes ISO 27001 gap assessment accessible to any organisation — for free.

---

## Features

### ✅ Currently Live

**Authentication & Onboarding**
- Landing page with tool overview and risk classification guide
- User registration with company name, industry, business size
- Login with show/hide password toggle
- Rate-limited login — 5 attempts per minute (brute force protection)
- Privacy disclaimer on registration
- Logout redirects to landing page

**Assessment Engine**
- 43-question ISO 27001 Annex A assessment — one question per page
- Progress bar tracking across all 43 questions
- Completion popup after final question
- Weighted scoring engine — criticality weights 1 (Advisory), 2 (Important), 3 (Critical)
- Theme-level risk scores — Organisational, People, Physical, Technological
- Overall compliance percentage with four-tier risk classification

**Results & Reporting**
- Colour-coded risk banner — Low / Medium / High / Critical
- Chart.js radar chart — theme-level compliance visualisation
- Theme-level progress bars with colour coding
- Identified weaknesses accordion — expandable per control with criticality badge
- Recommended control checklist accordion — expandable per control with remediation action
- PDF report download — identified weaknesses + recommended control checklist
- Download popup with spinner and completion confirmation

**Dashboard & History**
- User dashboard with previous assessments list
- View any past assessment report
- Delete assessment with double confirmation (type DELETE to confirm)
- Profile page — update company details and change password
- Assessment count and account information

**Security (OWASP Guidelines — ISO 27001 A.8.26)**
- Passwords hashed with Werkzeug bcrypt — never stored in plaintext
- CSRF protection via Flask-WTF on all forms
- HTTP security headers via Flask-Talisman (CSP, HSTS, X-Frame-Options)
- Rate limiting on login via Flask-Limiter
- Secret key stored as environment variable — not in source code
- `.gitignore` excludes `.env`, `.db`, `venv/`, `__pycache__/`

### 🔲 Post-Course Roadmap

- Remaining 50 ISO 27001 Annex A controls — full Annex A coverage (93 controls)
- NIST CSF 2.0 gap-fill layer — supplementary recommendations where ISO 27001 falls short
- GDPR compliance module — for EU-based organisations
- HIPAA, PCI-DSS, SOC 2, HITRUST — community contributions for broader industry coverage
- AI-assisted scoring layer
- Public REST API for GRC analyst integrations

All planned expansions are documented in [ROADMAP.md](ROADMAP.md).

---

## Risk Classification

| Risk Level | Score Range | Meaning | Action |
|---|---|---|---|
| 🟢 Low | 80–100% | Strong compliance — most controls in place | Maintain and schedule annual review |
| 🟡 Medium | 60–79% | Reasonable posture with notable gaps | Address gaps within 3 months |
| 🟠 High | 40–59% | Significant gaps — elevated risk | Prioritise Critical controls immediately |
| 🔴 Critical | 0–39% | Severe gaps — immediate action required | Escalate to management now |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11+, Flask |
| Authentication | Flask-Login, Werkzeug (bcrypt) |
| Security | Flask-WTF (CSRF), Flask-Talisman (HTTP headers), Flask-Limiter (rate limiting) |
| Database | SQLite (dev) → PostgreSQL on Render (production) |
| ORM | SQLAlchemy |
| Frontend | HTML, Tailwind CSS (CDN) |
| Charts | Chart.js (CDN) |
| PDF Reports | FPDF2 |
| Deployment | Render (free tier) |
| Version Control | GitHub (MIT licence) |

---

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Git

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/sunojkm/ComplianceIQ.git
cd ComplianceIQ
```

**2. Create a virtual environment**
```bash
python -m venv venv
```

**3. Activate the virtual environment**

Windows:
```bash
venv\Scripts\activate
```

Mac / Linux:
```bash
source venv/bin/activate
```

**4. Install dependencies**
```bash
pip install -r requirements.txt
```

**5. Run the application**
```bash
python run.py
```

**6. Open your browser**
```
http://127.0.0.1:5000
```

---

## Project Structure

```
ComplianceIQ/
├── run.py                              # Application entry point
├── requirements.txt                    # Python dependencies
├── render.yaml                         # Render deployment config
├── app/
│   ├── __init__.py                     # Application factory
│   ├── models.py                       # Database models — User, Assessment, Response
│   ├── questions.py                    # All 43 ISO 27001 Annex A questions
│   ├── pdf_report.py                   # FPDF2 PDF report generator
│   ├── auth.py                         # Auth blueprint — register, login, logout, landing
│   ├── main.py                         # Main blueprint — dashboard, profile
│   ├── assessment.py                   # Assessment blueprint — questionnaire, scoring, results
│   ├── templates/
│   │   ├── base.html                   # Base template — navigation bar
│   │   ├── auth/
│   │   │   ├── landing.html            # Landing page
│   │   │   ├── login.html              # Login page
│   │   │   ├── register.html           # Registration page
│   │   │   └── forgot_password.html    # Forgot password placeholder
│   │   ├── main/
│   │   │   ├── dashboard.html          # User dashboard with history
│   │   │   └── profile.html            # Profile and password change
│   │   └── results/
│   │       └── results.html            # Assessment results with chart and accordions
│   └── static/
│       ├── css/                        # Custom stylesheets
│       └── js/                         # Custom scripts
├── .gitignore                          # Excludes venv, db, .env, __pycache__
├── README.md                           # This file
└── ROADMAP.md                          # Post-course expansion plan
```

---

## How It Works

### 1. Land & Register
Visit the landing page to learn about the tool. Register with your company name, industry, business size, email, and password.

### 2. Start Assessment
Click **Start New Assessment** on the dashboard to begin the 43-question ISO 27001 Annex A questionnaire.

### 3. Answer Questions
Each question shows the ISO 27001 control reference, theme, and criticality badge (red Critical / yellow Important / green Advisory). Answer **YES** or **NO**. A progress bar tracks your position through all 43 questions.

### 4. View Results
After completing all questions, the results page shows:
- Overall compliance percentage and risk level
- Radar chart and theme-level progress bars
- **Identified Weaknesses** — every failed control by theme and criticality
- **Recommended Control Checklist** — specific ISO 27001 remediation action per gap

### 5. Download PDF Report
Click **Download PDF Report** to get a branded PDF containing your weaknesses report and recommended control checklist.

### 6. Track Progress
Return to the dashboard to view past assessments, compare scores over time, or start a new assessment after implementing controls.

---

## Question Scope

ISO 27001:2022 Annex A contains 93 controls. The MVP covers 43 — selected by **criticality weight** and **SMB applicability**. This prioritises controls with the highest impact on security posture while excluding controls impractical for 1–50 employee organisations.

The remaining 50 controls are on the post-course roadmap for community contribution.

---

## Security

Built following **OWASP secure coding guidelines** — reflecting ISO 27001 A.8.26 (Application Security) in practice:

- Passwords hashed with **Werkzeug bcrypt** — never stored in plaintext
- **Flask-WTF** provides CSRF token protection on all forms
- **Flask-Talisman** enforces HTTP security headers (CSP, HSTS, X-Frame-Options)
- **Flask-Limiter** rate limits login to 5 attempts per minute
- Secret key stored as **environment variable** — not in source code
- `.gitignore` excludes `.env`, `.db`, and `venv/` from version control

---

## Deployment

The application is deployed on **Render** (free tier):

- **Live URL:** https://complianceiq-dsgi.onrender.com
- **Database:** SQLite (local) / PostgreSQL (Render)
- **Start Command:** `gunicorn run:app`
- **Auto-deploy:** Every push to `main` branch triggers a new deployment

> Note: Free Render instances spin down after periods of inactivity. The app may take 30–60 seconds to wake up on first visit.

---

## Roadmap

See [ROADMAP.md](ROADMAP.md) for the full post-course expansion plan including:
- Remaining 50 ISO 27001 Annex A controls
- NIST CSF 2.0 gap-fill layer
- GDPR compliance module
- HIPAA, PCI-DSS, SOC 2, HITRUST (community contributions)

---

## Licence

This project is licensed under the **MIT Licence** — see [LICENSE](LICENSE) for details.

You are free to use, modify, and distribute this software for any purpose, including commercial use, provided the original licence and copyright notice are retained.

---

## Acknowledgements

- [ISO/IEC 27001:2022](https://www.iso.org/standard/27001) — Information Security Management Standard
- [Flask](https://flask.palletsprojects.com) — Lightweight Python web framework
- [Tailwind CSS](https://tailwindcss.com) — Utility-first CSS framework
- [Chart.js](https://www.chartjs.org) — JavaScript charting library
- [FPDF2](https://py-fpdf2.readthedocs.io) — Python PDF generation library
- [OWASP](https://owasp.org) — Secure coding guidelines

---

*Built with Python and Flask · Open source under MIT Licence · Live at [complianceiq-dsgi.onrender.com](https://complianceiq-dsgi.onrender.com)*
