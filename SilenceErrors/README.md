Provides a command to silence any errors that might arise from executing a subcommand

Usage:
```
<user> %silence [echo test]
<bot> test
<user> %silence [invalid command]
< no response >
```

Primarily made to be used with a MessageParser set to execute commands.
For example:
```
%MessageParser add "%(.*)%" "silence $1"
```