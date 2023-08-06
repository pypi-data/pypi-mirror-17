# py-mpache #

## INSTALL ##

Installation is fairly simple.  Just do the standard install as root:

    tar -xvzf py-mpache-*.tar.gz
    cd py-mpache-*
    python setup.py install

You can not yet also install directly using *pip* or *easy_install* but once thats implimented the line will be

    pip install py-mpache


## USAGE ##

This library will follows the XML API.  If you follow the 
documentation on https://github.com/ampache/ampache/wiki/XML-API 

it is forked from crusty monkeys subsonic python wrapper and the intention is that calls to that wrapper will be identical to calls to this ampache wrapper.

So you can also view crusty monkeys subsonic documentation at http://stuffivelearned.org/doku.php?id=programming:python:py-sonic

## BASIC TUTORIAL ##

This is about as basic as it gets.  We are just going to set up the connection
and then get a couple of random songs.

```python
#!/usr/bin/env python

from pprint import pprint
import libmpache

# We pass in the base url, the username, password, and port number
# Be sure to use https:// if this is an ssl connection!
conn = libmpache.Connection('http://music.example.com' , 'myuser' , 
    'secretpass' , port=80)
# Let's get 2 completely random songs
songs = conn.getRandomSongs(size=2)
# We'll just pretty print the results we got to the terminal
pprint(songs)
```

As you can see, it's really pretty simple.  If you use the documentation 
provided in the library:

    pydoc libsonic.connection

or the api docs on subsonic.org (listed above), you should be able to make use
of your server without too much trouble.

Right now, only plain old dictionary structures are returned.  The plan 
for a later release includes the following:

* Proper object representations for Artist, Album, Song, etc.
* Lazy access of members (the song objects aren't created until you want to
  do something with them)

## TODO ##
I havent started yet but changes required will be to parse the XML from the ampache server and return lists as per py-sonic.

My intention is to incorporate every api call available from the latest ampache api version so as to maximise the possible outputs from this wrapper

Ultimately once list returns are working I want to build another project linking this wrapper as a backend to mopidy. Probably based on the mopidy-subsonic extension.
