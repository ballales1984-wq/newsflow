# App Improvement Plan

## Backend
- Add auth on /api/admin/collect-news (currently open)
- Fix local backend startup docs and add health check endpoint
- Remove hardcoded Render URL from AGGIORNA_NOTIZIE.ps1; use env var
- Add DB migrations (alembic) usage; remove JSON file coupling
- Add tests for collect-news and articles endpoints

## Frontend
- Replace ngrok interceptor hardcoding; use environment config
- Add loading/error states in article-list
- Add pagination/infinite scroll for articles
- Add saved articles UI sync with backend
- Add e2e tests (Playwright) for main flows

## DevOps
- Consolidate scripts; add single `make dev` / npm scripts
- Add CI (GitHub Actions) for lint + tests
- Add Docker compose healthchecks
- Remove secrets from repo (youtube_credentials.json)

## Priorities
1. Security: protect admin endpoints
2. Reliability: local dev startup
3. UX: pagination + error states
4. Quality: tests + CI
" filePath">
C:\Users\user\news\PLAN_IMPROVEMENTS.md