# How to: Preview changes as they will be displayed in the app

## Introduction
Occasionally, it will be convinient to be able to visualise a clean text in the same way in which it will be ultimately be displayed without having to submit a pull request and merge to the `dev` branch. This is particularly true during the encoding of variation, where the encoding can be tricky to make sense of with the naked eye. The following process will allow you to quickly check what the changes you made will look like once you merge your branch to `dev`.

## Requirements
- You must have Python installed in your system. To verify whether you do, open a terminal window and type:
```
python --version
```
If you see something like `Python 3.9.7`, you have Python. Ideally, you will need at least Python 3 (i.e., first number should be 3), otherwise the process might not work. If see any other message (like `command not found`), head over to [https://www.python.org/](https://www.python.org/), download the latest release to your system, open the installer then follow the on-screen instructions.

## Instructions
1. Ensure you are in the [correct branch](../12_ensure_correct_branch/12_ensure_correct_branch.md), that is, the branch that contains the changes you want to preview.
2. Open a new terminal window in the repository folder: (on Mac, [follow these instructions](https://support.apple.com/en-gb/guide/terminal/trmlb20c7888/mac#:~:text=On%20your%20Mac%2C%20open%20a,window%3A%20Choose%20Open%20in%20Terminal.))
3. Enter the following command in the terminal:
```
python start_preview.py
```
4. If everything worked well, your default browser should have opened with a preview of your latest changes.
5. If your changes are not as you expected, check the terminal window: if there was a problem with any of the `<app>` it will tell you where the problem is (or where it is likely to be)
6. If no browser window opened, let Tiago know what error message you received.