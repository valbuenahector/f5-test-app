# F5 Test App

Small Flask container that echoes back the requesting client's IP, headers,
and cookies — styled to match F5's AppWorld 2026 demo branding. Built as a
general-purpose test/debug container for exercising deployment, proxy, and
load-balancing configs, with a configurable accent color and label so
multiple deployed instances can be told apart at a glance.


## Routes

| Route | Description |
|-------|-------------|
| `/` | HTML page showing client IP, request headers, cookies |
| `/api/whoami` | Same data as JSON |
| `/set-cookie` | Sets a demo cookie so cookie-echo can be verified without devtools |
| `/healthz` | Plain `200 ok` for container health checks |

## Configuration (environment variables)

| Variable | Default | Purpose |
|----------|---------|---------|
| `THEME_COLOR` | `f5red` | Accent color for nav badge / banner. Accepts a preset (`f5red`, `blue`, `green`, `purple`, `orange`) or a raw hex value like `#00A8E0` |
| `DEPLOYMENT_NAME` | `unnamed` | Free-text label shown next to the color swatch, e.g. `dev`, `staging`, `customer-demo` |
| `PORT` | `8080` | Port the app binds to inside the container |

Use these to visually distinguish multiple deployments of the same image
(e.g. blue+"dev" vs. red+"prod").

## Run locally (no Docker)

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
PORT=8080 THEME_COLOR=blue DEPLOYMENT_NAME=dev python app/app.py
```

## Run with Docker

```bash
docker build -t f5-test-app .
docker run --rm -p 8080:8080 \
  -e THEME_COLOR=blue -e DEPLOYMENT_NAME=dev \
  f5-test-app
```

## Run multiple differently-themed instances at once

```bash
docker compose up
# dev      -> http://localhost:8081  (blue)
# staging  -> http://localhost:8082  (orange)
# prod     -> http://localhost:8083  (f5red)
```

## Tests

```bash
pip install -r requirements.txt
pytest
```

## Publish to Docker Hub

Manual push:

```bash
docker build -t <dockerhub-username>/f5-test-app:latest .
docker push <dockerhub-username>/f5-test-app:latest
```

Automated: `.github/workflows/docker-publish.yml` builds and pushes a
multi-arch (`linux/amd64`, `linux/arm64`) image on every push to `main`
(tag `latest`) and on `v*` tags (semver tag). It requires two repository
secrets set under **Settings → Secrets and variables → Actions**:

- `DOCKERHUB_USERNAME` — your Docker Hub username
- `DOCKERHUB_TOKEN` — a Docker Hub access token (Account Settings → Security → New Access Token)

Pulling the published image:

```bash
docker pull <dockerhub-username>/f5-test-app:latest
```
