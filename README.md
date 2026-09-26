# llmapp09 local setup

This standalone repository loads local configuration from `.env` and uses a
dedicated Python 3.11 environment in `.venv`. GitHub Actions reads credentials
from repository secrets; credentials are never added to the Docker images.

## GitHub Actions secrets

GitHub Actions secrets belong to one repository and are not copied from the
original `DOAIS` repository. In the standalone repository, open **Settings >
Secrets and variables > Actions** and add:

- `OLLAMA_API_KEY` — required by the backend, PromptFoo, and DeepEval workflows.
- `OPENAI_API_KEY` — required by DeepEval's `GEval` metrics.
- `DOCKERHUB_TOKEN` — required to push the two images to Docker Hub on a branch
  push. Use a Docker Hub access token, not your account password.

Save each secret as its raw, single-line value. Do not include an `export`
command, the variable name, surrounding quotes, or extra line breaks.
The DeepEval workflow trims accidental leading or trailing whitespace and
rejects other control characters before running the paid model evaluations.

`OLLAMA_BASE_URL` is optional and defaults to `https://ollama.com`. The three
`LANGFUSE_*` secrets are optional and enable tracing when configured:
`LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`, and `LANGFUSE_HOST`.

The image workflows fail for fixable HIGH or CRITICAL vulnerabilities. They
ignore findings that do not yet have an upstream fix, matching the documented
local Trivy scan behavior.

Create the local environment and configuration file:

```bash
cd "/Users/aungtuntun/AI Models/DOAIS-llmapp09"
python3.11 -m venv .venv
cp .env.example .env
```

Open `.env` and add your local `OLLAMA_API_KEY`. Add Langfuse credentials only
when tracing is required. Never commit `.env`.

Install the guarded multi-route backend requirements:

```bash
cd "/Users/aungtuntun/AI Models/DOAIS-llmapp09/llm-multiroute"
../.venv/bin/python -m pip install -r requirements.txt
```

Run the guarded multi-route backend:

```bash
cd "/Users/aungtuntun/AI Models/DOAIS-llmapp09/llm-multiroute"
../.venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8085 --reload
```

Install the frontend requirements:

```bash
cd "/Users/aungtuntun/AI Models/DOAIS-llmapp09/llm-frontend-python"
../.venv/bin/python -m pip install -r requirements.txt
```

Run the frontend in another terminal:

```bash
cd "/Users/aungtuntun/AI Models/DOAIS-llmapp09/llm-frontend-python"
../.venv/bin/python app.py
```

Open `http://127.0.0.1:5006`. Swagger is at
`http://127.0.0.1:8085/swagger-ui.html`.

For Docker, use the project's original container names and ports. You can use
either of the following methods.

### Docker method 1: build, then start

Build both Docker images and then start the containers:

```bash
cd "/Users/aungtuntun/AI Models/DOAIS-llmapp09"
docker compose build
docker compose up -d
```

### Docker method 2: build and start with one command

The following command builds the images when necessary and starts the
containers in the background:

```bash
cd "/Users/aungtuntun/AI Models/DOAIS-llmapp09"
docker compose up -d --build
```

Check that both containers are running:

```bash
docker compose ps
```

The Docker frontend is available at `http://127.0.0.1:5000`, and its backend is
available at `http://127.0.0.1:8080`. These are separate from the direct local
run ports documented above (`5006` and `8085`).

After changing source code or requirements, run the method 2 command again to
rebuild and restart:

```bash
docker compose up -d --build
```

If Docker reports that port `5000` is already in use on macOS, open **System
Settings > General > AirDrop & Handoff** and turn off **AirPlay Receiver**.
Then run `docker compose down` and start the containers again. Alternatively,
change the frontend host-port mapping in `docker-compose.yml` from
`"5000:5000"` to an unused port such as `"5006:5000"`, then open
`http://127.0.0.1:5006`.

Stop and remove the containers and network with:

```bash
docker compose down
```

Run tests from either backend directory with
`../.venv/bin/python -m pytest -q`.
