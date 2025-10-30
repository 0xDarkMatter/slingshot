# Quick Start Guide

Get your first Cloudflare Worker deployed in 5 minutes!

## Prerequisites

- Python 3.10 or higher
- Cloudflare account (free tier works!)

## Step 1: Install CFWorker

```bash
# Navigate to CFWorker directory
cd CFWorker

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install
pip install -e .
```

Verify installation:
```bash
cfworker --version
```

## Step 2: Get Cloudflare Credentials

### Get Account ID
1. Go to https://dash.cloudflare.com
2. Look in the right sidebar - you'll see your Account ID
3. Copy it!

### Get API Token
1. Go to https://dash.cloudflare.com/profile/api-tokens
2. Click "Create Token"
3. Use "Edit Cloudflare Workers" template
4. Click "Continue to summary" then "Create Token"
5. Copy the token (you won't see it again!)

### Save Credentials

Run the setup wizard:
```bash
cfworker config-setup
```

Or create `.env` manually:
```bash
CLOUDFLARE_ACCOUNT_ID=your_account_id_here
CLOUDFLARE_API_TOKEN=your_api_token_here
```

**Important Security Note**: On Unix/Linux systems, set restrictive permissions on your `.env` file:
```bash
chmod 600 .env
```
This prevents other users from reading your Cloudflare credentials.

## Step 3: Create Your First Worker

```bash
# Create a simple API worker
cfworker init my-first-worker --template api
```

This creates:
- `.cfworker.json` - configuration
- `worker.js` - your code

## Step 4: Deploy!

```bash
cfworker deploy
```

That's it! Your worker is now live at:
```
https://my-first-worker.workers.dev
```

## Step 5: Test Your Worker

Open in browser:
```
https://my-first-worker.workers.dev/api/hello
```

You should see:
```json
{
  "message": "Hello, World!",
  "timestamp": 1234567890
}
```

## Security Best Practices

Before moving forward, understand these security considerations:

### 1. Protect Your Credentials
- **Never commit** `.env` files to version control (already in `.gitignore`)
- Set restrictive permissions: `chmod 600 .env` (Unix/Linux)
- Rotate your API tokens regularly

### 2. Review Code Before Deploying
- Check for hardcoded secrets or API keys
- Use environment variables for sensitive data
- Test deployments with `--dry-run` flag

### 3. Use Version Control
```bash
# Commit before deploying
git add worker.js .cfworker.json
git commit -m "Update worker implementation"
cfworker deploy
```

This allows easy rollback if something goes wrong.

## Next Steps

### Customize Your Worker

Edit `worker.js`:
```javascript
export default {
  async fetch(request, env, ctx) {
    return Response.json({
      message: "Hello from my custom worker!",
      yourName: "YOUR NAME HERE"
    });
  },
};
```

Deploy again:
```bash
cfworker deploy
```

### Try Different Templates

```bash
# Static website
cfworker init my-site --template static

# Edge function
cfworker init my-function --template edge
```

### Manage Your Workers

```bash
# List all workers
cfworker list

# Get worker details
cfworker info

# Delete a worker
cfworker delete
```

## Common Use Cases

### 1. Quick REST API
Perfect for: Backend APIs, webhooks, microservices

```bash
cfworker init my-api --template api
# Edit worker.js to add your endpoints
cfworker deploy
```

### 2. Static Website
Perfect for: Landing pages, portfolios, documentation

```bash
cfworker init my-site --template static
# Edit worker.js to customize HTML
cfworker deploy
```

### 3. Edge Function
Perfect for: Data processing, redirects, A/B testing

```bash
cfworker init my-function --template edge
# Edit worker.js for your logic
cfworker deploy
```

## Tips

### Rapid Iteration

Make changes to `worker.js`, then:
```bash
cfworker deploy
```

Changes are live in seconds!

### Validate Before Deploying

```bash
cfworker deploy --dry-run
```

### Multiple Projects

Each project needs its own directory with `.cfworker.json`:

```
projects/
├── api-project/
│   ├── .cfworker.json
│   └── worker.js
├── website-project/
│   ├── .cfworker.json
│   └── worker.js
```

### Environment Variables

Add to `.cfworker.json`:
```json
{
  "worker_name": "my-worker",
  "vars": {
    "API_KEY": "secret123",
    "ENVIRONMENT": "production"
  }
}
```

Access in worker:
```javascript
const apiKey = env.API_KEY;
```

## Troubleshooting

**"Invalid API credentials"**
- Double-check your `.env` file
- Ensure API token has Workers Scripts:Edit permission

**"Script not found"**
- Make sure `worker.js` exists
- Check you're in the right directory

**"Worker name already exists"**
- Change `worker_name` in `.cfworker.json`
- Or delete the old worker: `cfworker delete`

## Need Help?

- Check `README.md` for full documentation
- See `examples/` directory for code samples
- Review `.claude/agents/cloudflare-expert.md` for best practices

## Ready to Build?

You now have everything you need to:
- Prototype ideas quickly
- Deploy to production
- Scale globally with Cloudflare's edge network

Happy building! 🚀
