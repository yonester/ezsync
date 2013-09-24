A *simple* utility to run a pre-configured backup set using rsync.

Typical usage would look something like this:

Run all profiles:

    $ python ezsync.py

Run all profiles named "docs":

    $ python ezsync.py --profile docs

Run profiles named "photos" email me when done:

    $ python ezsync.py -p photos -e user@server.com

Configuration is read from `config.json`. See the included file as an example
of proper configuration parameters.
