---
layout: post
title: Ubuntu 10.04 on a Dell Mini 9
author: Will Ross
date: 2010-05-01
comments: true
---

The Mac OS X install on my Mini 9 was recently borked (friend was borrowing it, and
 an unclean shutdown corrupted the file system), and I didn't have the install 
discs on me. I'd also been messing with the Lucid Lynx beta in a VM on my machine,
 and was very impressed with the level of polish, so I decided to install Ubuntu on
 the Mini again and see how it went.
<!--more-->
This was a couple days before the release date, so I downloaded the release candidate
 and ran from there. I've used both the normal desktop and netbook remix in previous versions of Ubuntu, and for my workflow I prefer using the normal desktop. As there isn't a desktop .img available, I downloaded the desktop ISO and used the USB IMage Writer in my VM to copy the ISO to a flash drive. Installation had a minor hitch in that the first install didn't seem to take, in that after the installer was finished and the system rebooted, nothing showed up. I booted to the USB stick again, reinstalled, and everything worked after that.

Hardware support is very much improved in this version (I've previously used 8.04 and
 9.04). I didn't have to make any configuration changes to use sound hardware, Bluetooth 
worked right away, 3D acceleration was a given as I have an Intel GPU, and after I 
installed the Broadcom STA driver through the restricted driver installer, Wifi worked as well. Sleep works as well as it did under 9.10, as having an SD card mounted when you try sleeping causes the suspend process to hang. THe fix is detailed in [this](http://www.mydellmini.com/forum/ubuntu-netbook-remix/14722-suspend-hibernate-mini-9-broken-3.html#post143677) MyDellMini forum post. Reproduced here, the fix is to add a hook to the sleep process that unmounts all memory cards. Put the following script in the `/etc/pm/sleep.d/` directory.  

``` bash
    #!/bin/bash
    
    case $1 in
    hibernate|suspend)
    umount /dev/mmcblk*
        ;;
    #    thaw|resume)
    #        ;;    
    *)  echo $1 
        ;;
    esac
    exit 0	
```

Then make it executable.

Addendum: Turned out it wasn't a bout of file system madness, it was the SSD dying.
 I sent it into Dell and got it back a week and a half later.
