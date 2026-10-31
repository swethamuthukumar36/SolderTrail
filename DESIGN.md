# SolderTrail - System Design

## 1. Project Overview

SolderTrail is a Retrieval-Augmented Generation (RAG) application designed to help business development executives find reliable information about electronics manufacturing companies.

The system aims to use company documents such as annual reports, investor presentations, BRSRs, and earnings-call transcripts.

The initial target companies are:

- Avalon Technologies
- Dixon Technologies
- Kaynes Technology
- Syrma SGS
- Amber Enterprises

The current implementation focuses on the FastAPI backend, LLM integration, fallback handling, usage tracking, and Docker deployment.

Document ingestion and retrieval features are planned for future development.

## 2. Technology Stack

| Component | Technology |
|---|---|
| Backend | Python, FastAPI |
| LLM integration | OpenAI-compatible API / Fake Provider |
| LLM fallback | Configurable fallback provider |
| Configuration | Pydantic Settings |
| API server | Uvicorn |
| Usage tracking | JSONL cost logs |
| Containerization | Docker, Docker Compose |
| Testing | Pytest |
| Code quality | Ruff |
| CI | GitHub Actions |

## 3. API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Root endpoint |
| GET | `/hello` | Basic application greeting |
| GET | `/health` | Application liveness check |
| POST | `/chat` | Send messages to the configured LLM and receive a streamed response |
| GET | `/usage` | View daily token usage and estimated cost |

### GET /health

Checks whether the application is running.

Example response:

```json
{
  "status": "ok",
  "app": "examate-rag",
  "environment": "production"
}
```

This endpoint does not call the LLM or database.

### POST /chat

Accepts a conversation and streams the LLM response using Server-Sent Events (SSE).

Example request:

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Hello, SolderTrail!"
    }
  ]
}
```

Example streamed response:

```text
data: {"delta": "Hello"}

data: {"delta": " from the fake provider."}

event: done
data: {
  "usage": {
    "input_tokens": 0,
    "output_tokens": 2,
    "estimated": true
  },
  "cost_usd": 0.0
}
```

The application supports a primary LLM provider and a configurable fallback provider.

### GET /usage

Returns daily usage statistics from the JSONL cost log.

Example response:

```json
{
  "2026-10-31": {
    "calls": 2,
    "input_tokens": 0,
    "output_tokens": 4,
    "cost_usd": 0.0
  }
}
```

The usage log tracks:

- Provider and model
- Input and output tokens
- Estimated usage indicator
- Request latency
- Estimated cost
- Request success status
- Whether fallback was used

## 4. Data Storage Design

The current implementation does not use a relational database.

LLM usage records are stored as JSON Lines in `logs/cost.jsonl`.

A persistent Docker volume is configured for application logs.

### Planned Database Tables

The following tables are proposed for future document ingestion and retrieval functionality.

#### Documents

Stores information about collected company documents.

| Column | Description |
|---|---|
| document_id | Unique document identifier |
| company_name | Company name |
| document_name | Name of the document |
| document_type | Annual report, presentation, transcript, etc. |
| source_url | Original document URL |
| publication_date | Document publication date |

#### Document Chunks

Stores smaller text sections extracted from documents for retrieval.

| Column | Description |
|---|---|
| chunk_id | Unique chunk identifier |
| document_id | Related document |
| chunk_text | Extracted text |
| page_number | Source page number |

## 5. LLM Integration and Fallback

The application uses a configurable LLM provider.

If the primary provider becomes unavailable before producing response content, the application attempts to use the configured fallback provider.

The application records usage information, request latency, estimated cost, and fallback usage.

A `/usage` endpoint provides daily usage summaries.

The current development configuration uses a fake provider for testing without requiring external LLM API calls.

## 6. Docker and Deployment

The FastAPI application is containerized using Docker.

Docker Compose manages the API service.

Current deployment configuration includes:

- Python 3.12 slim base image.
- Uvicorn API server.
- Environment-based configuration.
- Persistent volume for application logs.
- Automatic container restart policy.
- Application health endpoint.

The application has been tested locally inside Docker.

Deployment to a free hosting platform is planned.

## 7. CI and Testing

GitHub Actions is configured to:

- Install project dependencies.
- Run Ruff code-quality checks.
- Execute automated tests using Pytest.

## 8. Future Improvements

- Document ingestion and processing.
- BM25 and vector-based retrieval.
- PostgreSQL with pgvector integration.
- Reranking retrieved documents.
- Source citations in generated answers.
- Query tracing and performance monitoring.
- OpenTelemetry integration.
- Query latency dashboard and trace waterfall.
