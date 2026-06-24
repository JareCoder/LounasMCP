# LounasMCP

A Model Context Protocol (MCP) server that scrapes daily lunch menus for restaurants located in **Kauppakeskus Sello, Espoo** from `lounaat.info`.

Built using the official Anthropic MCP Python SDK's `FastMCP` and `BeautifulSoup4`.

## Features
- **`get_sello_lunch_menus`**: Retrieve Sello restaurant lunch menus.
  - Parameter: `day` (optional): Query specific day (`keskiviikko`, `torstai`, etc.). Defaults to `"today"`.
- **Flexible Transport**: Natively supports both `stdio` and `sse` transports.
- **Docker Support**: Ready to be packaged and run in a containerized environment (ideal for connecting to LiteLLM).

## Setup & Running Locally

### Installation
Ensure you have Python 3.10+ installed.

```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install package
pip install -e .
```

### Running Server
By default, the server runs in **stdio** mode:
```bash
python server.py
```

To run in **SSE** mode (web server on port 8000):
```bash
python server.py --transport sse --port 8000
```

---

## Running with Docker

### 1. Build the Docker Image
```bash
docker build -t lounas-mcp .
```

### 2. Run Options

#### Option A: stdio Mode (Direct Command via Docker Exec)
Your MCP client can invoke Docker directly:
```bash
docker run -i --rm lounas-mcp --transport stdio
```

#### Option B: SSE Mode (HTTP Server)
Expose the HTTP port so other containers or host services can connect via HTTP SSE:
```bash
docker run -d --name lounas-mcp -p 8000:8000 lounas-mcp --transport sse --port 8000
```

---

## Connecting to LiteLLM

To integrate this MCP server with LiteLLM, you can configure the MCP settings depending on how your LiteLLM instance is running.

### Using SSE (Recommended for Containerized Environments)
If your LiteLLM is running in a Docker container, run `lounas-mcp` in SSE mode (Option B above) on the same network. Then, add it to your LiteLLM configuration:

```yaml
mcp_servers:
  lounas-mcp:
    type: sse
    url: http://lounas-mcp:8000/sse
```
*(If LiteLLM is running on the host machine and Docker port is mapped, use `http://localhost:8000/sse`)*

### Using stdio (If LiteLLM has docker-cli access)
If your LiteLLM server runs locally and can invoke `docker` directly:

```yaml
mcp_servers:
  lounas-mcp:
    type: command
    command: docker
    args:
      - run
      - -i
      - --rm
      - lounas-mcp
      - --transport
      - stdio
```
