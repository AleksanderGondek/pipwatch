### Proposal of information stored per python project

```json
{
    "name": "pyzote2",
    "url": "git@github.com:TheCompany/infra-utils.git",
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