#Pronto
Quick OSINT on twitter accounts.

Platforms:
---------
- Linux cli

Python Dependencies:
--------------------
1. python2
2. requests

Basic Usage:
------------
    ./pronto.py -i [ID-NUMBER] | Turn an ID into a Username.

    ./pronto.py -n [USERNAME] | Turn a Username into an ID.

    ./pronto.py -e [USERNAME] | Output basic profile account information.

    ./pronto.py -v [USERNAME] | Visualize a users tweets.

    ./pronto.py --tweets [USERNAME] | Collect all of a Users tweets.

    ./pronto.py --followers [USERAME] | Download all of the followers a twitter handle has.

    ./pronto.py --following [USERAME] s| Download all of the twitter handles that a user is following.

Donations:
----------
- 17vorVqtJqbDaN6ZC6UGE7UwGC4QVmDNMh

Protip:
-------
1. Whenever you collect something from a user, a directory will be made for said user, containing all the information that you've collected from them.
2. Usernames are case sensitive, if a case insensitive username is used '0' items will be collected or written to disk.
