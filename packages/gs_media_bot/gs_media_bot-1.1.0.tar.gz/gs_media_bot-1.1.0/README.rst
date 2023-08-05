gs_media_bot
==============
Bot for posting media to GNU Social.

Installation
------------

``pip install gs_media_bot``

or

``python3 setup.py install``

Basic usage
-----------

Set the configuration parameters in the default location (``$XDG_CONFIG_HOME/gs_media_bot/config.json``) or supply it to the script with ``-c``.

Configuration example:

::

    {
        "credentials": {"server_url": "https://gnusocial.server",
        "username": "username",
        "password": "password",
        },
        "dirs": {
            "~/My_Cool_Photos/": "Yet another photo!"
        }
    }
