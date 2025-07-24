Flow control for media stream
-----------------------------

The server's sending rate automatically adapts to the MP3 player's bitrate thanks to flow control.

Preguntar a ChatGPT


run server:

```
$ ./server.py 2000 | mplayer -quiet -
```

run client:

```
$ ./client.py localhost 2000 < audio.mp3
```
