# CaRMS Data Pipeline & AI Query API

## End-to-End Data Engineering & RAG Application

This project automates the ingestion, transformation, and querying of Canadian Residency Matching Service (CaRMS) data. It features a professional-grade stack moving data from local Excel sources to a cloud-hosted PostgreSQL database, served via a FastAPI interface with AI-powered natural language capabilities.

---
## Architecture
The system is decoupled into four distinct layers:

1. ***Orchestration (Dagster):*** Handles the ETL process, transforming raw Excel data and syncing it to the cloud.
2. ***Storage (AWS RDS):*** A managed PostgreSQL instance for structured residency program data.
3. ***API Layer (FastAPI):*** A containerized service deployed on AWS EC2 that handles data retrieval.
4. ***AI Layer (LangChain):*** A RAG (Retrieval-Augmented Generation) implementation that searches `.md` program descriptions to answer complex user questions.

---

## Live Services
- ***API Documentation:*** http://3.141.85.201/docs
- ***Primary Endpoint:*** http://3.141.85.201/disciplines
- ***Database:*** PostgreSQL on AWS RDS

---

## Tech Stack

| Category | Technology |
| --- | --- |
| Language | Python 3.11 |
| Orchestration | Dagster |
| API Framework | FastAPI |
| Database/ORM | PostgreSQL, SQLModel, SQLAlchemy |
| AI/LLM | LangChain |
| Cloud Infrastructure | AWS (EC2, RDS, ECR) |
| DevOps | Docker (Cross-platform builds), Environment Secrets |

---

## Key Technical Wins & Challenges

### ***Cloud Connectivity & Security***
Successfully bridged local development and cloud infrastructure by configuring AWS Security Groups and VPC Inbound Rules (Port 5432) to allow secure data migration from a local Dagster instance to AWS RDS.

### ***Cross-Platform Docker Deployment***
Solved "Exec Format Error" issues by implementing multi-platform builds.
```docker build --platform linux/amd64 -t carms-api .```
This ensured compatibility between Apple Silicon (M-series) development and AWS EC2 (Intel/AMD) runtime environments.

### ***Modular Logic Separation***
Architected a clean separation between the ***Write-side*** (Dagster pipelines) and the ***Read-side*** (FastAPI repository patterns), ensuring the API stays lightweight and highly available even during data refreshes.

---

## Local Setup
***1. Clone & Environment***

```Bash
git clone <repo-url>
cd carms_demo
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

***2. Environment Variables***

Create a `.env` file:
```
DATABASE_URL=postgresql://user:password@endpoint:5432/dbname
```

***3. Run the Pipeline (ETL)***

```Bash
dagster dev -f dagster_pipeline/pipelines.py
```

*Navigate to localhost:3000* to materialize the `etl_job`.

***4. Start the API***

```Bash
uvicorn main:app --reload
```

---

## Future Roadmap

- ***Vector Search:*** Transition from keyword matching to ChromaDB/FAISS vector embeddings for the `/ask` endpoint.
- ***CI/CD:*** Implement GitHub Actions to automatically push new Docker images to ECR on every commit.
- ***Monitoring:*** Add Prometheus/Grafana dashboard to track API latency and database query performance.

---