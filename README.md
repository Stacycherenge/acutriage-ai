#  AcuTriage AI: Multi-Modal Emergency Severity Index (ESI) Platform

[![FastAPI](https://shields.io)](https://tiangolo.com)
[![PyTorch](https://shields.io)](https://pytorch.org)
[![PostgreSQL](https://shields.io)](https://postgresql.org)
[![Security](https://shields.io)](https://jwt.io)

AcuTriage AI is a production-grade, secure-by-design healthcare microservice engineered to mitigate clinical overcrowding in emergency rooms and rural health networks. By combining immediate physiological vital tracks, continuous tracking metrics, long-term chronic disease flags, and unstructured free-text nurse narratives, the platform replaces traditional "black box" diagnostic algorithms with a high-performance **Multi-Modal Deep Learning Classification Engine (94.64% Validation Accuracy)** wrapped in game-theoretic feature attribution explainability maps (**SHAP**).


## System Architecture Blueprint

The ecosystem is built using a highly decoupled, **Modular Layered Architecture** that isolates data persistence from domain business logic via a strict dependency-injected execution path.
[ REACT FRONTEND SPA ]│(HTTP REST / JSON Payloads)│┌─────────────────────────▼──────────────────────────┐│ 1. ROUTERS LAYER (routers/patient.py)              ││    - Accepts requests & enforces HTTP endpoints    │└─────────────────────────┬──────────────────────────┘│ (Passes Pydantic Schemas)┌─────────────────────────▼──────────────────────────┐│ 2. SERVICES LAYER (services/patient.py)            ││    - Coordinates ML inference (PyTorch Runtime)    ││    - Enforces core healthcare business logic       │└─────────────────────────┬──────────────────────────┘│ (Calls Abstract Queries)┌─────────────────────────▼──────────────────────────┐│ 3. REPOSITORIES LAYER (repositories/patient.py)   ││    - Executes raw database transactions            │└─────────────────────────┬──────────────────────────┘│ (Mutates Python Objects)┌─────────────────────────▼──────────────────────────┐│ 4. DATABASE & MODELS LAYER (models/patient.py)     ││    - PostgreSQL instance via SQLAlchemy Async      │└────────────────────────────────────────────────────┘


## Core Cybersecurity Specs (Secure-by-Design)
* **Asymmetric Token Security:** Authorization utilizes asymmetric **RS256 JWT tokens**. The authorization provider retains the secure private key while this microservice uses the corresponding public key to verify signatures without exposing credentials.
* **Role-Based Access Control (RBAC):** Strict operational boundaries are enforced via dynamic backend interceptors:
  * `Junior Nurse`: Authorized for patient vital intake submissions and live AI triage generation.
  * `Attending Physician`: Authorized for diagnostic dashboards, historic trend line analysis, and **SHAP** graph reviews.
  * `System Administrator`: Full clearance to add/revoke staff credentials and inspect database logs.
* **Storage Defenses:** Ingestion filters strictly check bounds (e.g., rejecting physical anomalies like an SpO₂ > 100%) and password structures are hardened at the front door using memory-hard **Argon2id** algorithms.


##  Machine Learning Engine Core
The diagnostic core consists of a customized **Deep Feedforward Artificial Neural Network (ANN)** built from scratch in PyTorch, mapping a **162-dimensional input feature space** down to 5 discrete output logits corresponding to real-world ESI Urgency levels (0 = Critical Resuscitation, 4 = Non-Urgent).

* **Multi-Modal Data Fusion:** Concurrently processes continuous vitals, administrative demographics, over 20 programmatically harvested chronic disease flags (`hx_`), and sparse natural language text matrices.
* **NLP Ingestion Pipeline:** Converts raw free-text clinical logs using a specialized **TF-IDF Vectorizer** tracking the top 100 highest-impact diagnostic keywords.
* **Gradient Stabilization & Regularization:** Integrates layer-specific `BatchNorm1d` to equalize high-contrast feature sizes (e.g., Blood pressure vs. text tokens) and `Dropout` (p=0.3) to guarantee model generalization.
* **Model Serialization:** Optimization parameters are exported as standalone, portable binary matrices (`triage_nn.pt`, `scaler.pkl`, `tfidf.pkl`) loaded natively by the FastAPI service tier on system startup.


## Repository Directory Structure
acutriage-ai/
│
├── backend/
│   ├── app/
│   │   ├── core/                  # System runtime variables & cryptography
│   │   ├── database/              # Async database connection engine
│   │   ├── dependencies/          # Asymmetric token & RBAC middleware guards
│   │   ├── models/                # Persistent database entities (SQLAlchemy Core)
│   │   ├── schemas/               # Verification validation rules (Pydantic)
│   │   ├── repositories/          # Raw decoupled SQL transactional mappings
│   │   ├── services/              # Pure business logic & PyTorch ML orchestration
│   │   ├── routers/               # Microservice REST API network routes
│   │   └── main.py                # Global microservice bootstrapper
│   │
│   ├── ml_core/                   # Training notebooks & exploratory sandbox log
│   │   └── models/                # Compiled deployment assets (.pt / .pkl)
│   │
│   └── tests/                     # Automated unit and integration testing module
│
└── frontend/                      # High-contrast clinical dashboard (React Single Page App)


## Local Installation & Execution Strategy

### 1. Pre-requisites & Key Initialization
Ensure you have Python 3.11+, PostgreSQL, and OpenSSL installed locally. Generate your asymmetric keys via your terminal inside the `backend/app/core/` directory:
```bash
# Generate private RSA key
openssl genpkey -algorithm RSA -out rsa_private.pem -pkeyopt rsa_keygen_bits:2048
# Extract public key for verification
openssl rsa -pubout -in rsa_private.pem -out rsa_public.pem
```

### 2. Backend Environment Verification
Navigate into the backend project space, initialize an isolated virtual environment, and pull your environment requirements:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

Set up your workspace environment variables inside a localized `.env` file:
```env
DATABASE_URL=postgresql+asyncpg://postgres:YOUR_PASSWORD@localhost:5432/acutriage
PRIVATE_KEY_PATH=app/core/rsa_private.pem
PUBLIC_KEY_PATH=app/core/rsa_public.pem
```

Boot up the modular microservice server using Uvicorn:
```bash
uvicorn app.main:app --reload
```
Once initialized, access the dynamic backend API documentation playground at `http://127.0.0`.

### 3. Running System Verification Tests
Execute your decoupled test suites via PyTest to evaluate your authentication structures and data vectors:
```bash
pytest
```

