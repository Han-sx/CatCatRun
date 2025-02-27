# CatCatRun! Game

## Introduction
CatCatRun! is an exciting space shooting game developed using the Pygame library in Python. In this game, players control a character to shoot down various enemies and avoid being hit. When the player's lives run out, an end - video will play in a loop until the player presses the ESC key to exit.

## Features
1. **Multiple Enemy Types**: There are four types of enemies (cat, dog, leopard, tiger), each with different health points.
2. **Animated Character**: The player character has an animated walking effect.
3. **Sound Effects**: The game includes shooting sounds, enemy - hitting sounds, and background music to enhance the gaming experience.
4. **Pause Function**: When the player is hit by an enemy, the game pauses for one second.
5. **End - Video Loop**: After the player loses all lives, an end - video will play in a loop.

## Installation
### Prerequisites
- Python 3.12.4 or higher
- Pygame 2.6.1
- OpenCV (cv2)

### Steps
1. **Clone the Repository**
    - Open your terminal or command prompt.
    - Navigate to the directory where you want to store the project.
    - Run the following command to clone the repository:
```bash
git clone <repository_url>
```
2. **Install Dependencies**
    - If you haven't installed Pygame and OpenCV, you can install them using `pip`:
```bash
pip install pygame opencv - python
```

## How to Play
1. **Start the Game**
    - Navigate to the project directory in the terminal.
    - Run the following command to start the game:
```bash
python CatCatRun!.py
```
2. **In - Game Controls**
    - **Movement**: Use the `W`, `A`, `S`, `D` keys to move the player character up, left, down, and right respectively.
    - **Shoot**: Press the `J` key to shoot bullets at enemies.
    - **Pause and Exit**: Press the `ESC` key to exit the game. When the end - video is playing, press `ESC` to stop the video and exit the game.

## Directory Structure
- `image/`: Contains all the image files used in the game, such as player sprites, enemy sprites, bullet images, and background images.
- `sound/`: Stores all the sound files, including shooting sounds, enemy - hitting sounds, and background music.
- `video/`: Holds the end - video file that plays when the player loses all lives.
- `CatCatRun!.py`: The main Python script that runs the game.

## Known Issues
- **Resource Loading**: If the game fails to load images, sounds, or the video, please check if the files in the `image`, `sound`, and `video` directories exist and are named correctly.
- **Compatibility**: The game is developed and tested on specific versions of Python, Pygame, and OpenCV. Compatibility issues may occur on different versions or operating systems.

## Contributing
If you want to contribute to this project, please fork the repository and submit a pull request. You can also open an issue if you find any bugs or have suggestions for improvement.

## License
This project is released under the [MIT License](https://opensource.org/licenses/MIT). You are free to use, modify, and distribute the code as long as you include the original copyright notice and license.
