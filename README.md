# GotoDL

A simple tool designed to streamline the downloading of assets from Gotopazu, facilitating easy viewing and management with [AssetStudio](https://github.com/Perfare/AssetStudio). 

## Features

- **Ease of Use**: Simplify the process of fetching the latest game assets with a user-friendly interface.
- **Compatibility**: Supports both GUI and Console modes for different user preferences.
- **Integration**: Directly compatible with AssetStudio for viewing and managing downloaded assets.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

## Prerequisites

Before running Gotopazu Asset Grabber, ensure you have:

- Python 3.8 or higher installed on your system.

### Installation

GotoDL can be used in two different modes: a graphical user interface (GUI) version and a console (CLI) version. Here are the installation instructions for each:

#### GUI Mode

To use the GUI version of GotoDL, follow these steps:

1. Download the latest `.exe` file from the [Releases](https://github.com/Ryoshiin/GotoDL/releases/latest) page on GitHub.
2. Place the downloaded `.exe` file in the same directory as the `resources` folder. This is necessary for the application to correctly load its icon.
3. Double-click the `.exe` file to run the application.

The GUI is intuitive—simply follow the on-screen instructions to download and manage Gotopazu assets.

#### CLI Mode

To install and use the CLI version of GotoDL, follow these steps:

1. **Clone the Repository**:
	```bash
	git clone https://github.com/Ryoshiin/GotoDL
	cd GotoDL\CLI
	```
2. **Install the CLI Application**:
	Install the necessary Python packages using: 
	```pip install .```

#### Usage

GotoDL supports the following command-line options:

- `-h, --help`: Shows the list of available options.
- `--path PATH, -p PATH`: Specifies the path where the files will be downloaded. Defaults to the current directory.
- `--version VERSION, -v VERSION`: Specifies the app version to download. If not specified, fetches the latest version.


### Development Setup

For those interested in further developing or customizing the GotoDL project, ensure you're in the `GotoDL` directory and then run the following command to install all necessary development dependencies::

```bash
pip install -r requirements.txt
```

## Todo List

I already invested more time than necessary in this project but here are the future improvements if i'm not lazy : 
- [ ] Fix the GUI icon that needs to be put in the same folder as the executable to be visible.
- [ ] Add a preferences section to remember the directory and extra features.
- [ ] Implement a feature to automatically update the GUI application.
- [ ] Automate the conversion of the assets through AssetStudio.
