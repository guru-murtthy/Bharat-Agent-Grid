# Running Bharat Agent Grid

## Local (zero keys — stub mode)

```bash
pip install fastapi "uvicorn[standard]" pydantic
uvicorn src.api.app:app --reload
# open http://127.0.0.1:8000
```

CLI demo:

```bash
python -m demo.run_demo
```

## Enable real LLM planning

```bash
cp .env.example .env
# set LLM_PROVIDER=openai and OPENAI_API_KEY=sk-...
export $(grep -v '^#' .env | xargs)
uvicorn src.api.app:app --reload
```

With no key set, the planner falls back to deterministic keyword parsing, so the
app always runs.

## Tests

```bash
pip install pytest httpx
pytest -q
```

## Docker

```bash
docker build -t bharat-agent-grid .
docker run -p 8000:8000 bharat-agent-grid
```
