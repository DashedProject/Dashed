# Build
To build the ISO and all things, use or the automatic way, or choose to use the hard way by doing everything by hand.

## Automatic
This way is **NOT** available yet. (sorry for the hype up there...)

## Manual
### Preparing
Make sure to remove all the *\_\_pycache__* directories from the installer folder. Also check the sub-folders (*backend* *frontend*).<br>
Copy the installer folder into *./iso/profile/airootfs/opt/dashed/*, so it becomes in the folder *./iso/profile/airootfs/opt/dashed/installer*.

### Creating ISO
In the *iso* folder, run the command `./build.sh`.

### Running ISO
Two ways to run, to test it out use the `./run.sh` command. Or you could put it on a USB-stick and put it in the wished server.