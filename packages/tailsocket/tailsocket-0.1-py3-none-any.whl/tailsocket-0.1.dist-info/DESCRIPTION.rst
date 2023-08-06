# Tailsocket

A WebSocket application to tail files.

You've set up your machine and you're tweaking config files to get it just right, this last bit should do it... oh, it doesn't? Weird, where's that log again? Damn, I know it's in the history somewhere, or did I have it on screen/tmux? Which one? :/

I say no more! `pip install tailsocket`, run `tailsocket-server`, write the path to the log file *once* and let the logs come to you!

Ok, maybe I'm being a bit dramatic, but I've found this frustrating sometimes and seemed like a good use for WebSockets so I put this little project together using Tornado, asyncio and React.

Keep in mind Tailsocket can only read from files the owner of the process can read from.

Try it out at http://tailsocket.herokuapp.com/

## Issues

- Fallback to `select` on Linux causes high CPU loads and spam on the application logs.
- Changing a tailed log file does not show confirmation, simply new log entries.
- Application messages and errors show in the same context as log entries.

## Enhancements

- Globbing
- Multiple log screens

