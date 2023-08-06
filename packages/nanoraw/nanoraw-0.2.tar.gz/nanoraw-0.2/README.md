## Summary
This package provides tools for the analysis of raw nanopore sequencing data, including correction of basecalls and visualization.

## Installation
Install nanoraw via pip
```
pip install nanoraw
```

Install bleeding edge via github
```
pip install git+https://github.com/marcus1487/nanoraw.git
```

## Usage

```
nanoraw -h
nanoraw [command] [options]
```

#### Main Comand (Must be run before any other commands):
     genome_resquiggle             Re-annotate raw signal with genomic aignement of existing basecalls.

#### Genome Anchored Plotting Commands:
     plot_max_coverage             Plot signal in regions with the maximum coverage.
     plot_genome_location          Plot signal at defined genomic locations.
     plot_kmer_centered            Plot signal at regions centered on a specific kmer.
     plot_max_difference           Plot signal where signal differs the most between two groups.
     plot_most_significant         Plot signal where signal differs the most significantly between two groups.

#### Sequencing Time Anchored Plotting Command:
     plot_correction               Plot segmentation before and after correction.

#### Other Plotting Command:
     plot_kmer                     Plot signal quantiles acorss kmers.

#### Auxiliary Command:
    write_wiggle                  Write wiggle file of genome coverage from genome_resquiggle mappings.

> Get additional help for subcommands with `nanoraw [command] -h`

## Requirements

- HDF5 (<http://micro.stanford.edu/wiki/Install_HDF5#Install>)
- graphmap (<https://github.com/isovic/graphmap>)

#### python Requirements (handled by pip):
- python
- numpy
- scipy
- h5py
- rpy2

#### R Requirements:
- R
- ggplot2 (not actually enfored on install, but plotting commands will fail; install with `install.packages('ggplot2')` from an R prompt)

#### Optionally:
- changepoint (for using R's changepoint package for re-segmentation)
- Biopython (for robust FASTA parsing, but a simple parser is provided)

## Legal
nanoraw v.1 Copyright (c) 2016, The Regents of the University of California, through Lawrence Berkeley National Laboratory (subject to receipt of any required approvals from the U.S. Dept. of Energy).  All rights reserved.

If you have questions about your rights to use or distribute this software, please contact Berkeley Lab's Innovation and Partnerships department at IPO@lbl.gov referring to " nanoraw v.1 (2016-199)."

NOTICE.  This software was developed under funding from the U.S. Department of Energy.  As such, the U.S. Government has been granted for itself and others acting on its behalf a paid-up, nonexclusive, irrevocable, worldwide license in the Software to reproduce, prepare derivative works, and perform publicly and display publicly.  Beginning five (5) years after the date permission to assert copyright is obtained from the U.S. Department of Energy, and subject to any subsequent five (5) year renewals, the U.S. Government is granted for itself and others acting on its behalf a paid-up, nonexclusive, irrevocable, worldwide license in the Software to reproduce, prepare derivative works, distribute copies to the public, perform publicly and display publicly, and to permit others to do so.
