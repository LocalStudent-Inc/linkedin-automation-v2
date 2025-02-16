# linkedin-automation-v2

## Pre-requisites

1. Install the latest version of Python.
   - You can do this by visiting the [Python website](https://www.python.org/downloads/).
   - Select the most recent version and download the installer.
2. Install Git.
   - You can do this by visiting the [Git website](https://git-scm.com/downloads).
   - If you're on macOS, you'll most likely install via Homebrew since the installer is outdated. Install Homebrew via the instructions on [brew.sh](https://brew.sh/) and then run `brew install git`.

## Installation

1. Download the repository.
   - You can press the green "Code" button and then "Download ZIP".
2. Extract the ZIP file to somewhere you can easily access.
3. Open a new terminal in the extracted folder (on macOS, you should be able to right-click the folder in Finder and select "New Terminal at Folder").
4. Run the following command to install the required Python packages:

```bash
pip3 install --user -r requirements.txt
```

## Usage

1. Open a terminal in the extracted folder.
2. Run the following command to start the script:

```bash
python3 main.py
```

3. The script will prompt you through initial setup. Follow the instructions to configure the script.
4. You can now run the script to automate LinkedIn connections.

## Getting LinkedIn Cookies When Prompted

Occasionally, you may be prompted for a `JSESSIONID` and `li_at` cookie. These are used to authenticate the script with LinkedIn. To get these cookies:

1. Open LinkedIn in your browser. You must be logged in to the same account you used to set up the script.
2. Open the developer console. You can do this by right-clicking on the page and selecting "Inspect" or pressing `Cmd + Option + I` on macOS or `Ctrl + Shift + I` on Windows/Linux.
3. Go to the "Network" tab.
4. Refresh the page.
5. Search for requests with the keyword "voyager". Any request should work so long as there's a "Cookie" header.
6. Copy the `JSESSIONID` and `li_at` cookies from the "Cookie" header.
   - For the `JSESSIONID`, you only need the value after the `=` sign, between the `"` characters.
   - For the `li_at`, you only need the value between the `=` and `;` characters.

Below is a gif demonstrating how to get the cookies:

![clip](./demo.gif)
