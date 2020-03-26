# automated-job-manager-2
an python automated job manager that uses Advance Python Scheduler and builds as a .exe

# Advanced Python Scheduler documentation

### Setup for Debugging and Development

1. In a VSCode terminal (within the root of the project folder), create the virtual environment:

   ```
   python -m venv env  (windows)

   python3 -m venv env  (mac / linux)
   ```

2. Activate the virtual environment. Your command prompt should now be prefixed with (env):

   ```
   .\env\Scripts\activate.bat  (windows)

   source env/bin/activate  (mac / linux)
   ```
3. Install Python requirements:

   ```
   pip install -r requirements.txt   (windows)

   pip3 install -r requirements.txt   (mac / linux)

### Build the executable ###
a simple command (only tested on windows)
```
    pyinstaller -w -F main.py --console
``` 
creates a folder called dist. look insde to find the .exe

### Usage ###
1. /IMMEDIATE/: When running this program will process applicable files in this folder immediately
2. /QUEUE/: When running this program will process files in this folder on a regular schedule