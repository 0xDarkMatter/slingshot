# Slingshot Project Context

## What is Slingshot?

A lightweight Python CLI tool for quickly deploying and managing Cloudflare Workers. Perfect for rapidly prototyping app ideas and deploying them to the edge with minimal hassle.

**Formerly known as:** CFWorker (renamed October 2024)

## Architecture Overview

```
src/slingshot/
├── cli.py       - Click-based CLI interface (commands: init, deploy, delete, list, info, config-setup)
├── client.py    - Cloudflare API wrapper (Workers API v4)
├── config.py    - Configuration management (.slingshot.json and .env)
├── deployer.py  - Deployment orchestration (script bundling, metadata preparation)
└── py.typed     - Type hint marker
```

## Key Design Decisions

### Why Click over argparse?
- Better user experience with command groups
- Built-in help text formatting
- Easy subcommand management (future: `slingshot d1 create`)

### Why src/ layout?
- Better package isolation during development
- Prevents import confusion between installed and development versions
- Industry best practice for modern Python projects

### Why Workers API v4?
- Current stable API version
- Better support for bindings (KV, D1, R2)
- Improved metadata format

## Cloudflare Workers Domain Knowledge

### Worker Limits
- **Script size:** 1MB maximum (after bundling)
- **CPU time:** 50ms on free tier, 50ms-500ms on paid
- **Memory:** 128MB

### Bindings
Bindings connect workers to Cloudflare resources:
- **KV Namespaces:** Key-value storage
- **D1 Databases:** SQL database (SQLite at the edge) - *planned*
- **R2 Buckets:** Object storage (S3-compatible) - *planned*
- **Environment Variables:** Static config values

### Configuration Format (.slingshot.json)

```json
{
  "worker_name": "my-worker",
  "main": "worker.js",
  "compatibility_date": "2024-01-01",
  "kv_namespaces": [
    {
      "binding": "MY_KV",
      "id": "namespace_id"
    }
  ],
  "d1_databases": [],  // Future: D1 support
  "r2_buckets": [],    // Future: R2 support
  "vars": {
    "ENVIRONMENT": "production"
  }
}
```

### Deployment Flow

1. **Read config:** Load `.slingshot.json` and `.env`
2. **Validate:** Check worker script exists, parse metadata
3. **Prepare metadata:** Convert config to Cloudflare API format
4. **Build bindings:** Translate KV/D1/R2 configs to binding objects
5. **Upload script:** Multipart/form-data upload to Workers API
6. **Deploy:** Publish to workers.dev subdomain or custom routes

### Metadata Bindings Format

Cloudflare expects bindings in this format:
```json
{
  "bindings": [
    {
      "type": "kv_namespace",
      "name": "MY_KV",
      "namespace_id": "xxx"
    },
    {
      "type": "d1",
      "name": "DB",
      "id": "database_id"
    }
  ]
}
```

## Current Implementation Status

### Completed ✅
- Core CLI commands (init, deploy, delete, list, info)
- KV namespace management (list, create)
- Worker templates (API, static, edge)
- Configuration management
- Test suite with pytest
- Documentation (README, QUICKSTART, CONTRIBUTING)

### In Progress 🚧
- D1 database support (planned - see PLAN.md)
- R2 storage integration (planned - see PLAN.md)

### Not Yet Implemented ⏳
- Worker secrets management
- Durable Objects support
- Custom domains
- Tail logs streaming
- Local development server
- TypeScript transpilation

## Development Workflow

### Todo Management
- **Always sync both:** TodoWrite tool (session todos) AND PLAN.md checkboxes
- When marking complete: Update both session and markdown `[x]`
- When adding new tasks: Add to both locations

### Commit Style
- Follow [Conventional Commits](https://www.conventionalcommits.org/)
- Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`
- Examples: `feat(cli): add d1 create command`, `fix(client): handle timeout errors`

### Testing
- Run tests before significant commits: `pytest`
- Check coverage: `pytest --cov=slingshot --cov-report=html`
- Target: >80% code coverage

### Code Style
- Format with Black (100 char line length): `black src/ tests/`
- Lint with Ruff: `ruff check src/ tests/`
- Add type hints to all public functions

## Common Patterns

### Adding a New CLI Command

```python
@main.command()
@click.argument('name')
@click.option('--force', '-f', is_flag=True)
def mycommand(name: str, force: bool):
    """Short description for --help."""
    client = get_cloudflare_client()
    # Implementation
```

### Adding a Client Method

```python
def my_api_method(self, param: str) -> Dict[str, Any]:
    """Docstring with parameters and return value."""
    return self._request(
        "POST",
        f"accounts/{self.account_id}/resource",
        data={"param": param}
    )
```

### Updating Deployer for New Binding Type

```python
# In prepare_metadata():
for resource in self.config.get("my_resources", []):
    bindings.append({
        "type": "my_type",
        "name": resource.get("binding"),
        "id": resource.get("resource_id")
    })
```

## Security Considerations

### Credential Protection
- `.env` files contain plaintext credentials (Account ID, API Token)
- Always in `.gitignore` (never commit)
- Set `chmod 600 .env` on Unix/Linux systems
- API tokens should have minimal scope (Workers Scripts:Edit only)

### Deployment Safety
- Workers are deployed to public internet (workers.dev subdomain)
- Environment variables in `.slingshot.json` are deployed with the worker
- Always review code before deploying (consider `--dry-run` flag)

## Troubleshooting

### "Invalid API credentials"
- Check `.env` file exists and has correct values
- Verify API token has Workers Scripts:Edit permission
- Run `slingshot config-setup` to reconfigure

### "Script too large"
- Workers have 1MB limit
- Minimize dependencies
- Consider splitting into multiple workers

### KV/D1/R2 binding not working
- Check binding name matches in `.slingshot.json` and worker code
- Verify resource ID is correct
- Ensure resource exists in Cloudflare account

## Resources

- [Cloudflare Workers Docs](https://developers.cloudflare.com/workers/)
- [Workers API Reference](https://developers.cloudflare.com/api/operations/worker-script-upload-worker-module)
- [D1 Documentation](https://developers.cloudflare.com/d1/)
- [R2 Documentation](https://developers.cloudflare.com/r2/)
- [PLAN.md](./PLAN.md) - D1 and R2 implementation plan
