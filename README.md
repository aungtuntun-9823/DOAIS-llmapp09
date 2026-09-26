# llmapp09 local setup

This standalone repository loads local configuration from `.env` and uses a
dedicated Python 3.11 environment in `.venv`. GitHub Actions reads credentials
from repository secrets; credentials are never added to the Docker images.

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
