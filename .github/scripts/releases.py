from os import environ

from github import Github
from github.GitRelease import GitRelease

GITHUB_REPOSITORY = environ.get("GITHUB_REPOSITORY", "awtkns/fastapi-crudrouter")
GITHUB_TOKEN = environ.get("GH_TOKEN") or environ.get("GITHUB_TOKEN")
FILE_PATH = "docs/en/docs/releases.md"
COMMIT_MESSAGE = "🤖 auto update releases.md"

gh = Github(GITHUB_TOKEN)


def generate_header(r: GitRelease, separator: bool = False):
    header = ""
    if separator:
        header += "\n\n---\n"

    return (
        header
        + f"""
## [{r.title}]({r.html_url}){" { .releases } "}
{r.created_at.date()}
"""
    )


if __name__ == "__main__":
    repo = gh.get_repo(GITHUB_REPOSITORY)

    new_content = ""
    first = False
    for r in repo.get_releases():
        if not r.draft:
            new_content += generate_header(r, first)
            new_content += r.body
            first = True

    file = repo.get_contents(FILE_PATH)
    old_content = file.decoded_content.decode()

    if new_content == old_content:
        print("No new release information, Skipping.")
    else:
        print("Uploading new release documentation")

        repo.update_file(
            file.path, message=COMMIT_MESSAGE, content=new_content, sha=file.sha
        )
