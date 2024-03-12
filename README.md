# Clash-Royale Cycle Counter

This project is a Python application that processes live Clash Royale game footage to keep track of, and display both players cycle. It's a hobby project and a proof of concept I've wanted to make for a little while just to learn a bit about opencv. I'm not sure how much use it is or whether or not Supercell would take kindly to people actually using it while playing (although it doesn't reveal any info the player doesn't already have of course...).

## Project Structure


- `debug/`: Contains various scripts for debugging and testing - most of these I used for building it and probably don't need to be used if you're just going to run the main script, but I figured I'd include them in case anybody has issues with getting it to work on their machine (sorry for the unhelpful names).
- `handlogic.py`: Contains the logic for handling game hands.
- `locations/`: Contains JSON files with coordinates for various game elements.
- `main.py`: The main script that runs the application.
- `templates/`: Contains screenshots of card images as they show up in the game client.
- `utils/`: Contains utility scripts for loading templates, initializing functions, and printing.

## Main Features

The `main.py` script processes video game footage and tracks game data. It is currently set to display three windows, 1 with the game footage, 1 with the red players deck, and 1 with the blue players. It uses template matching to figure out when a card has been played and keeps track of the cards that have been played for each player in order to keep track of their cycle.

## Usage

To run the main script, make sure you have pyopencv (if not run ```pip install pyopencv ```). After that, simply run the main script: ```python main.py``` and it will ask you for the path to the video file. 

## TODO

Unfortunately right now it doesn't work with live game footage... It should be relatively easy to redirect opencv to a live feed instead of a video file, but I haven't tried, as this was really just done as a proof of concept. 

Right now, when the blue player emotes - the emotes cover some of their cards and mess with my system for determining when a card was played (as the template which was matched a frame ago is no longer matched). Right now I have a very hacky solution in place that basically kinda seems to work (although not all the time), but I'd like to add something much more ressilient. 

Actual command line options (ie for debugging, pointing to the video, etc...)

### Notes

Hopefully it goes without saying that you'd have a hard time actually running this on a phone, and you'll need a pc/laptop. Either you should use google play games (untested) on a pc or what I did during development which was screen record my iphone on my mac with quicktime player.