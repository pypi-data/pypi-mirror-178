# dc-logging

This is a tiny library to quickly and easily set up loggers in many projects.

Isn't it easy and simple enough already just to use the `logging` built-in?  
Well, yes and no.

It's quite simple to use indeed but I have a number of predefined defaults that
I always like to use and it makes no sense for me to repeat those in several
different projects. Instead, this library always assumes those defaults and I 
can still customize by passing different configurations when getting a logger or
by using the methods of the built-in `logging` library after getting a logger.

The usage is quite evident from reading the code, and small enough so to prevent
me from wanting to duplicate that here (for now).
