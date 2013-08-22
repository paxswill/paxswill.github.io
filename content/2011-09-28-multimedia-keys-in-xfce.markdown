---
layout: post
title: "Multimedia Keys in Xfce"
date: 2011-09-28 17:56
comments: true
categories: linux
published: false
---

After I got my [keyboard working](linky), I wanted to get my media keys
working with my system. In GNOME there are some helper tools, but I
didn't find a whole lot information abuot setting them up with Xfce. One
of the features I really wanted was a broadcast/multiple application
system, similar to what has been done in OS X where the media keys
interact with the last used media application. To this end I used
[Remoot](http://www.remoot.org/). While Remoot hasn't been updated in a
long time, it still works well, and has the features I need.

To install, just download the .deb
[package](http://sourceforge.net/projects/remoot/files/remoot/0.9/remoot.deb/download)
 and install it with `dpkg`. The only dependency I encountered was
 `perl-tk`, so install that as well.

```
# aptitude install perl-tk
# dpkg -i remoot.deb
```

To actually have the keys do something, open the Keyboard settings
dialog and add shortcuts for `/usr/bin/remoot action`, where action is
`playpause`, `prev`, and `next`.

NOTE: Add VLC support
