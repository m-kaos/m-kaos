"""Collect last-12-month commit stats for the profile README.

Walks every repository the token can see (own repos plus the configured orgs),
keeps only commits authored by the profile owner and writes aggregated numbers
to data/stats.json. Repository names never leave the run.

Env:
  STATS_TOKEN          token with read access to every repo to count (required)
  STATS_AUTHOR_EMAILS  extra commit emails that belong to the owner, comma-separated
"""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Iterator
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

API = "https://api.github.com"
LOGIN = "m-kaos"
ORGS = ("SalesHub-Agency",)
KAOS_REPO = "m-kaos/Parthenon"
SKIP_SUFFIXES = ("-clon",)
LOCAL_TZ = timezone(timedelta(hours=-6))  # Monterrey, no DST since 2022
OUT = Path(__file__).resolve().parent.parent / "data" / "stats.json"


class GitHubError(RuntimeError):
    """Raised when the API answers with an unexpected status."""


def next_link(header: str | None) -> str | None:
    if not header:
        return None
    for part in header.split(","):
        url, _, rel = part.partition(";")
        if 'rel="next"' in rel:
            return url.strip()[1:-1]
    return None


def fetch(url: str, token: str) -> tuple[list[dict], str | None]:
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "profile-stats",
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as res:
            return json.loads(res.read().decode("utf-8")), next_link(res.headers.get("Link"))
    except urllib.error.HTTPError as err:
        if err.code == 409:  # empty repository
            return [], None
        detail = err.read().decode("utf-8", "replace")[:200]
        raise GitHubError(f"{err.code} on {url}: {detail}") from err


def paginate(url: str, token: str) -> Iterator[dict]:
    next_url: str | None = url
    while next_url:
        page, next_url = fetch(next_url, token)
        yield from page


def active_repos(token: str, since: datetime) -> list[str]:
    sources = [f"{API}/user/repos?affiliation=owner&per_page=100"]
    sources += [f"{API}/orgs/{org}/repos?type=all&per_page=100" for org in ORGS]
    names: set[str] = set()
    for source in sources:
        for repo in paginate(source, token):
            pushed = repo.get("pushed_at")
            if not pushed or datetime.fromisoformat(pushed.replace("Z", "+00:00")) < since:
                continue
            if repo["name"].endswith(SKIP_SUFFIXES):
                continue
            names.add(repo["full_name"])
    return sorted(names)


def longest_streak(daily: list[int]) -> int:
    best = current = 0
    for count in daily:
        current = current + 1 if count else 0
        best = max(best, current)
    return best


def main() -> int:
    token = os.environ.get("STATS_TOKEN", "").strip()
    if not token:
        print("STATS_TOKEN is not set", file=sys.stderr)
        return 1
    emails = {e.strip().lower() for e in os.environ.get("STATS_AUTHOR_EMAILS", "").split(",") if e.strip()}

    end = datetime.now(LOCAL_TZ).date() - timedelta(days=1)
    start = end - timedelta(days=364)
    since = datetime.combine(start, datetime.min.time(), LOCAL_TZ)
    until = datetime.combine(end + timedelta(days=1), datetime.min.time(), LOCAL_TZ)

    daily = [0] * 365
    punch = [[0] * 24 for _ in range(7)]
    repos_with_commits: set[str] = set()
    kaos_commits = 0

    query = urllib.parse.urlencode({
        "since": since.astimezone(timezone.utc).isoformat(),
        "until": until.astimezone(timezone.utc).isoformat(),
        "per_page": 100,
    })
    for full_name in active_repos(token, since):
        for item in paginate(f"{API}/repos/{full_name}/commits?{query}", token):
            login = (item.get("author") or {}).get("login", "")
            commit_author = item["commit"]["author"]
            if login != LOGIN and commit_author.get("email", "").lower() not in emails:
                continue
            when = datetime.fromisoformat(commit_author["date"].replace("Z", "+00:00")).astimezone(LOCAL_TZ)
            index = (when.date() - start).days
            if not 0 <= index < 365:
                continue
            daily[index] += 1
            punch[when.weekday()][when.hour] += 1
            repos_with_commits.add(full_name)
            kaos_commits += full_name == KAOS_REPO

    stats = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "start": start.isoformat(),
        "end": end.isoformat(),
        "commits": sum(daily),
        "repositories": len(repos_with_commits),
        "active_days": sum(1 for c in daily if c),
        "longest_streak": longest_streak(daily),
        "kaos_commits": kaos_commits,
        "daily": daily,
        "punch": punch,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(stats, indent=2) + "\n", encoding="utf-8")
    print(f"{stats['commits']} commits in {stats['repositories']} repos, {start} to {end}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
