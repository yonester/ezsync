A *simple* utility to run a pre-configured backup set using rsync.

Typical usage would look something like this:

Run the "docs" profile:

    $ python ezsync.py docs

Configuration is read from a file called `config.json` which is formatted as follows:

    {
        "excludes" : ["<exclude_pattern>", ...],
        "flags": "<global_flags>",
        "profiles": {
            "<profile_name>": {
                "source": "<source_dir>",
                "target": "<target_dir>",
                "pairs": [
                    ["<source_subdir>", "<target_subdir>", "<optional_flags>"],
                    ...
                ]
            },
            ...
        }
    }

See the included file as an example.

Some limitations that could (should) be improved:

* Add flags for each profile. This could be useful when some pairs back up to a remote server and need extra flags to specify a secure shell, for example.

* Add an argument to only run a certain pair in a profile. Would give a bit more flexibility than having to create another profile.

* Maybe get rid of <target_subdir> if there isn't any?