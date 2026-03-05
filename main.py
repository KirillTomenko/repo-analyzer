import sys
import os
from analyzer import analyze_repository
from rich.console import Console
from rich.panel import Panel

console = Console()

def main():
    if len(sys.argv) < 2:
        console.print(Panel(
            "[bold yellow]Usage:[/bold yellow]\n"
            "  python main.py [bold cyan]<github_repo_url>[/bold cyan]\n\n"
            "[bold yellow]Examples:[/bold yellow]\n"
            "  python main.py https://github.com/user/repo\n"
            "  docker run repo-analyzer https://github.com/user/repo",
            title="[bold red]❌ No repository URL provided[/bold red]",
            border_style="red"
        ))
        sys.exit(1)

    repo_url = sys.argv[1]

    if "github.com" not in repo_url:
        console.print("[bold red]❌ Please provide a valid GitHub URL[/bold red]")
        sys.exit(1)

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        console.print("[bold red]❌ OPENAI_API_KEY environment variable is not set[/bold red]")
        console.print("[dim]Run with: docker run -e OPENAI_API_KEY=your_key repo-analyzer <url>[/dim]")
        sys.exit(1)

    analyze_repository(repo_url, api_key)

if __name__ == "__main__":
    main()
