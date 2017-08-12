While not actually a plugin; a complicated aka and a messageparser are used to bring fully featured regex-like substitutions on IRC.
Depends on the following plugins:
+ Aka
+ Conditional
+ Format
+ MessageParser
+ String
+ Utilities

**Please Note:** You need to be running a recent version of Limnoria, as the MessageParser relies on this bugfix https://github.com/ProgVal/Limnoria/commit/417f38b8c14351701280a2197ab120fe4337a33a

The first part, being the histsearch aka, can be added using the following:
```
%aka add histsearch "last --from [cif [ceq \"@3\" \"\"] \"echo $nick\" \"echo @3\"] --regexp [concat \"m/$1/\" [re s/g// \"@2\"]]"
```
The histsearch command searches the past logs in the channel and returns the match, syntax is
```
%histsearch "<string>" [flags] [user]
```

Next, the MessageParser needs to be added.
```
%messageparser add "^s/(.+)/(.*)/([^\s]*) ?(.*)" "echo Correction: [cif [ceq \"$4\" \"\"] \"echo <$nick>\" \"echo <$4>\"] [re \"s/$1/$2/$3\" [histsearch \"$1\" \"$3\" \"$4\"]]"
```

Some usage examples:
```
<User> This is a tset
<User> s/set$/est/
<Bot> Correction: <User> This is a test
```

```
<User> This AA is AA another AA test
<User> s/aa //gi
<Bot> Correction: <User> This is another test
```

```
<User1> This can be something
<User2> s/some/any/ User1
<Bot> Correction: <User1> This can be anything
```

```
<User> The results are known
<User> s/(kn.*)/un\\1/
<Bot> Correction: <User> The results are unknown
```
