# slot

Install
-------

* python3 is required

```
$ sudo pip3 install lark-parser
$ git clone https://github.com/jjsaio/slot
$ cd slot
$ ./bin/slot interactive
>s> |x|
  <Slot:*>
>s> .q
Bye!
```

Some examples
-------------

This will show some of the basic operation of interactive-mode:

```
$ ./bin/slot interactive
>s> .b misc/demo.batch
[INFO Slot] batch start:  misc/demo.batch
...
[INFO Slot] batch done
>s> 
```

You can enter `.h` at the interactive prompt for some (very basic) help.

