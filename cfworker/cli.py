"""CLI interface for CFWorker."""

import sys
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.table import Table
from rich import print as rprint

from . import __version__
from .config import Config
from .deployer import WorkerDeployer, DeploymentError

console = Console()


@click.group()
@click.version_option(version=__version__)
def main():
    """CFWorker - Deploy and manage Cloudflare Workers with ease."""
    pass


@main.command()
@click.argument('worker_name')
@click.option('--template', '-t', type=click.Choice(['api', 'static', 'edge']), default='edge',
              help='Worker template to use')
@click.option('--force', '-f', is_flag=True, help='Overwrite existing files')
def init(worker_name: str, template: str, force: bool):
    """Initialize a new worker project.

    Creates a .cfworker.json config file and a basic worker script from a template.
    """
    config_path = Path.cwd() / ".cfworker.json"
    worker_path = Path.cwd() / "worker.js"

    # Check if files already exist
    if config_path.exists() and not force:
        console.print("[red]Error:[/red] .cfworker.json already exists. Use --force to overwrite.")
        sys.exit(1)

    if worker_path.exists() and not force:
        console.print("[red]Error:[/red] worker.js already exists. Use --force to overwrite.")
        sys.exit(1)

    # Create config file
    try:
        config = Config.create_default(worker_name, str(config_path))
        console.print(f"[green]✓[/green] Created .cfworker.json")
    except Exception as e:
        console.print(f"[red]Error:[/red] Failed to create config: {e}")
        sys.exit(1)

    # Create worker script from template
    template_content = _get_template_content(template)
    try:
        with open(worker_path, 'w') as f:
            f.write(template_content)
        console.print(f"[green]✓[/green] Created worker.js from '{template}' template")
    except Exception as e:
        console.print(f"[red]Error:[/red] Failed to create worker script: {e}")
        sys.exit(1)

    # Create .env file if it doesn't exist
    env_path = Path.cwd() / ".env"
    if not env_path.exists():
        with open(env_path, 'w') as f:
            f.write("CLOUDFLARE_ACCOUNT_ID=your_account_id_here\n")
            f.write("CLOUDFLARE_API_TOKEN=your_api_token_here\n")
        console.print(f"[green]✓[/green] Created .env file")
        console.print("\n[yellow]Next steps:[/yellow]")
        console.print("1. Edit .env and add your Cloudflare credentials")
        console.print("2. Edit worker.js to implement your worker logic")
        console.print("3. Run 'cfworker deploy' to deploy your worker")
    else:
        console.print("\n[yellow]Next steps:[/yellow]")
        console.print("1. Edit worker.js to implement your worker logic")
        console.print("2. Run 'cfworker deploy' to deploy your worker")


@main.command()
@click.option('--config', '-c', default=None, help='Path to .cfworker.json config file')
@click.option('--dry-run', is_flag=True, help='Validate without deploying')
def deploy(config: Optional[str], dry_run: bool):
    """Deploy worker to Cloudflare.

    Reads the configuration from .cfworker.json and deploys the worker script.
    """
    try:
        # Load configuration
        cfg = Config(config)

        # Validate credentials
        if not cfg.account_id or not cfg.api_token:
            console.print("[red]Error:[/red] Cloudflare credentials not configured.")
            console.print("Set CLOUDFLARE_ACCOUNT_ID and CLOUDFLARE_API_TOKEN in your .env file.")
            sys.exit(1)

        # Initialize deployer
        with console.status("[bold green]Preparing deployment..."):
            deployer = WorkerDeployer(cfg)

        # Verify connection first
        if not dry_run:
            with console.status("[bold green]Verifying API connection..."):
                if not deployer.verify_connection():
                    console.print("[red]Error:[/red] Invalid API credentials.")
                    sys.exit(1)
            console.print("[green]✓[/green] API connection verified")

        # Deploy
        mode = "Validating" if dry_run else "Deploying"
        with console.status(f"[bold green]{mode} worker..."):
            result = deployer.deploy(dry_run=dry_run)

        # Show results
        if dry_run:
            console.print(f"[green]✓[/green] Validation successful")
            console.print(f"Worker name: {result['worker_name']}")
            console.print(f"Script size: {result['script_size']} bytes")
        else:
            console.print(f"[green]✓[/green] Worker deployed successfully!")
            console.print(f"Worker name: {result['worker_name']}")
            console.print(f"Script size: {result['script_size']} bytes")
            console.print(f"\n[yellow]Your worker is now live at:[/yellow]")
            console.print(f"https://{result['worker_name']}.workers.dev")

    except DeploymentError as e:
        console.print(f"[red]Deployment failed:[/red] {e}")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@main.command()
