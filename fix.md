Run the following command to install chrome executable(for plotly):
```bash
choreo_get_chrome
```
or
```bash
plotly_get_chrome
```

If chrome-related issues still show up, install dependencies:
```bash
sudo apt-get install -y libnss3 libxss1 libasound2 libatk1.0-0 libgtk-3-0 libffi7
```

If sudo access is not available, install manually:
## Fixing `ffi_type_pointer` Error in Chrome via Manual `libffi.so.7` Build

Error: symbol lookup error: libp11-kit.so.0: undefined symbol: ffi_type_pointer, version LIBFFI_BASE_7.0
This occurs when your system lacks a compatible `libffi.so.7` and you cannot install it using `apt` or other system package managers.

### 1. Download and Extract `libffi` Source
```bash
mkdir -p ~/libffi7
cd ~/libffi7
wget https://mirrorservice.org/sites/sourceware.org/pub/libffi/libffi-3.3.tar.gz
tar -xvzf libffi-3.3.tar.gz
cd libffi-3.3
```

### 2. Build libffi Locally (No sudo required)
```bash
./configure --prefix=$HOME/libffi7/install
make -j4
make install
```
This installs the shared library to: ~/libffi7/install/lib/libffi.so.7

### 3. Run Your Python Script Using LD_PRELOAD
Preload the correct libffi version to avoid symbol errors:
```bash
LD_PRELOAD=$HOME/libffi7/install/lib/libffi.so.7 python your_script.py
```

This workaround avoids the need for root access and allows Choreographer (or other Chrome-based tools) to function without crashing due to incompatible libffi versions.
