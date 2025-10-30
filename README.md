# CFWorker

A lightweight Python CLI tool for quickly deploying and managing Cloudflare Workers. Perfect for rapidly prototyping app ideas and deploying them to the edge with minimal hassle.

## Features

- Simple CLI for deploying Cloudflare Workers
- Multiple starter templates (REST API, static site, edge function)
- Configuration management via `.cfworker.json`
- Secure credential handling with `.env` files
- List, deploy, and manage workers from the command line
- Zero server administration - deploy directly to Cloudflare's edge network

## Installation

### From Source

```bash
# Clone or navigate to the CFWorker directory
cd CFWorker

# Create a virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install in development mode
pip install -e .
```

### Requirements

- Python 3.10 or higher
- Cloudflare account with Workers enabled
- Cloudflare API token with Workers Scripts:Edit permissions

## Quick Start

### 1. Setup Cloudflare Credentials

First, get your Cloudflare credentials:

1. **Account ID**: Found in your [Cloudflare dashboard](https://dash.cloudflare.com/) (in the right sidebar)
2. **API Token**: Create one at https://dash.cloudflare.com/profile/api-tokens
   - Use the "Edit Cloudflare Workers" template
   - Or create custom token with `Workers Scripts:Edit` permissions

Then run the interactive setup:

```bash
cfworker config-setup
```

Or manually create a `.env` file:

```bash
CLOUDFLARE_ACCOUNT_ID=your_account_id_here
CLOUDFLARE_API_TOKEN=your_api_token_here
```

### 2. Initialize a New Worker

```bash
# Create a new worker from a template
cfworker init my-worker --template api

# Available templates:
# - api: REST API with routing
# - static: Static HTML site
# - edge: Simple edge function
```

This creates:
- `.cfworker.json` - Worker configuration
- `worker.js` - Your worker script
- `.env` - Credentials file (if not exists)

### 3. Deploy Your Worker

```bash
# Deploy to Cloudflare
cfworker deploy

# Your worker will be live at:
# https://my-worker.workers.dev
```

### 4. Manage Your Workers

```bash
# List all workers
cfworker list

# Get info about a specific worker
cfworker info

# Delete a worker
cfworker delete
```

## Usage Examples

### Example 1: Quick REST API

```bash
# Initialize
cfworker init my-api --template api

# Edit worker.js to add your endpoints
# Deploy
cfworker deploy
```

### Example 2: Static Website

```bash
# Initialize
cfworker init my-site --template static

# Edit worker.js to customize your HTML
# Deploy
cfworker deploy
```

### Example 3: Edge Function

```bash
# Initialize
cfworker init my-function --template edge

# Customize the function logic
# Deploy
cfworker deploy
```

## Configuration

### `.cfworker.json`

The configuration file defines your worker settings:

```json
{
  "worker_name": "my-worker",
  "main": "worker.js",
  "compatibility_date": "2024-01-01",
  "routes": [],
  "kv_namespaces": [],
  "vars": {
    "ENVIRONMENT": "production"
  },
  "triggers": {
    "crons": []
  }
}
```

### Environment Variables

Set in your `.env` file:

```bash
CLOUDFLARE_ACCOUNT_ID=your_account_id
CLOUDFLARE_API_TOKEN=your_api_token
```

### Adding KV Storage

1. Create a KV namespace in Cloudflare dashboard
2. Add to `.cfworker.json`:

```json
{
  "kv_namespaces": [
    {
      "binding": "MY_KV",
      "id": "your_kv_namespace_id"
    }
  ]
}
```

3. Use in your worker:

```javascript
// Read
const value = await env.MY_KV.get('key');

// Write
await env.MY_KV.put('key', 'value');
```

## CLI Commands

### `cfworker init <worker_name>`

Initialize a new worker project.

**Options:**
- `--template, -t` - Template to use (api, static, edge)
- `--force, -f` - Overwrite existing files

**Example:**
```bash
cfworker init my-worker --template api
```

### `cfworker deploy`

Deploy worker to Cloudflare.

**Options:**
- `--config, -c` - Path to config file
- `--dry-run` - Validate without deploying

**Example:**
```bash
cfworker deploy
cfworker deploy --dry-run
```

### `cfworker delete`

Delete worker from Cloudflare (with confirmation prompt).

**Options:**
- `--config, -c` - Path to config file

**Example:**
```bash
cfworker delete
```

### `cfworker info`

Get information about deployed worker.

**Options:**
- `--config, -c` - Path to config file

**Example:**
```bash
cfworker info
```

### `cfworker list`

List all workers in your account.

**Options:**
- `--config, -c` - Path to config file

**Example:**
```bash
cfworker list
```

### `cfworker config-setup`

Interactive setup for Cloudflare credentials.

**Example:**
```bash
cfworker config-setup
```

## Project Structure

```
CFWorker/
├── cfworker/              # Main Python package
│   ├── __init__.py
│   ├── client.py          # Cloudflare API wrapper
│   ├── config.py          # Configuration management
│   ├── deployer.py        # Deployment logic
│   └── cli.py             # CLI interface
├── templates/             # Worker templates
│   ├── api/               # REST API template
│   ├── static/            # Static site template
│   └── edge/              # Edge function template
├── examples/              # Example projects
│   ├── hello-world/
│   └── kv-storage/
├── .claude/               # Claude Code integration
│   └── agents/
│       └── cloudflare-expert.md
├── pyproject.toml         # Python project config
├── .env.example           # Example environment file
└── README.md
```

## Cloudflare Expert Agent

This project includes a Cloudflare Workers expert agent for Claude Code. The agent can help with:

- Worker development best practices
- Cloudflare-specific features (KV, Durable Objects, etc.)
- Deployment troubleshooting
- Performance optimization
- Security best practices

See `.claude/agents/cloudflare-expert.md` for detailed information.

## Development

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black cfworker/
ruff check cfworker/
```

### Installing Development Dependencies

```bash
pip install -e ".[dev]"
```

## Examples

Check the `examples/` directory for complete working examples:

- **hello-world**: Minimal worker example
- **kv-storage**: Using KV storage for persistence

Each example includes a `worker.js` and `.cfworker.json` you can use as reference.

## Troubleshooting

### "Invalid API credentials" error

- Verify your `CLOUDFLARE_ACCOUNT_ID` and `CLOUDFLARE_API_TOKEN` in `.env`
- Ensure your API token has `Workers Scripts:Edit` permissions
- Run `cfworker config-setup` to reconfigure

### "Script file not found" error

- Ensure `worker.js` exists in your current directory
- Check the `main` field in `.cfworker.json` matches your script filename

### Deployment fails with "Script too large"

- Workers have a 1MB size limit
- Minimize your code and dependencies
- Consider splitting into multiple workers

### CORS errors in browser

- Add CORS headers to your worker responses:

```javascript
const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
};

return Response.json(data, { headers: corsHeaders });
```

## Resources

- [Cloudflare Workers Documentation](https://developers.cloudflare.com/workers/)
- [Workers Examples](https://developers.cloudflare.com/workers/examples/)
- [API Reference](https://developers.cloudflare.com/workers/runtime-apis/)
- [Community Forum](https://community.cloudflare.com/)

## License

MIT License - See LICENSE file for details

## Contributing

Contributions welcome! Please feel free to submit issues or pull requests.

## Roadmap

- [ ] TypeScript support with automatic transpilation
- [ ] Local development server with hot reload
- [ ] Built-in testing framework
- [ ] Wrangler.toml import/export
- [ ] Durable Objects support
- [ ] R2 storage integration
- [ ] D1 database support
- [ ] Worker-to-worker bindings
- [ ] Tail logs streaming
- [ ] Custom domains management
