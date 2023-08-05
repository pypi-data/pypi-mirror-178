read~vmeoffline~
================

*we read asc data files from CAEN - created by gregory (or mc2). Create
histograms, count zeroes etc...*

Usage - brief version 2022
--------------------------

We try to update - with experiment 2021 12 03

``` {.shell}
./bin_readvme cut ~/09_DATA_ANALYSIS/20211203_54fe_nfs_ganil/Evaluation_1_fe40/run0055_211203_203227_1Fe40p3.asc 0 5 15
```

cuts channel 0 from 5sec to 15 sec

### eva~cuttime~

-   `simple_read.eva_cut_time`
    -   calls `general.readtable`
    -   calls `general.select_channels`
    -   calls `general.enhance_by_dtus...`
    -   call `general.detect_zeroes` for timewindow 4.2us

offers

Usage -brief version (OLD)
--------------------------

``` {.shell}
# convert asc to h5
read_vme_offline a2df run0022_20190719_070923.asc

# create spectra and table and ORG (text) file
read_vme_offline df2s run0014_20190718_165928.h5 --Emax 15200 -Ethres 5

# MASS CONVERT:
ls -1 *asc | xargs -n 1 -I III  read_vme_offline a2df III
ls -1 *h5 | xargs -n 1 -I III  read_vme_offline df2s  III  --Emax 15200 -Ethres 5

```

Installation
------------

-   you can use `./pipall.py` to get all python modules needed
-   since this is an exprerimental project, the recommended way to
    install is
    -   `pip3 install -e .`
    -   then you work on the code in local repo and run it globally in
        the same time
    -   remove with `pip3 uninstall project`

Installation of ROOT
--------------------

-   we start the manual with 6.22:
    <https://root.cern/releases/release-62206/>
-   the file `root_v6.22.06.Linux-ubuntu20-x86_64-gcc9.3.tar.gz`
-   create/unpack in in `~/root`
-   run `source ~/root/bin/thisroot/sh`
-   go to `~/root/tutorials/pyroot` and run `python3 demo.py`
-   something works, but there is a lot of problems

Connecting together
-------------------

-   in the terminal, where `source thisroot.sh` was run try to call
    `read_vme_offline`
-   install

dependent module\'s details
---------------------------

### root~numpy~

See <http://scikit-hep.org/root_numpy/>

-   create and FILL HISTOGRAMS from `numpy array`
-   an efficient interface between ROOT and NumPy
-   At the core of root~numpy~ are powerful and flexible functions for
    converting ROOT TTrees into structured NumPy arrays
-   converting NumPy arrays back into ROOT TTrees
-   function for creating a random NumPy array by sampling a ROOT
    function or histogram:

``` {.python}
from root_numpy import fill_hist
import numpy as np

# Fill a ROOT histogram from a NumPy array
hist = TH2D('name', 'title', 20, -3, 3, 20, -3, 3)
fill_hist(hist, np.random.randn(1000000, 2))
hist.Draw('LEGO2')
```

### pylatex

*library for creating and compiling LaTeX files or snippets*

-   dependencies maybe
    `sudo apt-get install texlive-pictures texlive-science texlive-latex-extra latexmk`
-   <https://github.com/JelteF/PyLaTeX>

History
-------

-   jm entered 2020 05 26
-   jm access 2021 02 19
