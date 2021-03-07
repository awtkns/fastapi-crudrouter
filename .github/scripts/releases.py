from os import environ
from pathlib import Path

from github import Github
from github.GitRelease import GitRelease

GITHUB_REPOSITORY = environ.get('GITHUB_REPOSITORY')
GITHUB_TOKEN = environ.get('GITHUB_TOKEN')
FILE_PATH = "docs/en/docs/releases.md"
COMMIT_MESSAGE = "🤖 auto update releases.md"

gh = Github(GITHUB_TOKEN)


def generate_header(r: GitRelease, separator: bool = False):
    header = ''
    if separator:
        header += "\n\n---\n"

    return header + f"""
## [{r.title}]({r.html_url}){" { .releases } "}
{r.created_at.date()}
"""


if __name__ == '__main__':
    repo = gh.get_repo(GITHUB_REPOSITORY)

    content = ''
    first = False
    for r in repo.get_releases():
        if not r.draft:
            content += generate_header(r, first)
            content += r.body
            first = True

    contents = repo.get_contents(FILE_PATH)
    repo.update_file(
        contents.path,
        message=COMMIT_MESSAGE,
        content=content,
        sha=contents.sha
    )