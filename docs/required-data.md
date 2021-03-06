### Proposal of information stored per python project

```json
{
    "name": "pyzote2",
    "git_repository": {
        "flavour": "github|gerrit|git",
        "url": "git@github.com:TheCompany/infra-utils.git",
        "upstream_url": "git@github.com:TheCompany/infra-utils.git",
        "github_api_address": "http://api.github.com",
        "github_project_name": "infra-utils",
        "github_project_owner": "owner"
    },
    "namespace": "infrastructure/utils",
    "tags": [
        "tools", "infra"
    ],
    "requirementsFiles": [
        {
            "name": "requirements.txt",
            "status": "up-to-date",
            "requirements": [
                {
                    "name": "requests",
                    "status": "up-to-date",
                    "current-version": ">=2.11.0",
                    "desired-version": "2.13.0"
                }
            ]
        },
        {
            "name": "requirements-development.txt",
            "status": "up-to-date",
            "requirements": [
                {
                    "name": "ipython",
                    "status": "up-to-date",
                    "current-version": ">=5.3.0",
                    "desired-version": "6.0.0"
                }
            ]
        }
    ]
}
```

Upstream_url is required for working in github-flow. Should point to original repository (not clone).
Gerrit-flow assumes that `.gerrit` file is placed in root project directory.
