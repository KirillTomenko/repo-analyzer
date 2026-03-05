import re
import requests
from openai import OpenAI
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import box
from datetime import datetime

console = Console()


def parse_github_url(url: str) -> tuple[str, str]:
    """Extract owner and repo name from GitHub URL."""
    url = url.rstrip("/").replace(".git", "")
    match = re.search(r"github\.com/([^/]+)/([^/]+)", url)
    if not match:
        raise ValueError(f"Cannot parse GitHub URL: {url}")
    return match.group(1), match.group(2)


def fetch_repo_data(owner: str, repo: str) -> dict:
    """Fetch repository metadata, README and file tree from GitHub API."""
    headers = {"Accept": "application/vnd.github.v3+json"}
    base = f"https://api.github.com/repos/{owner}/{repo}"

    # Repo metadata
    r = requests.get(base, headers=headers, timeout=10)
    r.raise_for_status()
    meta = r.json()

    # README
    readme_text = ""
    try:
        r2 = requests.get(f"{base}/readme", headers={**headers, "Accept": "application/vnd.github.v3.raw"}, timeout=10)
        if r2.status_code == 200:
            readme_text = r2.text[:3000]
    except Exception:
        pass

    # File tree (top level)
    file_list = []
    try:
        r3 = requests.get(f"{base}/git/trees/HEAD?recursive=0", headers=headers, timeout=10)
        if r3.status_code == 200:
            tree = r3.json().get("tree", [])
            file_list = [item["path"] for item in tree if item["type"] == "blob"][:40]
    except Exception:
        pass

    # Languages
    languages = {}
    try:
        r4 = requests.get(f"{base}/languages", headers=headers, timeout=10)
        if r4.status_code == 200:
            languages = r4.json()
    except Exception:
        pass

    # Recent commits
    commits = []
    try:
        r5 = requests.get(f"{base}/commits?per_page=5", headers=headers, timeout=10)
        if r5.status_code == 200:
            for c in r5.json():
                commits.append(c["commit"]["message"].split("\n")[0])
    except Exception:
        pass

    return {
        "name": meta.get("name"),
        "full_name": meta.get("full_name"),
        "description": meta.get("description", "No description"),
        "stars": meta.get("stargazers_count", 0),
        "forks": meta.get("forks_count", 0),
        "open_issues": meta.get("open_issues_count", 0),
        "language": meta.get("language", "Unknown"),
        "created_at": meta.get("created_at", ""),
        "updated_at": meta.get("updated_at", ""),
        "license": meta.get("license", {}).get("name", "No license") if meta.get("license") else "No license",
        "readme": readme_text,
        "files": file_list,
        "languages": languages,
        "commits": commits,
        "topics": meta.get("topics", []),
        "has_ci": any(f in [".github/workflows", "Jenkinsfile", ".travis.yml", "circle.yml"] for f in file_list),
    }


def analyze_with_gpt(data: dict, api_key: str) -> str:
    """Send repo data to GPT-4o and get structured analysis."""
    client = OpenAI(api_key=api_key)

    prompt = f"""You are a senior software engineer doing a professional code repository review.

Analyze this GitHub repository and provide a structured report in Markdown.

## Repository Data:
- **Name:** {data['full_name']}
- **Description:** {data['description']}
- **Primary Language:** {data['language']}
- **All Languages:** {data['languages']}
- **Stars:** {data['stars']} | **Forks:** {data['forks']} | **Open Issues:** {data['open_issues']}
- **License:** {data['license']}
- **Topics/Tags:** {data['topics']}
- **Has CI/CD:** {data['has_ci']}
- **Recent commits:** {data['commits']}

## File Structure:
{chr(10).join(data['files'][:30])}

## README (first 3000 chars):
{data['readme'][:2000] if data['readme'] else 'No README found'}

---

Provide your analysis in this EXACT Markdown structure:

## 🎯 Project Overview
Brief 2-3 sentence summary of what this project does and its purpose.

## ✅ Strengths
- List 3-5 genuine strengths with brief explanations

## ⚠️ Areas for Improvement
- List 3-5 specific, actionable improvements

## 🔒 Security & Best Practices
Assessment of security practices, secrets management, dependency management.

## 📁 Code Structure & Architecture
Assessment of project organization, separation of concerns, maintainability.

## 📊 Overall Score
Provide scores (1-10) for:
- Code Quality: X/10
- Documentation: X/10
- Security: X/10
- Architecture: X/10
- **Overall: X/10**

## 🚀 Top 3 Priority Actions
Numbered list of the 3 most impactful things to do next.

Be specific and technical. Base your analysis on actual files and README content."""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1500,
        temperature=0.3,
    )

    return response.choices[0].message.content


def print_repo_header(data: dict):
    """Print a nice header with repo metadata."""
    table = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
    table.add_column("Key", style="bold cyan", width=18)
    table.add_column("Value", style="white")

    updated = data["updated_at"][:10] if data["updated_at"] else "—"
    created = data["created_at"][:10] if data["created_at"] else "—"

    table.add_row("⭐ Stars", str(data["stars"]))
    table.add_row("🍴 Forks", str(data["forks"]))
    table.add_row("🐛 Open Issues", str(data["open_issues"]))
    table.add_row("📝 License", data["license"])
    table.add_row("🗓 Created", created)
    table.add_row("🔄 Last Updated", updated)
    if data["topics"]:
        table.add_row("🏷 Topics", ", ".join(data["topics"]))

    console.print(Panel(
        table,
        title=f"[bold green]🔍 {data['full_name']}[/bold green]",
        subtitle=f"[dim]{data['description']}[/dim]",
        border_style="green"
    ))


def analyze_repository(repo_url: str, api_key: str):
    """Main function: fetch data, analyze, print report."""
    owner, repo = parse_github_url(repo_url)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    ) as progress:
        task1 = progress.add_task("[cyan]Fetching repository data from GitHub...", total=None)
        try:
            data = fetch_repo_data(owner, repo)
        except requests.exceptions.HTTPError as e:
            console.print(f"[bold red]❌ GitHub API error: {e}[/bold red]")
            return
        progress.update(task1, description="[green]✓ Repository data fetched")

        task2 = progress.add_task("[cyan]Analyzing with GPT-4o...", total=None)
        analysis = analyze_with_gpt(data, api_key)
        progress.update(task2, description="[green]✓ Analysis complete")

    console.print()
    print_repo_header(data)
    console.print()
    console.print(Panel(
        Markdown(analysis),
        title="[bold magenta]🤖 AI Analysis Report[/bold magenta]",
        border_style="magenta",
        padding=(1, 2)
    ))
    console.print()
    console.print(f"[dim]Generated by repo-analyzer • {datetime.now().strftime('%Y-%m-%d %H:%M')}[/dim]")
