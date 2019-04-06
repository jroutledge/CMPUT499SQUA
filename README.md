# CMPUT 499 Ashley and Jeffrey project of ultimate victory and being cool and stuff

## Build and Run Instructions 

* Note, project supported on Linux and MacOS with Python 2.7
1. Ensure Python2.7 and it's pip are installed, as well as Python3 and it's pip 
    > sudo apt update \
    sudo apt-get install python2.7 \
    sudo apt-get install python-pip \
    sudo apt-get install python3 \ 
    sudo apt-get install python3-pip
2. Install PyGame, Pillow, and SciPy packages 
    > pip install PyGame \
    pip install Pillow \
    pip install SciPy \
    pip3 install thesaurus==0.2.3 
3. Clone repository on local machine 
    > git clone https://github.com/jroutledge/CMPUT499SQUA.git
4. Navigate to folder 
    > cd <path to folder>/CMPUT499SQUA/setup
5. Run the setup script  
    > python3 setup.py
6. Return to main project folder
    > cd ..
7. To run the game, run:
    > python game.py [number between 1 and 8] [Synonym or Antonym]
    
    or the following for help 
    
    > python game.py --help
7.1. If the game is not working becuase of a Pillow font error, try running the following commands:
    > sudo apt-get install ttf-mscorefonts-installer \ 
    sudo fc-cache \ 
    fc-match Arial

---

## Known bugs

* There is a bug in pygame if you run pygame on a mac in python 3.7.2, use 2.7 on mac ([resource](https://www.python.org/downloads/mac-osx/)) (note: this is supposedly fixed if you're not using a homebrew installation of python 3.7.2)

* The window is of a fixed size, regardless of screen resolution, this leads some things, like fonts, to look strange.
