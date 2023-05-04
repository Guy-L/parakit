# thgym - Superplayer Gym environment for Touhou
(that's not actually why the repo's named that lesanae)

Simple python tool to extract game state data: player coords and state, resources, list of on-screen enemies, bullets and items
\nMeant to help parakeets analyze their games; should be easy to build various analysis tools on top of this (feel free to fork)
\nFor instance: over the next 5 seconds, when/where will the biggest bullet cluster in a certain radius be?

Doesn't yet work with every game and will definitely need some changes to maximize accuracy/usability
\nIf you have feature requests or need help making your own tool let me know

Supported games:
* DDC

Goals:
* Multi-game support (refactoring)
* UM support
* Extracting more useful things
* Visualization methods (storing screenshots, drawing shapes, etc)

## Setup 
(using a venv to minimize python headaches)
\n(you might be prompted to install virtualenv if you haven't, it'll tell you how)

Windows:
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Linux/Mac:
```bash
python -m venv venv
source venv_name/bin/activate
pip install -r requirements.txt
```

If you need to exit the venv for whatever reason (script will no longer work), type `deactivate`.

## Running

To get the state once:
```bash
python state-reader.py
```

To get the states over 500 in-game frames (# must be integer):
```bash
python state-reader.py 500f
```

To get the states over 10.5 in-game seconds (# can be decimal):
```bash
python state-reader.py 10.5s
```

Depending on how fast your machine is and how much stuff is on screen, extracting the game state can take longer than a frame (1/60ths of a second), and as a result, the extracted frames **will not be contiguous and some frames will have been skipped**. For instance, if I run `python state-reader.py 100f`, we'll go from frame #2901 to #3049 after extracting 100 frames (a difference of 148): 48 frames that happened during the extraction were skipped. 

To **prevent this**, add the argument `exact` to your command, i.e.: `python state-reader.py 100f exact`. This will slow the game down to ensure extraction always finishes in time for the next frame (and as a side-effect, it'll help you be more precise if you plan to play while this is going on).

Either way, extraction will most likely take longer than the actual time specified (especially for longer periods).

## Screenshots

Single state extraction:

![single state extraction](https://i.imgur.com/mKAfFJ0.png)

Analysis over 50 frames (`exact`):

![analysis over 50 frames](https://i.imgur.com/voSiS0I.png)