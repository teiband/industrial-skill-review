# skill-taxonomy-extraction

Code to extract information automatically from a review table about skill-taxonomies.

1. Open review table on google drive
2. File > Download > Comma Separated Values (.csv) > Save in project subdirectory named `data/in`
3. Goto this project directory `/src`
3. You might need to adapt the variable `results_file` in `main.py` to the filename of the csv file
3. Run `python3 main.py`
4. Check the generated graphs in subdirectory `data/out`

