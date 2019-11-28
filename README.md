# The Hamstrometer
This repository contains the code and circuit schematics for [the Hamstrometer](https://tinwhiskers.net/post/hamstrometer), a
Raspberry Pi Powered Hamster Pedometer.

# Press
This project was featured in 
- [Raspberry Pi Geek Magazine](https://tinwhiskers.net/post/hamster_mag) 
- [OpenSource.com](https://opensource.com/life/15/10/tracking-hamster-activity-raspberry-pi)
- [HackaDay](https://hackaday.com/2015/11/02/tracking-the-hamster-marathon/)

# Backstory
[The Internet](https://en.wikipedia.org/wiki/Roborovski_hamster) claims that Roborovski hamsters (the breed I own)
run "an equivalent of four human marathons each night on average".

This repo is part of a silly scientific project to determine if my two pet hamsters -- Hamtaro and Hamtaro Grande -- can hold their own
against this claim. 

# Attribution
## License
This project is licensed under the [GNU General Public License (GPLv3)](https://www.gnu.org/licenses/quick-guide-gplv3.html):

> Developers who write software can release it under the terms of the GNU GPL. When they do, it will be free software and stay free software, no matter who changes or distributes the program. We call this copyleft: the software is copyrighted, but instead of using those rights to restrict users like proprietary software does, we use them to ensure that every user has freedom.

## Shout Outs and Citations
I appreciate citations and shout outs and recommend following [MIT's Code Citation Standards](http://integrity.mit.edu/handbook/writing-code). Please attribute code to Alex Leonhart, [www.tinwhiskers.net](https://www.tinwhiskers.net), when possible. 

That being said, one of the many joys of releasing open source code is seeing others use it in their own work.  
If you use my code in your project, I'd love to hear about it! Please email me at alexleonhartcode@gmail.com and show me what you made!  

Thank you to icon-library.net for <a href="https://icon-library.net/icon/anonymous-tumblr-icon-17.html" rel="noopener">Anonymous Tumblr Icon #390821</a>!  

## Questions
I try my best to respond to all emails I get about my work and how to use it. If you're struggling with using something 
in your own project, send me an email to alexleonhartcode@gmail.com and I'll try to help you out.  

### Students
I frequently receive emails about this project from engineering students who are trying to learn how to make similar projects, 
and from science students who are hoping to use a similar design to gather data for their work. I love hearing from 
students and will try to help you if I can, but I have to be realistic about my schedule. Please give ample time before 
your deadline.

# How to Build Your Own
I recommend reading [the full blog post](https://tinwhiskers.net/post/hamstrometer) to understand the physical project setup. 

## The [Fritzing](https://fritzing.org/) Files
The "fritzing" folder contains several different views for the circuit setup. Pick the one that works the best for you. If 
you are new to building circuits, I suggest you try hamster_board_3.png, because it is the simplest setup.
- hamster_board_1.png (Advanced) is a traditional circuit board layout, useful if you plan to have a real circuit board printed
- hamster_board_2.png (Intermediate) is a breadboard layout for use with a ribbon cable
- hamster_board_3.png (Simplest) is a breadboard layout for use with individual wires

## The Python Files
The code that runs the Hamstrometer is not flashy or fancy at all. It is just a few scripts that work together to 
collect and process the data.

### collect_data.py
This script is meant to be left running continuously. This script is what records your hamster data as they get on and 
off of the wheel. It should be left running whenever you want to track activity.  

Activity from this script will be written to data/1_data_live as it is processing a sprint.  
Activity from this script will be written to data/2_data_ready once the sprint is over.

### send_data_to_thingspeak.py
This step is optional. It's only needed if you'd like to send your data somewhere. This script is meant to run asynchronously on a set interval. I recommend setting it to run once every few hours in a cron.  

This script will read the data in the files in data/2_data_ready and will send them to ThingSpeak. Once the data from the file is sent successfully, the file will be moved to data/2_data_processed.