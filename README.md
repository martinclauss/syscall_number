# syscal_number.py

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
git clone https://github.com/martinclauss/syscall_number.git
cd syscall_number
pip3 install --user -r requirements.txt
```

for a system-wide installation (still inside the cloned directory)
```
sudo ln -s $(pwd)/syscall_number.py /usr/local/bin/syscall_number
```

Now you can run the command without the `.py` extension from everywhere:
```
syscall_number --help
```

## Uninstallation

here `syscall_number` is the cloned directory
```
rm -rf syscall_number
```

remove the global installation link

```
sudo rm /usr/local/bin/syscall_number
```

## Usage

```
chmod +x syscall_number.py
./syscall_number.py --help

# the first time the command takes a bit longer since it builds a cache for all system calls
./syscall_number.py -s read -b 32

# this should run a lot faster
./syscall_number.py -s write -b 64

# this lists all 32bit system calls
./syscall_number.py -a -b 32

# and this lists all 64bit system calls
./syscall_number.py -a -b 64

# if you just want the system call number without any additional text use this
./syscall_number.py -s connect -b 32 -q

# or in a more complex scenario with pwntools' asm script (http://docs.pwntools.com/en/stable/asm.html)
echo "mov eax, $(./syscall_number.py -s exit -b 32 -q); mov ebx, 42; int 0x80" | asm
```

## Contribution

Pull Requests are welcome! :)

## TODOs

- make this a Python package with a setup.py