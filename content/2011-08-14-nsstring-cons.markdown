---
layout: post
title: "NSString Cons"
date: 2011-08-14 06:54
comments: true
categories: code
---

One of the fundamental operators in functional languages is 'cons'. It concatenates lists
of things together, and since strings are usually treated as lists of characters, cons gets
a lot of use in string processing as well. One of the cool tricks I saw done with
Objective-C a while ago was implementing cons on NSString, using `:` like Haskell and ML
do. I have been unable to find the original site, so I decided to reimplement it
myself recently.

<!--more-->

A quick caveat to the following: this uses Objective-C trickery that may not be very safe
in a production environment. Also, the upcoming Automatic Reference Counting in Clang/LLVM 3.0
will not compile this code. With that out of the way, lets look at how we're going to do this.
In Objective-C, methods are backed by a
concrete implementation in the form of a standard C function. The runtime uses the
[`IMP`](http://developer.apple.com/library/mac/documentation/Cocoa/Reference/ObjCRuntimeRef/Reference/reference.html#//apple_ref/doc/uid/TP40001418-CH3g-BAJFGBJF)
type for this, which is defined as

``` objectivec
    id (*IMP)(id self, SEL selector, ...)
```

The `...` in this case stands for additional arguments for the method.
For example, `[@"foo" stringByAppendingString:@"bar"]` will eventually be executed by a 
function matching the prototype below.

``` objectivec
    id functionName(id self, SEL sel, NSString *otherString)
```

Additional arguments are just tacked onto the end. This can be combined with standard C
varargs. The only caveat is we need to signal the end of the varargs somehow. I used `nil`.

``` objectivec
    id stringCons(id self, SEL selector, ...){
    	va_list strings;
    	NSMutableString *fullString = [[NSMutableString alloc] initWithString:self];
    	va_start(strings, selector);
    	id currentString = nil;
    	// End on nil
    	while((currentString = va_arg(strings, id))){
    		[fullString appendString:currentString];
    	}
    	va_end(strings);
    	return fullString;
    }
```

There are two approaches to adding a method to a class at runtime in Objective-C. The 
normal way is to use
[`class_addMethod`](http://developer.apple.com/library/mac/documentation/Cocoa/Reference/ObjCRuntimeRef/Reference/reference.html#//apple_ref/c/func/class_addMethod). This is enough in most cases, but because we have a variable length selector, we can't use this method. Another
way methods can be added is with the dynamic method resolution available through NSObject
(Mike Ash touches on this method in a post on [message forwarding](http://mikeash.com/pyblog/friday-qa-2009-03-27-objective-c-message-forwarding.html)\).

``` objectivec
    +(BOOL)resolveInstanceMethod:(SEL)sel{
    	// Check that the selector is just ':' characters
    	const char *checkName = sel_getName(sel);
    	BOOL isCons = YES;
    	int i = 0;
    	char c = checkName[i];
    	while(c != '\0'){
    		if(c != ':'){
    			isCons = NO;
    			break;
    		}
    		c = checkName[++i];
    	}
    	// Add the method, or pass this message up the chain
    	if(isCons){
    		// Make the type string
    		size_t typesSize = 4 + i;
    		char *types = malloc(sizeof(char) * typesSize);
    		types[0] = '@';
    		types[1] = '@';
    		types[2] = ':';
    		for(int j = 3; j < typesSize - 1; ++j){
    			types[j] = '@';
    		}
    		types[typesSize - 1] = '\0';
    		// Add the method
    		class_addMethod([self class], sel, stringCons, types);
    		return YES;
    	}else{
    		return [super resolveInstanceMethod:sel];
    	}
    }
```

Here all were doing is checking to see if the selector is completely made up of ':' characters.
If it is, we add the `stringCons` IMP from above for that selector. Note the else block at
the end. The call to `[super resolveInstanceMethod:sel]` is very important, as other parts of
a class may depend on this dynamic method resolution.

The final hurdle is how to add `+resolveInstanceMethod:` to NSString. The safest way would be
to subclass NSString, but since NSString is a class cluster this is not possible. I ended up
using a category, but a safer choice might be to use method swizzling to insert our method
in addition to any NSString may have defined.

That's it to adding a cons-like operator to NSString in Objective-C. To use it, just insert
it between instances of NSString ending with `nil`, like below.

``` objectivec
    NSString *one = @"1";
    NSString *two = @"2";
    NSString *three = @"3";
    NSString *all = [one:two:three:nil];
```
