A *simple* utility to run a pre-configured backup set using rsync.

Typical usage would look something like this:

Run the "docs" profile:

    $ python ezsync.py docs

Configuration is read from a file called `config.json` which is formatted as follows:

    {
        "excludes" : ["<exclude_pattern>", ...],
        "flags": "<rsync_flags>",
        "profiles": {
            "<profile_name>": {
                "source": "<source_path>",
                "target": "<target_path>",
                "excludes": ["<exclude_pattern", ...]
            },
            ...
        }
    }

See the included file as an example.