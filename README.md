# dchelp

Console tool for managing docker-compose projects.

Capabilities:
- list projects
- up and down project
- reset all active projects
- extra features (live mode, common statistics)

![](example.gif)

## Install

```
git clone https://github.com/smokehill/dchelp.git
cd dchelp/
make install
dchelp
```

## Settings

After installation fill `~/.config/dchelp/data.json` with your projects list.

Example:
```json
[
    {
        "title": "project",
        "path": "/path/to/project/"
    }
]
```