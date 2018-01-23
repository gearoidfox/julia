# julia

Plot filled [Julia sets](https://en.wikipedia.org/wiki/Julia_set).

### Usage:

    python julia.py Z

Where Z is a complex number in the form x+yJ. For example,

    python julia.py .44+.21J

If the real part x is negative, quote the argument with a leading space so it isn't interpreted as an option, or precede the argument with '--'. For example,

    python julia.py ' -0.5+.75J'
    python julia.py -- -0.5+.75J
    

### Examples:

`python julia.py 0+1J`
![Example image](example2.png?raw=true)

`python julia.py ' -0.4+0.6J' -i 300 --offset 0.67 -r 2000 --colour  --smooth`
![Example image](example1.png?raw=true)
