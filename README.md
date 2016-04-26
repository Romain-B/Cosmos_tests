# Cosmos_tests
This repository contains tests I've done on the Cosmos python library (using a small quality treatment algorithm)

## Requirements
* Cosmos 2 must be installed (see [here](http://cosmos.hms.harvard.edu/COSMOS2/))
* Jupyter must be installed (at least to use the ipython notebooks in the 'src' folder see [here](http://jupyter.org/))
* R must be installed (any version over 2.1 will do, see [here](https://www.r-project.org/))

## Setting up the tests
* Go to the directory you have Cosmos 2 installed and find the 'examples' directory.
* Rename the 'main.py' file to  anything (main.old.py for example)
* Copy the given 'main.py' and 'testxx.py' files in this repository in the current directory (path2yourCosmosInstall/examples)
* Then copy the **entire** src folder in the 'examples' directory.

## Jupyter notebooks
The notebooks in the src folder work separately from the 'testxx.py' and 'main.py' files, they are a handy way to visualize the code while it's running (to launch the jupyter notebook local server, type `jupyter notebook` in a command prompt and get to the files with the interface that pops up) Once you've opened the notebook click 'Cell'->'Run All' in the menu bar to run all the code cells.
* The 'Tools-test.ipynb' notebook only tests the different tools for the Quality treatment, it has no link to cosmos. Results will appear in the generated 'data' and 'results' folders (under 'src').
* The 'Workflow_test.ipynb' notebook uses Cosmos, and basically the IPython notebook version of the 'testxx.py' file. Results will appear in the generated 'testing' folder (under 'src').

## Cosmos tests
To launch the Cosmos Web interface, go to the 'src' folder you added and use the following command :
```
python ../main.py runweb --host 0.0.0.0 --port 8080
``` 
(similar to what's given in the tutorial at [this page](http://cosmos.hms.harvard.edu/COSMOS2/3_getting_started.html#launch-the-web-interface)).
Now, when you go to [http://localhost:8080/](http://localhost:8080/) you should see the Cosmos web interface.
The terminal in which you launched the command is now constantly running that interface. Open a new terminal (or add a '&' character after the command) go to the 'src' folder and execute the following command :
```
python ../testxx.py runweb --host 0.0.0.0 --port 8080
``` 
You will see the job start its process in the terminal and if you look at the web interface and click on the 'Testx' job, you will see the tasks and their status. The results of this test will be found in the generated 'testing' folder and its subfolders.
