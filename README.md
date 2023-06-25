Implements (parts of) the algorithm presented in the research paper "Approximating a full Bidirectional Reflectance Distribution Function from a slice", which is currently unpublished. <br>
Creates three-dimensional BRDFs from a list of two-dimensional points trough solids of revolution. <br>
To use the program run the main.py file.<br>
To create a different BRDF simply alter the input data.<br>

NOTES:
1. Part of the algorithm is not completely implemented; <br> You need to manually divide the slice into sub-curves and provide the axis of rotation for each.
2. The program does not save the BRDF to a file, it only visualizes it.

<br>
Author: Gino Tramontina


Both code and research paper were created for The Computer Graphics and Visualization group at the TU Delft. <br>
This code was made during the Research Project CSE3000, 2022/2023; a part of CSE bachelor at TUDelft (https://github.com/TU-Delft-CSE). <br>
Find all public submissions for the Research Project CSE3000 at: https://github.com/TU-Delft-CSE/Research-Project