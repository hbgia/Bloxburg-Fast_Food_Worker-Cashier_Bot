# Bloxburg - Fast Food Worker - Cashier Bot

This is an in-game service automation tool that uses TensorFlow to detect on-screen objects, infer the current menu state, and identify the food item plus quantity/size to click. The program then controls mouse input to place the order in the correct sequence.

## How It Works

The main loop lives in `main.py`:

1. Continuously capture the full screen.
2. Use the object detection model to identify UI elements on the screen.
3. Use a separate classifier to determine size or quantity.
4. Split the order by menu state: main, side, and drink.
5. When enough data is collected and the system is in the correct state, the program automatically clicks through the menu to place the order.

## Usage
**0. Create virtual environment (Optional).**
> ```powershell
> python -m venv .venv
> ```
> Activate virtual environment
> ```powershell
> .venv/Scripts/Activate.ps1
> ```
> If Windows blocks `.ps1` scripts, run this first in the same PowerShell window and then try again:
> ```powershell
> Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
> .venv/Scripts/Activate.ps1
> ```
> **Note**: You can use another virtual environment if you want (for example: conda)

**1.** Install the dependencies from `requirements.txt`.
> ```powershell
> pip install -r requirements.txt
> ```
> **Note**: This program was built in Python 3.11.9 so its dependencies were installed appropriately for that version. If installing fails, please try again with the mentioned Python version.

**2.** Run the program with:

> ```powershell
> python main.py
> ```

**3.** Wait for the system to finish loading before starting.
> Start your work session only after the program is ready to monitor the screen. (Seeing "State detected: 0" in terminal means it's ready).

**4.** Ensure stability.
> While the game is running, try to keep the Roblox window in full-screen so the system can read the screen and click accurately. Do not touch your desktop during operation.

**5.** Stop when you have earned enough.
> To stop, simply jump out of the cashier position. Then switch to the terminal running the program and press Ctrl + C (or simply just close the terminal).  

## Requirements
- Windows
- Python 3.11 or an equivalent environment
- Packages listed in `requirements.txt`
- TensorFlow models already present in the project directory

## Main Files

- `main.py`: main loop.
- `object_detector.py`: screen object detection.
- `quantity_and_size_classifier.py`: size/quantity classification.
- `logic.py`: state handling and order construction.
- `output_manager.py`: automated clicking for order placement.
- `input_manager.py`: screen capture and image preprocessing.

## Notes

- This program currently only works on Windows.
- This program is made specificaly for Bloxburg Fast Food Worker Cashier job only.
- If the menu or UI is blocked or resized, the program may detect the wrong state or click the wrong position.
- This is a screen-vision-based automation tool, so stability depends heavily on display quality and the game window position.
- This program performs better when you have a GPU.

## License & Project Philosophy

**License:** GNU General Public License v3.0 (GPLv3)

**Project Philosophy:**
This project is primarily a practical research application of Deep Learning and Computer Vision for GUI automation. I chose the **GPLv3** license because I believe in an open-source ecosystem. The knowledge and techniques regarding AI, OCR, and state-machine logic used here should be freely shared to foster learning and collaborative improvement, rather than being locked away in closed-source, commercialized cheating tools. 

If you use, modify, or distribute this code, you must also open-source your modifications under the same GPLv3 license. See the [LICENSE](LICENSE) file for more details.