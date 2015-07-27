# Installation
1. If you are using a Debian-based OS, run `sudo apt-get install python-dev libmysqlclient-dev`
2. Create a virtualenv, I use virtualwrapper. So `mkvirtualenv osqaconverter`
3. Run `pip install -r requirements.txt`


# Requirements

1. An OSQA database
2. A working internet connection to convert markdown to mediawiki

# Usage

1. Fill in your OSQA DB details in run.py
2. Run `python run.py` this should take quite a while
3. Check export/ folder for results, you should have a number of .tid files
4. Move all .tid files to the tiddlywiki tiddlers/ folder
5. Shutdown and restart tiddlywiki
