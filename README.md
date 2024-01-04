# Coin

Developed in Python, it uses the MetaTrader5 API and the DearPyGui user interface to provide an efficient and easy-to-use trading experience. This bot is based on a hedging strategy that takes advantage of market volatility during opening sessions.

Requirements
----------

- Python 3.11.4
- Pipenv

Installation
-----------

+ Make sure you have Python 3.11.4 installed on your system. You can check your Python version with the following command:

``` Bash
python --version
```

+ Install Pipenv, which is a packaging tool for Python. You can install it with the following command:

``` Bash
pip install pipenv
```

+ Clone the Coin repository:

``` Bash
git clone https://github.com/davdcsam/Coin.git
cd Coin
```

+ Activate Pipenv virtual environment:

``` Bash
pipenv shell
```

+ Install the project dependencies with Pipenv:

``` Bash
pipenv install
```

Quick usage
----------

+ Activate Pipenv virtual environment:

``` Bash
pipenv shell
```

+ Run the main Coin script:

``` Bash
python main.py
```

This will open the Coin user interface, where you can interact with the MetaTrader5 API.


Creating an executable file
--------------------------

This project uses PyInstaller to convert the Python script into an executable file. To create the executable file, follow these steps:

+ First, switch to main_build branch

``` Bash
git checkout main_build
```

+ Activate Pipenv virtual environment:

``` Bash
pipenv shell
```

+ Make sure you have PyInstaller installed. 

``` Bash
pyinstaller --version
```

+ If you don't have it, you can install it with pip:

``` Bash
pipenv install pyinstaller
```

+ Run the following command in the root of the project:

``` Bash
pyinstaller --onefile --windowed --name=Coin --icon=assets/Coin.ico main.py
```

This command tells PyInstaller to create an executable file from the `main.py` script. The options used are as follows:

- `--onefile`: Creates a single executable file.
- `--windowed`: Suppresses the console when running the application.
- `--name=Coin`: Sets the executable file name to "Coin".
- `--icon=assets/Coin.ico`: Sets the icon of the executable file to "Coin.ico" located in the "assets" folder.

Copying folders to the dist/ folder
------------------------------------

After creating the executable file, you can copy the `assets/`, `data/`, and `files/` folders to the `dist/` folder with the following commands:

For Unix/Linux:

``` Bash
cp -r assets/ data/ files/ dist/
```

For Windows:

``` Bash
xcopy /E /I assets dist\assets
```

``` Bash
xcopy /E /I data dist\data
```

``` Bash
xcopy /E /I files dist\files
```

Documentation
-------------

For more information on how to use Coin, see the [full documentation no available].

Contributions
--------------

Contributions are welcome. Theren't no a guide for fork or makes pull request yet.

License
--------

Coin is licensed under the a property license. See the `LICENSE` file for details.
