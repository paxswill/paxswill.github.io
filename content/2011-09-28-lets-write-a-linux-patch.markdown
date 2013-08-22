---
layout: post
title: "Let's Write a Linux Patch"
date: 2011-09-30
comments: true
categories: code linux
published: false
---

Due to an unfortunate accident involving a glass of water and my main
laptop, I've been using my netbook running Debian Sid. To make working
with code easier, I purchased an Apple Wireless Keyboard, but I was
suprised to find it wasn't completely supported. Namely the 'Fn' key
didn't register, meaning I couldn't use the multmedia keys or use the
simulated Page Up/Down, Home and End keys.
<!-- more -->
## Writing the patch

Most solutions to this problem are from 2008 for Linux kernel 2.6.25.
Shortly after these bugs were filed, the kernel added special handing
for these keyboards. But this is 2011 and I'm using the 3.0 release of
the kernel. There's a crucial hint in most of the older patches though.
For example, here's a patch for kernel 2.6.25.

{% codeblock 2.6.25 Patch lang:diff http://chezphil.org/apple-alu-bluetooth-kb-linux/ Source %}
--- linux-2.6.25/net/bluetooth/hidp/core.c      2008-04-17 03:49:44.000000000 +0100
+++ /usr/local/src/linux-2.6.25/net/bluetooth/hidp/core.c       2008-05-25 13:26:32.000000000 +0100
@@ -678,6 +678,8 @@
 } hidp_blacklist[] = {
        /* Apple wireless Mighty Mouse */
        { 0x05ac, 0x030c, HID_QUIRK_MIGHTYMOUSE | HID_QUIRK_INVERT_HWHEEL },
+        /* Apple Bluetooth alu ISO keyboard */
+        { 0x05ac, 0x022d, HID_QUIRK_APPLE_HAS_FN | HID_QUIRK_APPLE_ISO_KEYBOARD },
 
        { }     /* Terminating entry */
 };
{% endcodeblock %}

The `0x05ac` is Apple's vendor ID, while `0x022d` is the product ID of
the keyboard he has. A quick check confirmed that my keyboard has the
product ID `0x0255`.

To add support for this keyboard we need to look for where quirks mode
is enabled for various devices. Between now and 2008 the method for
defining quirks was rewritten to be more developer friendly. The three
files we need to modify are `drivers/hid/hid-core.c`,
`drivers/hid/hid-apple.c` and `drivers/hid/hid-ids.c`

`hid-ids.c` is the easiest. We just need to define a constant for this
keyboard's product ID. Because there were another set of variants in
2009, I just modified the form to use 2011.

{% include_code 2011-09-28/hid-ids.diff %}

I only have the ANSI version of the keyboard, but as European and
Japanese users start using them they can add the correct product IDs.

Next we modify `hid-core.c` to tell it to use quirks with devices
matching Apple's vendor ID and the new product ID.

{% include_code 2011-09-28/hid-core.diff %}

And finally we modify `hid-apple.c` to use the specific quirks for this
keyboard.

{% include_code 2011-09-28/hid-apple.diff %}

## Testing the patch

To test the patch, you will need to be able to build your modified kernel.
Debian makes it pretty easy, but if you're using another distribution it
will be different. Install `kernel-package` through apt, and then run

```
# make-kpkg -initrd kernel_image
```

in the root of the kernel source tree. Currently there is a bug with
`kernel-package`, but the bug can be fixed by applying this patch.

{% codeblock kernel-package Patch lang:diff http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=638012#21 Source %}
--- ruleset/targets/common.mk-orig	2011-08-17 18:24:16.048922011 +0300
+++ ruleset/targets/common.mk	2011-08-17 20:08:26.623916939 +0300
@@ -323,8 +323,13 @@ ifeq ($(DEB_HOST_ARCH_OS), linux)
     endif
   endif
   ifneq ($(strip $(shell grep -E ^[^\#]*CONFIG_LGUEST $(CONFIG_FILE))),)
+	if [ -e Documentation/lguest ]; then \
 	$(MAKE) $(do_parallel) $(EXTRAV_ARG) $(FLAV_ARG) ARCH=$(KERNEL_ARCH) \
-			    $(CROSS_ARG) -C Documentation/lguest
+			    $(CROSS_ARG) -C Documentation/lguest; \
+	elif [ -e Documentation/virtual/lguest ]; then \
+	$(MAKE) $(do_parallel) $(EXTRAV_ARG) $(FLAV_ARG) ARCH=$(KERNEL_ARCH) \
+			    $(CROSS_ARG) -C Documentation/virtual/lguest; \
+	fi
   endif
 else
   ifeq ($(DEB_HOST_ARCH_OS), kfreebsd)
{% endcodeblock %}

To apply the patch, save it somewhere, move to `/usr/share/kernel-package` and
run this command:

```
# patch -p0 < /path/to/the/patch.patch
```

Building the kernel can take a while, but requires some interaction when
done this way. Once the the kernel image is built, you can install it
with

```
# dpkg -i ../linux-image-3.1.0-rc8+_3.1.0-rc8+-10.00.Custom_i386.deb
```

Reboot and verify that your patch works. In this case it does, and all
the special keys were sending the proper key codes (verified with `xev`).

## Submitting the patch

It's a good idea to read the `Documentation/SubmittingPatches` document,
as it covers the basics of submitting patches and the style expected in
your correspondence. If (like me), you use git during your development,
you can use it to create your patches.

```
$ git format-patch -<N> -s --subject-prefix='PATCH'
```

If you run that in your Linux tree, and replace <N> with the number of
commits your patchset comprises, you will get a bunch of files ready to
mail off. Well, almost. `git format-patch` creates files that are ready
to be sent out with standard CLI email utilities. If you're using
another email client, you can copy-paste the information into the
appropriate fields. The `-s` adds a "Signed-off-by" line. This is used
by the Linux kernel to verify that each line of code is legally allowed
to be released under the GPL.

Now that you have the content of your email, you should choose where to
send it. As the `SubmittingPatches` document says, you should read
through the `MAINTAINERS` list to find the person in charge of the area
you've changed. In my case it was Dmitry Torokhov, as he is the
maintainer for input drivers. You also should CC a couple of other
entities. Because this is a change to the input subsection, the
linux-input list should be CC'd. I did not CC linux-kernel as most of
the examples on the
[list archives](http://www.spinics.net/lists/linux-input/) were not
including it. Before you send your email to any list, make sure to
subscribe to it, or the email will not be received properly.

