# SolderTrail – System Design

## 1. Project Overview

SolderTrail is a Retrieval-Augmented Generation (RAG) application designed to help business development executives find reliable information about electronics manufacturing companies.

The system aims to use company documents such as annual reports, investor presentations, Business Responsibility and Sustainability Reports (BRSRs), and earnings-call transcripts.

The initial target companies are:

- Avalon Technologies
- Dixon Technologies
- Kaynes Technology
- Syrma SGS
- Amber Enterprises

The current implementation focuses on the FastAPI backend, LLM provider integration, retry and fallback handling, usage tracking, automated testing, Docker deployment, and CI.

Document ingestion, text extraction, indexing, and retrieval are planned for future development.

## 2. Technology Stack

| Component | Technology |
|---|---|
| Backend | Python, FastAPI |
| LLM integration | OpenAI-compatible API / Fake Provider |
| LLM reliability | Retry and configurable fallback |
| Configuration | Pydantic Settings |
| API server | Uvicorn |
| Usage tracking | JSONL cost logs |
| Database | PostgreSQL with pgvector (Docker Compose configuration) |
| Containerization | Docker, Docker Compose |
| Testing | Pytest |
| Code quality | Ruff |
| CI | GitHub Actions |
| Deployment | Render |

## 3. System Architecture

The current application follows a modular backend architecture.

Main components:

- **FastAPI application:** Exposes API endpoints.
- **LLM provider layer:** Supports fake and OpenAI-compatible providers.
- **Reliability layer:** Handles retry attempts and fallback provider execution.
- **Usage tracking:** Records token usage, latency, and estimated cost.
- **Configuration layer:** Loads application settings and environment variables.
- **Database service:** PostgreSQL with pgvector is configured through Docker Compose for future retrieval functionality.

The current application can process chat requests using the configured LLM provider and stream responses through Server-Sent Events (SSE).

Document retrieval is not yet connected to the chat workflow.

## 4. API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Root endpoint |
| GET | `/hello` | Basic application greeting |
| GET | `/health` | Application liveness check |
| GET | `/ready` | Application and database readiness check |
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

This endpoint checks application liveness without calling the LLM.

### GET /ready

Checks whether the application is ready to serve requests.

When no database is configured, the endpoint reports that the database is not configured. When a database URL is configured, it checks database connectivity.

### POST /chat

Accepts conversation messages and streams the LLM response using Server-Sent Events (SSE).

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
data: {"usage": {"input_tokens": 0, "output_tokens": 2, "estimated": true}, "cost_usd": 0.0}
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

## 5. Data Storage Design

LLM usage records are currently stored as JSON Lines in `logs/cost.jsonl`.

Docker Compose configures PostgreSQL with the pgvector extension for future document storage and vector retrieval functionality.

Document ingestion and retrieval are not yet implemented.

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
| embedding | Vector representation for semantic search |

## 6. LLM Integration and Reliability

The application uses a configurable LLM provider.

The current implementation includes:

- Fake provider for local development and testing.
- OpenAI-compatible provider integration.
- Retry handling for transient provider failures.
- Configurable fallback provider.
- Protection against retrying or falling back after partial response output.

The application records usage information, request latency, estimated cost, and fallback usage.

The `/usage` endpoint provides daily usage summaries.

The current development and deployment configuration uses the fake provider. Live responses from a real external LLM provider require separate configuration and verification.

## 7. Docker and Deployment

The FastAPI application is containerized using Docker.

Docker Compose manages the API and PostgreSQL database services.

Current deployment configuration includes:

- Python 3.12 slim base image.
- Uvicorn API server.
- Environment-based configuration.
- PostgreSQL with pgvector.
- Persistent volume for application logs.
- Container health checks.
- Automatic container restart policy.

The application has been tested locally using Docker and Docker Compose.

The application is deployed on Render:

https://soldertrail.onrender.com

The deployed application currently uses the fake provider for testing without requiring an external LLM API key.

## 8. CI and Testing

GitHub Actions is configured to:

- Install project dependencies.
- Run Ruff code-quality checks.
- Execute automated tests using Pytest.
- Build the Docker image.
- Perform a Docker health-check smoke test.

The current local verification includes:

- 16 automated tests passing.
- Ruff code-quality checks passing.

## 9. Future Improvements

- Document ingestion and processing.
- PDF text extraction using pypdf.
- HTML content extraction using BeautifulSoup.
- PostgreSQL document metadata storage.
- BM25 and vector-based retrieval.
- Reranking retrieved documents.
- Source citations in generated answers.
- Query tracing and performance monitoring.
- OpenTelemetry integration.
- Query latency dashboard and trace waterfall.