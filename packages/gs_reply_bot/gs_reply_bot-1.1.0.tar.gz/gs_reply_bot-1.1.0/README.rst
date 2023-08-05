gs_reply_bot
============
Installation
------------

``pip install gs_reply_bot``

or

``python3 setup.py install``


Basic usage
-----------

Set the configuration parameters in the default location (``$XDG_CONFIG_HOME/gs_reply_bot/config.json``) or supply it to the script with ``-c``.

Configuration example:

::

    {
        "server_url": "https://gnusocial.server",
        "username": "username",
        "password": "password",
        "users": {
            "user@gnusocial.server": ["message", "another message"]
        }
    }
