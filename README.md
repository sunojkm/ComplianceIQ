# ComplianceIQ

**Automated ISO 27001 Annex A Security Risk Assessment Tool for Small and Micro Businesses**

[![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.x-black?logo=flask)](https://flask.palletsprojects.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Phase%202%20Complete-green)]()
[![GitHub](https://img.shields.io/badge/GitHub-sunojkm%2FComplianceIQ-lightgrey?logo=github)](https://github.com/sunojkm/ComplianceIQ)

---

## What is ComplianceIQ?

ComplianceIQ is a free, open-source, web-based security risk assessment tool designed for small and micro businesses (1–50 employees). It guides organisations through a structured 43-question assessment mapped directly to **ISO/IEC 27001:2022 Annex A** controls — covering all four control themes:

- **Organisational** — 15 questions (A.5.x controls)
- **People** — 5 questions (A.6.x controls)
- **Physical** — 8 questions (A.7.x controls)
- **Technological** — 15 questions (A.8.x controls)

No compliance expertise required. Any business owner who understands English can complete a full ISO 27001 gap assessment and receive a prioritised action plan.

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

### Current (Phase 2 — Complete)
- ✅ User registration and login with company onboarding
- ✅ Industry and business size selection
- ✅ 43-question ISO 27001 Annex A assessment — one question per page
- ✅ Progress bar tracking across all questions
- ✅ Weighted scoring engine — criticality weights 1 (Advisory), 2 (Important), 3 (Critical)
- ✅ Theme-level risk scores — Organisational, People, Physical, Technological
- ✅ Overall compliance percentage with four-tier risk classification
- ✅ Colour-coded risk banner — Low / Medium / High / Critical
- ✅ Identified weaknesses accordion — expandable list of failed controls
- ✅ Recommended control checklist accordion — specific remediation per control
- ✅ Password show/hide toggle on login and register pages
- ✅ Forgot password placeholder page
- ✅ CSRF protection (Flask-WTF)
- ✅ HTTP security headers (Flask-Talisman)
- ✅ Secure password hashing (Werkzeug bcrypt)

### Planned (Phase 4 — Weeks 9–13)
- 🔲 Chart.js radar dashboard — theme-level compliance visualisation
- 🔲 FPDF2 PDF report — downloadable weaknesses report + control checklist
- 🔲 Deployment to Render with PostgreSQL
- 🔲 Password reset via Flask-Mail with email token
- 🔲 Assessment history and progress tracking

---

## Risk Classification

| Risk Level | Score Range | Meaning |
|---|---|---|
| 🟢 Low | 80–100% | Strong compliance — most controls in place |
| 🟡 Medium | 60–79% | Reasonable posture with notable gaps |
| 🟠 High | 40–59% | Significant gaps — elevated risk |
| 🔴 Critical | 0–39% | Severe gaps — immediate action required |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11+, Flask |
| Authentication | Flask-Login, Werkzeug (bcrypt) |
| Security | Flask-WTF (CSRF), Flask-Talisman (HTTP headers) |
| Database | SQLite (dev) → PostgreSQL on Render (production) |
| ORM | SQLAlchemy |
| Frontend | HTML, Tailwind CSS (CDN) |
| Charts | Chart.js (planned) |
| PDF Reports | FPDF2 (planned) |
| Deployment | Render (planned) |
| Testing | Pytest (planned) |

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
pip install flask flask-sqlalchemy flask-login flask-wtf flask-talisman werkzeug fpdf2
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
├── run.py                          # Application entry point
├── app/
│   ├── __init__.py                 # Application factory — Flask, SQLAlchemy, blueprints
│   ├── models.py                   # Database models — User, Assessment, Response
│   ├── questions.py                # All 43 ISO 27001 Annex A questions
│   ├── auth.py                     # Authentication blueprint — register, login, logout
│   ├── main.py                     # Main blueprint — dashboard
│   ├── assessment.py               # Assessment blueprint — questionnaire, scoring, results
│   ├── templates/
│   │   ├── base.html               # Base template — navigation and layout
│   │   ├── auth/
│   │   │   ├── login.html          # Login page
│   │   │   ├── register.html       # Registration page
│   │   │   └── forgot_password.html# Forgot password placeholder
│   │   ├── main/
│   │   │   └── dashboard.html      # User dashboard
│   │   └── assessment/
│   │       ├── question.html       # Individual question page
│   │       └── results.html        # Assessment results with accordions
│   └── static/
│       ├── css/                    # Custom stylesheets
│       └── js/                     # Custom scripts
├── tests/                          # Pytest test suite (planned)
├── .gitignore                      # Excludes venv, db, .env, __pycache__
└── README.md                       # This file
```

---

## How It Works

### 1. Register
Create an account with your company name, industry, business size, email, and password.

### 2. Start Assessment
Click **Start Assessment** on the dashboard to begin the 43-question ISO 27001 Annex A questionnaire.

### 3. Answer Questions
Each question maps to a specific ISO 27001 Annex A control. The control reference, theme, and criticality weight are displayed alongside the question. Answer **YES** or **NO**.

### 4. View Results
After completing all 43 questions, the results page displays:
- Your overall compliance percentage and risk level
- **Identified Weaknesses** — every failed control listed by theme and criticality
- **Recommended Control Checklist** — specific ISO 27001 remediation action for each gap

---

## Question Scope

ISO 27001:2022 Annex A contains 93 controls in total. The MVP covers 43 — selected by **criticality weight** and **SMB applicability**. This prioritises controls with the highest impact on security posture while excluding controls impractical for organisations of 1–50 employees.

This approach is consistent with how GRC consultants scope ISO 27001 assessments for smaller organisations — addressing the highest-risk controls first and expanding coverage incrementally.

**The remaining 50 controls are on the roadmap** for post-course community contributions.

---

## Security

ComplianceIQ is built following **OWASP secure coding guidelines**, reflecting ISO 27001 A.8.26 (Application Security) in practice:

- All passwords hashed with **Werkzeug bcrypt** — never stored in plaintext
- **Flask-WTF** provides CSRF token protection on all forms
- **Flask-Talisman** enforces HTTP security headers (CSP, HSTS, X-Frame-Options)
- `.env` file excluded from version control via `.gitignore`
- **pip-audit** used periodically to scan for vulnerable dependencies

---

## Roadmap

### Phase 4 — Dashboard, PDF & Deployment (Weeks 9–13)
- Chart.js radar chart showing theme-level compliance scores
- FPDF2 downloadable PDF report (weaknesses report + control checklist)
- Full deployment to Render with PostgreSQL
- Password reset via Flask-Mail

### Post-Course Expansions
- **Remaining 50 ISO 27001 controls** — full Annex A coverage across all 93 controls
- **NIST CSF 2.0 gap-fill layer** — supplementary recommendations where ISO 27001 falls short (detection, response, governance)
- **GDPR compliance module** — for EU-based organisations
- **HIPAA** — healthcare data protection (community contribution)
- **PCI-DSS** — payment card security (community contribution)
- **SOC 2** — technology and SaaS (community contribution)
- **HITRUST** — healthcare enterprise (community contribution)

All planned expansions are tracked in [ROADMAP.md](ROADMAP.md).

---

## Licence

This project is licensed under the **MIT Licence** — see [LICENSE](LICENSE) for details.

You are free to use, modify, and distribute this software for any purpose, including commercial use, provided the original licence and copyright notice are retained.

---

## Acknowledgements

- [ISO/IEC 27001:2022](https://www.iso.org/standard/27001) — Information Security Management Standard
- [Flask](https://flask.palletsprojects.com) — Lightweight Python web framework
- [Tailwind CSS](https://tailwindcss.com) — Utility-first CSS framework
- [OWASP](https://owasp.org) — Secure coding guidelines

---

*Built with Python and Flask · Open source under MIT Licence · github.com/sunojkm/ComplianceIQ*