@click.option('--config', '-c', default=None, help='Path to .cfworker.json config file')
@click.confirmation_option(prompt='Are you sure you want to delete this worker?')
def delete(config: Optional[str]):
    """Delete worker from Cloudflare.

    Removes the deployed worker. This action cannot be undone.
    """
    try:
        cfg = Config(config)
        deployer = WorkerDeployer(cfg)

        with console.status("[bold red]Deleting worker..."):
            result = deployer.delete()

        console.print(f"[green]✓[/green] Worker '{result['worker_name']}' deleted successfully")

    except DeploymentError as e:
        console.print(f"[red]Deletion failed:[/red] {e}")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@main.command()
@click.option('--config', '-c', default=None, help='Path to .cfworker.json config file')
def info(config: Optional[str]):
    """Get information about deployed worker.

    Shows details about the currently deployed worker.
    """
    try:
        cfg = Config(config)
        deployer = WorkerDeployer(cfg)

        with console.status("[bold green]Fetching worker info..."):
            result = deployer.get_info()

        console.print(f"[green]✓[/green] Worker information:")
        rprint(result)

    except DeploymentError as e:
        console.print(f"[red]Failed to get info:[/red] {e}")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@main.command()
@click.option('--config', '-c', default=None, help='Path to .cfworker.json config file')
def list(config: Optional[str]):
    """List all workers in your account.

    Shows all deployed workers for the configured Cloudflare account.
    """
    try:
        cfg = Config(config)
        deployer = WorkerDeployer(cfg)

        with console.status("[bold green]Fetching workers..."):
            result = deployer.list_workers()

        if result['count'] == 0:
            console.print("[yellow]No workers found in your account.[/yellow]")
            return

        # Create table
        table = Table(title=f"Workers ({result['count']})")
        table.add_column("Name", style="cyan")
        table.add_column("Created", style="green")
        table.add_column("Modified", style="yellow")

        for worker in result['workers']:
            table.add_row(
                worker.get('id', 'N/A'),
                worker.get('created_on', 'N/A'),
                worker.get('modified_on', 'N/A')
            )

        console.print(table)

    except DeploymentError as e:
        console.print(f"[red]Failed to list workers:[/red] {e}")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@main.command()
def config_setup():
    """Interactive setup for Cloudflare credentials.

    Walks you through setting up your Cloudflare API credentials.
    """
    console.print("[bold]Cloudflare Credentials Setup[/bold]\n")
    console.print("You'll need:")
    console.print("1. Account ID - Found in your Cloudflare dashboard")
    console.print("2. API Token - Create one at https://dash.cloudflare.com/profile/api-tokens")
    console.print("   Required permissions: Workers Scripts:Edit\n")

    account_id = click.prompt("Enter your Cloudflare Account ID")
    api_token = click.prompt("Enter your Cloudflare API Token", hide_input=True)

    # Save to .env file
    env_path = Path.cwd() / ".env"
    with open(env_path, 'w') as f:
        f.write(f"CLOUDFLARE_ACCOUNT_ID={account_id}\n")
        f.write(f"CLOUDFLARE_API_TOKEN={api_token}\n")

    console.print(f"\n[green]✓[/green] Credentials saved to .env")

    # Verify credentials
    try:
        cfg = Config()
        deployer = WorkerDeployer(cfg)
        if deployer.verify_connection():
            console.print("[green]✓[/green] Credentials verified successfully!")
        else:
            console.print("[red]✗[/red] Credentials verification failed. Please check your API token.")
    except Exception as e:
        console.print(f"[red]✗[/red] Verification failed: {e}")


def _get_template_content(template: str) -> str:
    """Get worker template content.

    Args:
        template: Template name (api, static, edge)

    Returns:
        Template content
    """
    templates = {
        'edge': '''// Simple edge function worker
export default {
  async fetch(request, env, ctx) {
    return new Response('Hello from Cloudflare Workers!', {
      headers: { 'Content-Type': 'text/plain' },
    });
  },
};
''',
        'api': '''// REST API worker
export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const path = url.pathname;

    // Simple routing
    if (path === '/api/hello') {
      return Response.json({ message: 'Hello, World!' });
    }

    if (path === '/api/status') {
      return Response.json({ status: 'ok', timestamp: Date.now() });
    }

    // 404 for unknown routes
    return Response.json({ error: 'Not found' }, { status: 404 });
  },
};
''',
        'static': '''// Static site worker
const HTML = `
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>My Cloudflare Worker Site</title>
</head>
<body>
  <h1>Hello from Cloudflare Workers!</h1>
  <p>This is a static site served from the edge.</p>
</body>
</html>
`;

export default {
  async fetch(request, env, ctx) {
    return new Response(HTML, {
      headers: { 'Content-Type': 'text/html' },
    });
  },
};
'''
    }

    return templates.get(template, templates['edge'])


if __name__ == '__main__':
    main()
