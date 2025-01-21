# fpl-toolkit

Jupyter Notebook tool enabling users to research, optimize, and manage their Fantasy Premier League teams.

## Features

## Installation
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

## Usage
Open the jupyter notebook with:
```bash
jupyter notebook
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Examples

## Tests
Run all unit tests:
```bash
python -m unittest discover -v
```
Run a specific unit test:
```bash
python -m unittest tests.test_optimizer.TestOptimizer.test_optimize_team
```
