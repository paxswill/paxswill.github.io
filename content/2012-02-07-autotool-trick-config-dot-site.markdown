---
layout: post
title: "Autotools Trick: config.site"
date: 2012-02-07 16:01
comments: true
categories: autoconf
---
This is a quick trick for those who have to continually set up common settings
when using Autotools style `configure` scripts. One of the initial steps a
configure script does is to look for a `$prefix/share/config.site`
file and then to execute its contents. An example of how this may be useful is
if you have some common libraries that are not on the default search paths for
your compiler and you want `CFLAGS` and `LDFLAGS` set automatically. In my case
I commonly use the Nvidia OpenCL headers, which on the machines I use are
installed to `/usr/local/cuda/include`. To use them, I could have a config.log
file like so in my default installation prefix.

``` bash
CPPFLAGS="${CPPFLAGS} -I/usr/local/cuda/include"
```

Now when I run `configure`, it picks up that additional flag for the C 
preprocessor.

A more complicated example is if you maintain a seperate prefix. I do this in
my home folder for my CS department account. Because my home folder is shared
over NFS to all of the department's machines, and many of them have different
architectures and operating environments, I keep a prefix for different classes
of machines. For example:

    ~/local/
	        fast-sparc/
	        fast-ubuntu/
	        nv-s1070/
	        nv-c870/
	        src/

The `src` directory is just a repository for all of the source packages that I 
end up installing in the other directories. In my `.bashrc` I export a
variable, `LOCAL_PREFIX`, that is set to the prefix for the machine I'm logging
into. Then, all I need to do is `./configure --prefix=$LOCAL_PREFIX` and the
compiler flags are properly set for that prefix. Another possibility is to
export the `CONFIG_SITE` variable set to the path to the config.site file for
that machine configuration.

More details about config.site can be found in the [Autoconf manual][autoconf-site].

[autoconf-site]:http://www.gnu.org/savannah-checkouts/gnu/autoconf/manual/autoconf-2.68/html_node/Site-Defaults.html#Site-Defaults
