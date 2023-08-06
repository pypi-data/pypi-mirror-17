nclib is netcat as a python library, or at least a couple of common things
netcat can do.

nclib provides:
- Easy-to-use interfaces for connecting to and listening on TCP and UDP sockets
- recv_until, receiving until a given substring comes over the wire
- Highly customizable logging, including logging in hex encoding
- Interactive mode, connecting the socket to your stdin/stdout
- Intelligent detection of socket closes and connection drops
- Long-running functions cleanly abortable with ctrl-c
- Lots of aliases in case you forget the right method name
- A script (serve-stdio) to easily daemonize command-line scripts, requires socat

run help(nclib) for help.

If you are familiar with pwntools, nclib provides much of the functionaly that
pwntools' socket wrappers do, but with the bonus feature of not being pwntools.


