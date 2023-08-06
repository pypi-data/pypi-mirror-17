README for pwclip - http://packages.python.org/pwclip/
======================================================

pwclip is a small tool to generate (via yubikey challenge-response) password
hashes. The first yubikey found on system and the first slot, configured with
challenge-response, will be used. Linux (with xsel), Windows and OSX (pbcopy)
is supported. Using python3's Tk library to create a password input window.
If no text is inserted there will be a challenge-response for that empty
string. The appropriate response is saved for only 3 seconds by default. The 
utility also supports the input of any integer number which is then used as
timer. Otherwise the environment is searched for the variable PWCLIPTIME and
if set uses the vaule of that environment-variable as timer.

Install
-------

pwclip requires the "xsel" package on Debian-Like Systems to have access to
copy/paste buffers. On Windows Systems the libusb package must be integrated
to python3 as "USB-Backend" (see libusb documentation)

* https://wiki.ubuntuusers.de/xsel/
* https://sourceforge.net/projects/libusb/

If you are on a Debian-Like system the installation of the dependencies
should work like the following (on root terminal):

$ apt-get install xsel


Documentation
-------------
http://packages.python.org/pwclip/


