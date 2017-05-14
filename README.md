# raspi-voice-actions
Separate added actions from default aiyprojects-raspbian repo code.  

## Fun actions for AIY Projects
Actions for https://github.com/google/aiyprojects-raspbian/blob/master/src/action.py

## Create the symlink
After cloning the repo, setup a symlink to ~/voice-recognizer-raspi/src/action.py
```bash
# Backup current action.py
cp ~/voice-recognizer-raspi/src/action.py ~/voice-recognizer-raspi/src/action-backup.py

# Remove current action.py
rm ~/voice-recognizer-raspi/src/action.py

# Create the symlink
sudo ln -s ~/raspi-voice-actions/action.py action.py
```
## Adding actions
- Add your module into the actions directory
- Import your module at the top of actions.py
```bash
from play import *
```

### Raspberry Pi AIY Projects forum
All of these actions were contributed by members of the Raspberry Pi forums.  
To get more ideas for fun actions visit: https://www.raspberrypi.org/forums/viewforum.php?f=114
