Title: The C Preprocessor
Date: 2012-01-16 22:31
Slug: tutorials/cpp

Here's a moderately quick primer on how the C preprocessor works. The C preprocessor
is a macro processor. It searches through its input, replacing certain sequences of
characters (tokens) with other sequences. It has a fairly small language, with most
of the primary token you'll encounter listed below.

    :::c
    #include
    #if
    #ifdef
    #ifndef
    #else
    #elif
    #endif
    #define
    #undef
    #warning
    #error

The `#ifdef` and `#ifndef` are shorthand for `#if defined` and `#if !defined` respectively.

## \#include

`#include` is replaced with the contents of the file it references. The two ways to refer
to a file are with brackets (`<>`) and with double quotes (`""`). The difference between
them is that filenames specified using brackets are first searched for in the system
directories, while those specified with quotes are first searched for in the working
directory and then in the system directories.

Now let's see what's going on. You can stop the `gcc` from going past preprocessing by giving
it the `-E` flag. Here are the two files we're going to use.

foo.c

    :::c
    int addOne(int x){
        return x + 1;
    }
bar.c

    :::c
    #include "foo.c"

    int addTwo(int y){
        return addOne(addOne(y));
    }

Because `addTwo` uses the `addOne` function, foo.c needs to include bar.c. If I run
`gcc -E` on each file, this is the result.

foo.i

    :::c
    # 1 "foo.c"
    # 1 "<built-in>"
    # 1 "<command-line>"
    # 1 "foo.c"
    int addOne(int x){
     return x + 1;
    }

bar.i

    :::c
    # 1 "bar.c"
    # 1 "<built-in>"
    # 1 "<command-line>"
    # 1 "bar.c"
    # 1 "foo.c" 1
    int addOne(int x){
     return x + 1;
    }
    # 2 "bar.c" 2

    int addTwo(int y){
     return addOne(addOne(y));
    }

Notice that the contents of foo.i are duplicated in bar.i (`.i` is the extension for
preprocessed files). This is because the preprocessor copies in the contents of foo.c
where the `#include "foo.c"` statement was. The preprocessor then contines processing the
file, which now has whatever foo.c had.

## Defining New Macros

The `#define` statement can be used to create new macros. A common example is if you have a
constant.

    :::c
    #define GRAVITY_EARTH -9.81

This creates a token named `GRAVITY_EARTH`, that will be replaced with the text `-9.81`. You
can also create macros that don't get replaced with anything, they just exist.

    :::c
    #define HAS_GRAVITY

This defines a token called `HAS_GRAVITY`. If you have this text in your code, it will be deleted.

## Include Guards

Let's look back at our example files. Say I create a new file with a new function the uses the
previous two files.

baz.c

    :::c
    #include "foo.c"
    #include "bar.c"

    int addThree(int z){
        return addOne(addTwo(z));
    }

And here's the preprocessed version.

baz.i

    :::c
    # 1 "baz.c"
    # 1 "<built-in>"
    # 1 "<command-line>"
    # 1 "baz.c"
    # 1 "foo.c" 1
    int addOne(int x){
     return x + 1;
    }
    # 2 "baz.c" 2
    # 1 "bar.c" 1
    # 1 "foo.c" 1
    int addOne(int x){
     return x + 1;
    }
    # 2 "bar.c" 2

    int addTwo(int y){
     return addOne(addOne(y));
    }
    # 3 "baz.c" 2

    int addThree(int z){
     return addOne(addTwo(z));
    }

Notice that we have the contents of foo.c in there twice. This will cause a compilation error,
as you can't have two functions called the same thing. To get around this issue, a thing called
include guards are used. Let's look at new versions of our example files.

foo-new.c

    :::c
    #ifndef INCLUDE_FOO_C
    #define INCLUDE_FOO_C
    int addOne(int x){
        return x + 1;
    }
    #endif /* INCLUDE_FOO_C */
bar-new.c

    :::c
    #ifndef INCLUDE_BAR_C
    #define INCLUDE_BAR_C
    #include "foo-new.c"

    int addTwo(int y){
        return addOne(addOne(y));
    }
    #endif /* INCLUDE_BAR_C */

baz-new.c

    :::c
    #ifndef INCLUDE_BAZ_C
    #define INCLUDE_BAZ_C
    #include "foo-new.c"
    #include "bar-new.c"

    int addThree(int z){
        return addOne(addTwo(z));
    }
    #endif /* INCLUDE_BAZ_C */

Now the preprocessed output of baz.c is 

    :::c
    # 1 "baz-new.c"
    # 1 "<built-in>"
    # 1 "<command-line>"
    # 1 "baz-new.c"


    # 1 "foo-new.c" 1


    int addOne(int x){
     return x + 1;
    }
    # 4 "baz-new.c" 2
    # 1 "bar-new.c" 1




    int addTwo(int y){
     return addOne(addOne(y));
    }
    # 5 "baz-new.c" 2

    int addThree(int z){
     return addOne(addTwo(z));
    }

What's happening here is called conditional compilation. In C, you can conditionally
do thing with `if` statements. You can do the same thing with the C preprocessor. The
new lines in the source files basically say "If INCLUDE\_SOMETHING\_C is _not_ defined,
keep going, if it _is_ defined, skip to the `#endif` token and continue on from there."
Inside the conditional (the "keep going" part of the sentence above), we define
INCLUDE\_SOMETHING\_C. By doing this, we ensure that the body of the conditional with
all of our code is included only once.

