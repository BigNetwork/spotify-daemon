# Intro

A Spotify player that fetches songs from an URL and plays the first song found (it parses it as XML and searches for first item with an href attribute).

Made to work with BIP:

http://github.com/Bignetwork/BIP

But should be able to work with other things. 

Developers:
* Jonathan Ström
* Victor Sollerhed
		
# How to use:

    $ python client.py -u USERNAME -p PASSWORD

It only works with premium accounts (since those are Spotifys rules for libspotify).

# Requirements

* libspotify
* pyspotify
* pygame (for playing ads between songs)

## libspotify:

http://developer.spotify.com/en/libspotify/overview/

### How to install

#### On Mac:

    brew install libspotify

#### On Linux: 

(old, new instructions for libspotify-0.0.6 might be needed)

    wget https://developer.spotify.com/download/libspotify/libspotify-0.0.4-linux6-i686.tar.gz
    tar xzf libspotify-*.tar.gz
    cd libspotify-*
    sudo make install prefix=/usr/local
    (export LD_LIBARY_PATH=${LD_LIBRARY_PATH}:/usr/local/lib/)

## pyspotify: 

Specifically jodals fork (because it's the most updated one): 

http://github.com/jodal/pyspotify

### How to install:

#### On Mac:

    git clone http://github.com/jodal/pyspotify.git
    sudo setup.py instalal

The prefix used on Linux might be needed on Mac aswell, not sure, needs testing. 

#### On Linux:

    git clone http://github.com/jodal/pyspotify.git
    sudo setup.py install --prefix=/usr/local

Or see these instructions:

http://www.mopidy.com/docs/master/installation/libspotify/

## pygame (for ads-player):

### How to install:

#### On Linux:

    sudo apt-get install python-pygame
