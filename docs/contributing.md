**Thanks for considering contributing to Parsera!**   
This project is in the early stage of development, so any help will be highly appreciated. You can start from looking through existing [issues](https://github.com/raznem/parsera/issues), or directly asking about the most helpful contributions on [Discord](https://discord.gg/gYXwgQaT7p).

## Issues
The best way to ask a question, report a bug, or submit feature request is to [submit an Issue](https://github.com/raznem/parsera/issues/new). It's much better than asking about it in email or Discord since conversation becomes publicly available and easy to navigate.

## Pull requests
### Installation and setup
Fork the repository on GitHub and clone your fork locally.  

Next, install dependencies using poetry:
```bash
# Clone your fork and cd into the repo directory
git clone git@github.com:<your username>/parsera.git
cd parsera

# If you don't have poetry install it first:
# https://python-poetry.org/docs/
# Then:
poetry install
# If you are using VS Code you can get python venv path to switch:
poetry which python
# To activate virtual environment with installation run:
poetry shell
```
Now you have a virtual environment with Parsera and all necessary dependencies installed.

### Code style
The project uses `black` and `isort` for formatting. Set up them in your IDE or run this before committing:
```bash
make format
```

### Commit and push changes
Commit your changes and push them to your fork, then create a pull request to the Parsera's repository.


**Thanks a lot for helping improve Parsera!**
