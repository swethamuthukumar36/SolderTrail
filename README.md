# SolderTrail

## Problem
Business development executives at electronic-component suppliers need quick and reliable information about electronics manufacturing companies before sales meetings. Important details like new plants, order books, product lines, and PLI incentives are spread across annual reports, investor presentations, BRSRs, and earnings-call transcripts. Searching these documents manually takes time, and the existing chatbot is slow, making it difficult to understand where the delay occurs. SolderTrail helps users find relevant information quickly with cited sources and stage-by-stage performance tracking.

## Who it is for
Business development executives at electronic-component suppliers who work with electronics manufacturing services (EMS) companies, especially those operating in and around Sriperumbudur.

## Signature feature
Why was this slow? — A button that displays the trace waterfall for a particular answer, showing the time taken by each stage, including query rewriting, BM25 search, vector search, re-ranking, and LLM generation.

## Hardest problem (my interview story)
The hardest problem is improving response speed while maintaining accurate, source-backed answers. I will use OpenTelemetry tracing to measure the time taken by each stage of the retrieval and answer-generation pipeline. I will set a p95 end-to-end latency target of under 4 seconds and use a dashboard to identify and optimize the slowest stage, comparing performance before and after the changes.

## Dataset

| Source | Link | Documents | Pages | Licence / terms |
|---|---|---:|---:|---|
| Avalon Technologies | [Investor Relations](https://www.avalontec.com/investors/) | To be collected | To be counted | Check individual document terms |
| Dixon Technologies | Official investor relations page | To be collected | To be counted | Check individual document terms |
| Kaynes Technology | Official investor relations page | To be collected | To be counted | Check individual document terms |
| Syrma SGS | Official investor relations page | To be collected | To be counted | Check individual document terms |
| Amber Enterprises | Official investor relations page | To be collected | To be counted | Check individual document terms |


## 10 real questions
See [docs/QUESTIONS.md](docs/QUESTIONS.md).

## Run it
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
cp .env.example .env                                 # Windows: copy .env.example .env
uvicorn app.main:app --reload
curl localhost:8000/health
```

## Live link
<Added in Week 2>
