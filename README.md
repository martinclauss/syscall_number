# syscall_number

## Description

With this little script you can search for Intel x86 Linux system call names and get the system call number as a result. There are websites like https://filippo.io/linux-syscall-table/ or https://www.informatik.htw-dresden.de/~beck/ASM/syscall_list.html but who want's to google all the time whe he/she can have a command-line tool that works for 32bit **and** 64bit!

## Requirements

### gcc with 32bit support

Debian/Ubuntu:
```
sudo apt-get install gcc gcc-multilib
```

Fedora:
```
sudo dnf install gcc glibc-devel.i686
```

## Installation

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

## Uninstallation

```
pip3 uninstall syscall_number
```

remove the global installation

```
sudo pip uninstall syscall_number
```

## Usage

```
# the first time the command takes a bit longer since it builds a cache for all system calls
syscall_number -s read -b 32

# this should run a lot faster
syscall_number -s write -b 64

# this lists all 32bit system calls
syscall_number -a -b 32

# and this lists all 64bit system calls
syscall_number -a -b 64

# if you just want the system call number without any additional text use this
syscall_number -s connect -b 32 -q

# or in a more complex scenario with pwntools' asm script (http://docs.pwntools.com/en/stable/asm.html)
echo "mov eax, $(syscall_number -s exit -b 32 -q); mov ebx, 42; int 0x80" | asm
```

## Contribution

Pull Requests are welcome! :)

## Thanks

[@tbehner](https://github.com/tbehner)