# ATA 52 Door Reliability Intelligence

Analysing public aircraft service-difficulty data for **doors (ATA Chapter 52)** to surface failure modes, trends and regulatory context for door engineers.

> This project uses **public data only** (FAA, EASA). No proprietary or company-internal data is used.

## Data sources

| Source | Content | Access |
|---|---|---|
| FAA Service Difficulty Reports (SDR) | Operator-reported failures, malfunctions and defects | [Yearly CSV downloads](https://www.faa.gov/av-info/download_SDR) |
| EASA Airworthiness Directives | Mandatory actions on unsafe conditions, tagged by ATA chapter | [EASA Safety Publications Tool](https://ad.easa.europa.eu) |

**Known limitation:** SDRs come mostly from US-registered aircraft, so fleet coverage is not global.

## Roadmap

- [ ] **Phase 1** – Ingestion pipeline (SDR + EASA ADs) into PostgreSQL, cleaning, EDA
- [ ] **Phase 2** – Failure-mode classification (latch, seal, hinge, actuator, sensor/warning, slide) + dashboard
- [ ] **Phase 3** – REST API (FastAPI), CI/CD (GitHub Actions), cloud deployment
- [ ] **Phase 4** – RAG assistant over ADs and reports + MCP server on the database

## Project structure

```
├── data/
│   ├── raw/          # downloaded files (not committed)
│   └── processed/    # cleaned data (not committed)
├── src/
│   ├── ingest/       # download / scraping
│   ├── transform/    # cleaning and normalisation
│   └── db/           # database schema and loading
├── notebooks/        # exploration (EDA)
├── tests/
└── docker-compose.yml
```

## Quick start

**Requirements:** Docker, Python 3.10+

```bash
# Clone
git clone https://github.com/azizchrif/ata52-door-intelligence.git
cd ata52-door-intelligence

# Start PostgreSQL
docker compose up -d

# Check the database
docker compose exec db psql -U ata52 -d ata52
```

## Tech stack

Python · pandas · PostgreSQL · Docker