Load point cloud data of heliostat surface.
Clean it up.
Fit curves to it.
Graph residual error.

Install with "poetry install".
Run with "poetry run src/surface_analysis/main.py"


Workflow:
1. Have a folder full of scans that you want to process.
2. Inside that folder have a file called designfocallengths.txt where each line is "<scan-name> <design-focal-length>".
3. Have a config file that contains the width, height and optionall the desired fileloader and preprocessor to use.
