### Proposal of information stored per python project

```json
{
    "name": "pyzote2",
    "url": "git@github.com:TheCompany/infra-utils.git",
    "namespace": "infrastructure/utils",
    "tags": [
        "tools", "infra"
    ],
    "requirements": [
        {
            "name": "requirements.txt",
            "packages": [
                {
                    "name": "requests",
                    "current-version": ">=2.11.0",
                    "desired-version": "2.13.0"
                }
            ]
        },
        {
            "name": "requirements-development.txt",
            "packages": [
                {
                    "name": "ipython",
                    "current-version": ">=5.3.0",
                    "desired-version": "6.0.0"
                }
            ]
        }
    ]
}
```