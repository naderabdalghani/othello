<br />
<p align="center">
  <a href="https://github.com/naderabdalghani/othello">
    <img src="assets/icon.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Othello</h3>

  <p align="center">
    A basic Othello (Reversi) implementation that is playable by both humans and general minimax alpha-beta pruning agents.
  </p>
</p>

## Table of Contents

* [About the Project](#about-the-project)
  * [Starting Window](#starting-window)
  * [Settings Window](#settings-window)
  * [Agent](#agent)
  * [Board](#board)
  * [Move](#move)
  * [Othello](#othello)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Executable] (#executable)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
  * [Running](#running)
* [Acknowledgements](#acknowledgements)

## About The Project

Agents' configuration parameters (hints, search depth, etc.) and moves are read by and applied to a graphical user interface (GUI) implemented using `tkinter`.

### Starting Window

![Starting Window][starting-window]

### Settings Window

![Settings Window][settings-window]

### Agent

[agent.py](agent.py) contains the implementation of a general agent that can solve any 2-player zero-sum perfect information game with the following interface using minimax algorithm with alpha-beta pruning:

```python
class Game:
    def __init__(self, n):
        self.n  # dimension of the game board
        self.state  # current state of the board and its pieces as a 2D matrix
        self.black_score
        self.white_score
        self.last_move  # last move applied to the game

    def move_generator(self, player):
        """
        Parameters
        ----------
        player : int
            The integer code of a player
        
        Returns
        ----------
        moves : list(Moves)
            A list of possible moves available to 'player' at the current state
        """

    def apply_move(self, player, move):
        """
        Parameters
        ----------
        player : int
            The integer code of a player
        move : Move
            Move to be applied to the current state
        """

    def status(self):
        '''
        Returns
        ----------
        game_status : int
            An integer code to the current status of the game.
            Could be on of the following:
                GAME_IN_PROGRESS = 0
                DRAW = 1
                BLACK_WON = 2
                WHITE_WON = 3
        '''
    def simple_evaluation_fn(self):
        '''
        Computes a value for the current state of the game using a simple 
        heuristic function, then stores it in the last_move value field.
        '''

    def advanced_evaluation_fn(self, player):
        '''
        Parameters
        ----------
        player : int
            The integer code of a player

        Computes a value for the current state of the game using a more 
        advanced heuristic function, then stores it in the last_move value field.
        '''
```

### Board

![Game Window][game-window]

Inherits `tkinter.Frame` object. This [module](board.py) initializes the agents and renders a valid Othello board given the right arguments. It also serves as a wrapper for the Othello game instance and the agents, as it controls the game flow and reflects changes done to the Othello object by either of the two agents through the graphical user interface.

### Move

Instances of [Move](move.py) represents a move with coordinates `x` and `y` and a `value` field which is used in the process of state evaluation.

### Othello

The [Othello](othello.py) class implements the game of Othello (Reversi) in accordance with its rules using the interface mentioned in the [Agent](#agent) section.

### Built With

* [Python 3.9](https://www.python.org/downloads/release/python-390/)
* [PyCharm](https://www.jetbrains.com/pycharm/)
* [TkInter](https://docs.python.org/3/library/tkinter.html)
* [NumPy](https://numpy.org/)
* [Pillow](https://pillow.readthedocs.io/en/stable/)
* [PyInstaller](https://www.pyinstaller.org/)

## Getting Started

### Executable

You can find the executable in the [Releases](https://github.com/naderabdalghani/othello/releases) section of this repository.

Download and extract `Othello.rar` and launch the game by double-clicking on `Othello.exe`.

**Note:** Usually `PyInstaller` executables are flagged by antiviruses, so make sure you exclude the directory where you are planning on extracting the `.rar` file content into or temporarily turn off your antivirus protection if you are just trying.

### Prerequisites

* Setup Python using this [link](https://realpython.com/installing-python/)

### Installation

1. Create a virtual environment
	`cd <project-directory>`
	- On Unix-based OS's:
	`$ python3 -m venv venv`
	- On Windows:
	`> py -3 -m venv venv`

2. Activate the environment
	- On Unix-based OS's:
	`$ . venv/bin/activate`
	- On Windows:
	`> venv\Scripts\activate`

3. Install app dependencies
	`pip install -r requirements.txt`

### Running

* Make sure you are in the project directory
	`cd <project-directory>`
	- On Unix-based OS's:
  `$ python main.py`
	- On Windows:
	`> py main.py`

## Acknowledgements

* [Initial board boilerplate](https://stackoverflow.com/a/4959995/9476692)
* [WinOthello – A C# implementation of Reversi](https://reflectivecode.com/tag/reversi/)
* [Wikipedia – Computer Othello Evaluation Techniques](https://en.wikipedia.org/wiki/Computer_Othello#Evaluation_techniques)
* [A helpful video on minimax and alpha-beta pruning](https://www.youtube.com/watch?v=l-hh51ncgDI)
* [Icon source](https://apprecs.com/android/uk.co.alexcale.othello/othello)

[starting-window]: assets/starting_window.png
[settings-window]: assets/settings_window.png
[game-window]: assets/game_window.png
