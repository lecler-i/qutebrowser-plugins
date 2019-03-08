# My Qutebrowser plugins

This is using some core api of qutebrowser, any change in qutebrowser
can break those plugins ! They are relatively small so it should not be
an issue to fix.

### Buku integration

Replace the bookmark and quickmark of qutebrowser to use `buku` library.


### How to setup

Link the `init_custom_plugins.py` to your qutebrowser config dir.

`ln -s ${pwd}/init_custom_plugins.py $XDG_CONFIG_HOME/qutebrowser/`

In your `config.py` file add the following line : 

`config.source("init_custom_plugins.py")`

### Todo

Make the plugins to activate configurable in `config.py`


