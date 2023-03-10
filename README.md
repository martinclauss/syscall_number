# syscall_number

## Description

With this little script you can search for Intel x86 Linux system call names and get the system call number as a result. There are websites like https://filippo.io/linux-syscall-table/ or https://www.informatik.htw-dresden.de/~beck/ASM/syscall_list.html but who wants to google all the time when he/she can have a command-line tool that works for 32bit **and** 64bit!

## Requirements

### gcc with 32bit support

Ubuntu:
```
sudo apt-get install gcc gcc-multilib
```

Fedora:
```
sudo dnf install gcc glibc-devel.i686
```

## Installation

Requires Python version >= 3.6! (check with `python3 --version`)

```
pip3 install --user git+https://github.com/martinclauss/syscall_number.git
```

for a system-wide installation
```
sudo pip3 install git+https://github.com/martinclauss/syscall_number.git
```

Now you can run the command without the `.py` extension from everywhere:
```
syscall_number --help
```

## Updates

You won't get new features / bug fixes automatically but you can easily update:

```
pip3 install --user --upgrade git+https://github.com/martinclauss/syscall_number.git
```

or

```
sudo pip3 install --upgrade git+https://github.com/martinclauss/syscall_number.git
```

## Uninstallation

```
pip3 uninstall syscall_number
```

remove the global installation

```
sudo pip3 uninstall syscall_number
```

## Usage

```shell
# the first time the command takes a bit longer since it builds a cache for all system calls
# query the system call (-s) read for 32bit (-b 32):
syscall_number -s read -b 32

# this should run a lot faster
# query the system call (-s) write for 64bit (-b 64):
syscall_number -s write -b 64

# reverse lookup is also possible with decimal and hexadecimal numbers
syscall_number -n 11 -b 32
syscall_number -n 0xb -b 32 

# this lists all (-a) 32bit (-b 32) system calls:
syscall_number -a -b 32

# and this lists all (-a) 64bit (-b 64) system calls:
syscall_number -a -b 64

# reverse search is also possible with grep:
syscall_number -a -b 32 | grep read

# if you just want the system call number without any additional text use -q:
syscall_number -s connect -b 32 -q

# or in a more complex scenario with pwntools' asm script (http://docs.pwntools.com/en/stable/asm.html)
echo "mov eax, $(syscall_number -s exit -b 32 -q); mov ebx, 42; int 0x80" | asm

# additionally show an excerpt of the man page for the system call with -m:
syscall_number -s read -b 32 -m


```


## Alternatives

[pwntools](http://docs.pwntools.com/en/stable/) also provides a similar but more complex method with the `syscall()` function: [32bit](http://docs.pwntools.com/en/stable/shellcraft/i386.html#pwnlib.shellcraft.i386.linux.syscall) and [64bit](http://docs.pwntools.com/en/stable/shellcraft/amd64.html#pwnlib.shellcraft.amd64.linux.syscall).

## Contribution

Pull Requests are welcome! :)

## Thanks

[@tbehner](https://github.com/tbehner)
