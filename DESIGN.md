# SolderTrail - System Design

## 1. Project Overview

SolderTrail is a Retrieval-Augmented Generation (RAG) application designed to help business development executives find reliable information about electronics manufacturing companies.

The system uses company documents such as annual reports, investor presentations, BRSRs, and earnings-call transcripts...

The initial target companies are:

- Avalon Technologies
- Dixon Technologies
- Kaynes Technology
- Syrma SGS
- Amber Enterprises

## 2. Technology Stack

| Component | Technology |
|---|---|
| Backend | Python, FastAPI |
| LLM integration | Primary LLM with fallback model |
| Document processing | Python |
| API server | Uvicorn |
| Configuration | Pydantic Settings |
| Containerization | Docker |
| Testing | Pytest |
| CI | GitHub Actions |

## 3. API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/hello` | Basic application greeting |
| GET | `/health` | Check application health |
| POST | `/query` | Submit a question and retrieve an answer |
| GET | `/usage` | View token consumption and estimated LLM cost |

### GET /health

Checks whether the application is running.

Example response:

```json
{
  "status": "ok",
  "app": "examate-rag",
  "environment": "local"
}
```

The health endpoint should not call the LLM or database.

### POST /query

Accepts a user question and returns an answer supported by relevant company documents.

Planned request:

```json
{
  "question": "What are the major products manufactured by Avalon Technologies?"
}
```

Planned response:

```json
{
  "answer": "Answer generated using retrieved documents.",
  "sources": [],
  "model": "primary"
}
```

### GET /usage

Returns LLM token usage and estimated cost.

Planned response:

```json
{
  "total_input_tokens": 0,
  "total_output_tokens": 0,
  "total_cost": 0.0
}
```

## 4. Database Design

The following tables are proposed for the application.

### Documents

Stores information about collected company documents.

| Column | Description |
|---|---|
| document_id | Unique document identifier |
| company_name | Company name |
| document_name | Name of the document |
| document_type | Annual report, presentation, transcript, etc. |
| source_url | Original document URL |
| publication_date | Document publication date |

### Document Chunks

Stores smaller text sections extracted from documents for retrieval.

| Column | Description |
|---|---|
| chunk_id | Unique chunk identifier |
| document_id | Related document |
| chunk_text | Extracted text |
| page_number | Source page number |

### Usage Logs

Tracks LLM usage and estimated costs.

| Column | Description |
|---|---|
| usage_id | Unique usage identifier |
| model_name | LLM model used |
| input_tokens | Input token count |
| output_tokens | Output token count |
| estimated_cost | Estimated API cost |
| created_at | Request timestamp |

## 5. LLM Integration and Fallback

The application will use a primary LLM for generating answers.

If the primary model fails or becomes unavailable, the application will attempt to use a configured fallback model.

The application should record which model generated each response and track token usage and estimated cost.

## 6. Deployment and Monitoring

- Docker will be used to containerize the FastAPI application.
- Uvicorn will serve the API.
- The `/health` endpoint will support health checks.
- GitHub Actions will run automated code-quality checks and tests.
- The application will be deployed to a free hosting platform for demonstration.

## 7. Future Improvements

- Document ingestion and processing.
- BM25 and vector-based retrieval.
- Reranking retrieved documents.
- Source citations in generated answers.
- Query tracing and performance monitoring.
- Query latency dashboard and trace waterfall.