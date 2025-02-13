# fpl-toolkit ⚽

Jupyter Notebook tool enabling users to research, optimize, and manage their Fantasy Premier League teams.

## Features

- 📊 **Extract Data & Insights**: Easily extract data for each player and their clubs from the official FPL API, and gain valuable insights for your research.
- ⬇️ **Download Team Info**: Download the information for your own FPL team.
- 📈 **Optimize Team**: Optimize your own FPL team based on a customizable expected points calculator.



## Installation

If you want to check out the tool instantly click on the binder link here (**TODO**) which hosts an interactive jupyter notebook for you.  

Alternatively, if you want to use it locally follow

1. Clone the repository:
   ```bash
   git clone https://github.com/aav31/fpl-toolkit.git
   cd fpl-toolkit
   ```
2. Create the conda environment:
   ```bash
   conda env create -f environment.yml
   ```
3. Activate the environment
   ```bash
   conda activate fpl-toolkit
   ```

This will install all the necessary libraries and tools required to run the project.

## Basic Usage
Open the jupyter notebook in the usual way with `jupyter notebook` or `jupyter lab` (in binder you don't need to do this) and navigate to the [Quickstart Notebook](./quickstart.ipynb) which contains a some examples to get you started.

The `fpl` package contains the following modules:
- [`expected_points_calculator.py`](./fpl/expected_points_calculator.py)
- [`formation.py`](./fpl/formation.py)
- [`loader.py`](./fpl/loader.py)
- [`optimizer.py`](./fpl/optimizer.py)
- [`player.py`](./fpl/player.py)
- [`team.py`](./fpl/team.py)


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg)


## Tests
Run all unit tests:
```bash
python -m unittest discover -v
```
Run a specific unit test:
```bash
python -m unittest tests.test_optimizer.TestOptimizer.test_optimize_team
```
