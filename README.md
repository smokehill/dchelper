# dchelp

Console tool that helps to up and down local projects via docker-compose.

## Install

<pre>
git clone https://github.com/smokehill/dchelp.git
cd dchelp/
make install
dchelp
</pre>

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

## Example

![](example.gif)