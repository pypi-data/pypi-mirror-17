import argparse


###################################
#### kwargs for parser options ####
###################################

# genome resquiggle opts
basedir_opt=('fast5_basedir', {
    'help':'Directory containing fast5 files.'})
graphmap_opt=('graphmap_path', {
    'help':'Full path to built graphmap version.'})
fasta_pos_opt=('genome_fasta', {
    'help':'Path to fasta file for mapping.'})

# optional genome resquiggle opts
proc_opt=('--processes', {
    'default':1, 'type':int,
    'help':'Number of processes. Default: %(default)d'})
timeout_opt=('--timeout', {
    'default':None, 'type':int,
    'help':'Timeout in seconds for the processing of a single ' +
    'read.  Default: No timeout.'})
cpt_opt=('--cpts-limit', {
    'default':None, 'type':int,
    'help':'Maximum number of changepoints to find within a single ' +
    'indel group. (Not setting this option can cause a process ' +
    'to stall and cannot be controlled by the timeout option). ' +
    'Default: No limit.'})
pat_opt=('--fast5-pattern', {
    'help':'A pattern to search for a subset of files within ' +
    'fast5-basedir. Note that on the unix command line patterns ' +
    'may be expanded so it is best practice to quote patterns.'})
ovrwrt_opt=('--overwrite', {
    'default':False, 'action':'store_true',
    'help':'Overwrite previous corrected group in FAST5/HDF5 ' +
    'file. (Note this only effects the group defined ' +
    'by --corrected-group).'})
failed_opt=('--failed-reads-filename', {
    'help':'Output failed read filenames into a this file ' +
    'with assoicated error for each read. Default: ' +
    'Do not store failed reads.'})
rcpt_opt=('--use-r-cpts', {
    'default':False, 'action':'store_true',
    'help':'Use R changepoint package to determine new event ' +
    'delimiters. (requires rpy2, R and R package ' +
    '"changepoint" to be installed)'})

# FAST5 dir opts
fast5dir_opt = ('--fast5-basedirs', {
    'nargs':'+', 'required':True,
    'help':'Directories containing fast5 files.'})
altfast5dir_opt=('--fast5-basedirs2', {
    'nargs':'+',
    'help':'Second set of directories containing fast5 files to ' +
    'compare.'})

# FAST5 data storage opts
corrgrp_opt=('--corrected-group', {
    'default':'RawGenomeCorrected_000',
    'help':'FAST5 group to access/plot created by ' +
    'genome_resquiggle script. Default: %(default)s'})
bcgrp_opt=('--basecall-group', {
    'default':'Basecall_1D_000',
    'help':'FAST5 group to use for obtaining original ' +
    'basecalls (under Analyses group). Default: %(default)s'})
bcsubgrp_opt=('--basecall-subgroup', {
    'default':'BaseCalled_template',
    'help':'FAST5 subgroup (under Analyses/[corrected-group]) where ' +
    'individual template or complement read is stored. ' +
    'Default: %(default)s'})
bcsubgrps_opt=('--basecall-subgroups', {
    'default':['BaseCalled_template',],
    'nargs':'+',
    'help':'FAST5 subgroup (under Analyses/[corrected-group]) where ' +
    'individual template and/or complement reads are stored. ' +
    'Default: %(default)s'})
twod_opt=('--2d', {
    'dest':'basecall_subgroups', 'action':'store_const',
    'const':['BaseCalled_template', 'BaseCalled_complement'],
    'help':'Input contains 2D reads. Equivalent to ' +
    '`--basecall-subgroups BaseCalled_template BaseCalled_complement`'})

# k-mer dist plotting opts
kmerlen_opt=('--kmer-length', {
    'default':3, 'type':int, 'choices':(2,3,4),
    'help':'Value of K to analyze. Should be one of {2,3,4}. ' +
    'Default: %(default)d'})
trimerthresh_opt=('--num-trimer-threshold', {
    'default':4, 'type':int,
    'help':'Number of each kmer required to include a read in ' +
    'read level averages. Default: %(default)d'})
readmean_opt=('--read-mean', {
    'default':False, 'action':'store_true',
    'help':'Plot kmer event means across reads as opposed to ' +
    'each event.'})

# misc number of item opts
numreads_opt=('--num-reads', {
    'type':int, 'default':10,
    'help':'Number of reads to plot (one region per read). ' +
    'Default: %(default)d'})
numobs_opt=('--num-obs', {
    'type':int, 'default':500,
    'help':'Number of observations to plot in each region. ' +
    'Default: %(default)d'})
numreg_opt=('--num-regions', {
    'type':int, 'default':10,
    'help':'Number of regions to plot. Default: %(default)d'})
numbases_opt=('--num-bases', {
    'type':int, 'default':51,
    'help':'Number of bases to plot from region. Default: %(default)d'})

# correction process plotting opts
regtype_opt=('--region-type', {
    'default':'random', 'choices':['random', 'start', 'end'],
    'help':'Region to plot within each read. Choices are: ' +
    'random (default), start, end.'})

# genome location plotting opts
gnmloc_opt=('--genome-locations', {
    'required':True, 'nargs':'*',
    'help':'Plot genomic locations instead of regions selected ' +
    'by criterion (default is max coverage regions). Format ' +
    'locations as "chrm:position [chrm2:position2 ...]"'})

# kmer signal plotting opts
kmer_opt=('--kmer', {
    'required':True,
    'help':'DNA K-mer of interest. Should be composed of ' +
    'ACGT characters.'})
fasta_opt=('--genome-fasta', {
    'required':True,
    'help':'FASTA file used to map reads with "genome_resquiggle" ' +
    'command.'})
deepcov_opt=('--deepest-coverage', {
    'default':False, 'action':'store_true',
    'help':'Plot the deepest coverage regions.'})

# overplotting opts
ovpltthresh_opt=('--overplot-threshold', {
    'type':int, 'default':50,
    'help':'Number of reads to trigger alternative plot type ' +
    'instead of raw signal due to overplotting. ' +
    'Default: %(default)d'})
ovplttype_opt=('--overplot-type', {
    'default':'Downsample',
    'choices':['Downsample', 'Boxplot', 'Quantile', 'Violin'],
    'help':'Plot type for regions with higher coverage. ' +
    'Choices: Downsample (default), Boxplot , Quantile, Violin'})

# write wiggle opts
wigfn_opt=('--wiggle-filename', {
    'default':'Nanopore_read_coverage.wig',
    'help':"Output wiggle read coverage file. Note that this will " +
    "also be the track name in the def line."})

# misc opts
pdf_opt=('--pdf-filename', {
    'help':'PDF filename to store plot(s). Default: %(default)s'})
quiet_opt=(('--quiet', '-q'), {
    'default':False, 'action':'store_true',
    'help':"Don't print status information."})
help_opt=(('--help', '-h'), {
    'action':'help',
    'help':"Print this help message and exit"})



# define function for getting parser so it can be shared in
# __main__ package script
def get_resquiggle_parser():
    parser = argparse.ArgumentParser(
        description='Parse raw data from oxford nanopore R9 FAST5 ' +
        'files and re-segment to match genomic alignment.',
        add_help=False)

    req_args = parser.add_argument_group('Required Arguments')
    req_args.add_argument(basedir_opt[0], **basedir_opt[1])
    req_args.add_argument(graphmap_opt[0], **graphmap_opt[1])
    req_args.add_argument(fasta_pos_opt[0], **fasta_pos_opt[1])

    filt_args = parser.add_argument_group('Read Filtering Arguments')
    filt_args.add_argument(timeout_opt[0], **timeout_opt[1])
    filt_args.add_argument(cpt_opt[0], **cpt_opt[1])

    io_args = parser.add_argument_group('Input/Output Arguments')
    io_args.add_argument(pat_opt[0], **pat_opt[1])
    io_args.add_argument(ovrwrt_opt[0], **ovrwrt_opt[1])
    io_args.add_argument(failed_opt[0], **failed_opt[1])

    fast5_args = parser.add_argument_group('FAST5 Data Arguments')
    fast5_args.add_argument(corrgrp_opt[0], **corrgrp_opt[1])
    fast5_args.add_argument(bcgrp_opt[0], **bcgrp_opt[1])
    bcsub_args = fast5_args.add_mutually_exclusive_group()
    bcsub_args.add_argument(bcsubgrps_opt[0], **bcsubgrps_opt[1])
    bcsub_args.add_argument(twod_opt[0], **twod_opt[1])

    multi_args = parser.add_argument_group('Multiprocessing Argument')
    multi_args.add_argument(proc_opt[0], **proc_opt[1])

    misc_args = parser.add_argument_group('Miscellaneous Arguments')
    misc_args.add_argument(rcpt_opt[0], **rcpt_opt[1])
    misc_args.add_argument(*quiet_opt[0], **quiet_opt[1])
    misc_args.add_argument(*help_opt[0], **help_opt[1])

    return parser


def get_max_cov_parser():
    parser = argparse.ArgumentParser(
        description='Plot raw signal in regions with the ' +
        'deepest sequencing coverage.',
        add_help=False)
    req_args = parser.add_argument_group('Required Argument')
    req_args.add_argument(fast5dir_opt[0], **fast5dir_opt[1])

    alt_args = parser.add_argument_group('Comparison Group Argument')
    alt_args.add_argument(altfast5dir_opt[0], **altfast5dir_opt[1])

    fast5_args = parser.add_argument_group('FAST5 Data Arguments')
    fast5_args.add_argument(corrgrp_opt[0], **corrgrp_opt[1])
    bcsub_args = fast5_args.add_mutually_exclusive_group()
    bcsub_args.add_argument(bcsubgrps_opt[0], **bcsubgrps_opt[1])
    bcsub_args.add_argument(twod_opt[0], **twod_opt[1])

    ovplt_args = parser.add_argument_group('Overplotting Arguments')
    ovplt_args.add_argument(ovpltthresh_opt[0], **ovpltthresh_opt[1])
    ovplt_args.add_argument(ovplttype_opt[0], **ovplttype_opt[1])

    misc_args = parser.add_argument_group('Miscellaneous Arguments')
    misc_args.add_argument(numreg_opt[0], **numreg_opt[1])
    misc_args.add_argument(numbases_opt[0], **numbases_opt[1])
    misc_args.add_argument(
        pdf_opt[0], default='Nanopore_read_coverage.max_coverage.pdf',
        **pdf_opt[1])
    misc_args.add_argument(*quiet_opt[0], **quiet_opt[1])
    misc_args.add_argument(*help_opt[0], **help_opt[1])

    return parser

def get_genome_loc_parser():
    parser = argparse.ArgumentParser(
        description='Plot raw signal in defined genomic locations.',
        add_help=False)
    req_args = parser.add_argument_group('Required Arguments')
    req_args.add_argument(fast5dir_opt[0], **fast5dir_opt[1])
    req_args.add_argument(gnmloc_opt[0], **gnmloc_opt[1])

    alt_args = parser.add_argument_group('Comparison Group Argument')
    alt_args.add_argument(altfast5dir_opt[0], **altfast5dir_opt[1])

    fast5_args = parser.add_argument_group('FAST5 Data Arguments')
    fast5_args.add_argument(corrgrp_opt[0], **corrgrp_opt[1])
    bcsub_args = fast5_args.add_mutually_exclusive_group()
    bcsub_args.add_argument(bcsubgrps_opt[0], **bcsubgrps_opt[1])
    bcsub_args.add_argument(twod_opt[0], **twod_opt[1])

    ovplt_args = parser.add_argument_group('Overplotting Arguments')
    ovplt_args.add_argument(ovpltthresh_opt[0], **ovpltthresh_opt[1])
    ovplt_args.add_argument(ovplttype_opt[0], **ovplttype_opt[1])

    misc_args = parser.add_argument_group('Miscellaneous Arguments')
    misc_args.add_argument(
        pdf_opt[0],
        default='Nanopore_read_coverage.genome_locations.pdf',
        **pdf_opt[1])
    misc_args.add_argument(numbases_opt[0], **numbases_opt[1])
    misc_args.add_argument(*quiet_opt[0], **quiet_opt[1])
    misc_args.add_argument(*help_opt[0], **help_opt[1])

    return parser

def get_kmer_loc_parser():
    parser = argparse.ArgumentParser(
        description='Plot raw signal centered on a DNA kmer ' +
        'of interest.',
        add_help=False)
    req_args = parser.add_argument_group('Required Argument')
    req_args.add_argument(fast5dir_opt[0], **fast5dir_opt[1])
    req_args.add_argument(kmer_opt[0], **kmer_opt[1])
    req_args.add_argument(fasta_opt[0], **fasta_opt[1])

    alt_args = parser.add_argument_group('Comparison Group Argument')
    alt_args.add_argument(altfast5dir_opt[0], **altfast5dir_opt[1])

    fast5_args = parser.add_argument_group('FAST5 Data Arguments')
    fast5_args.add_argument(corrgrp_opt[0], **corrgrp_opt[1])
    bcsub_args = fast5_args.add_mutually_exclusive_group()
    bcsub_args.add_argument(bcsubgrps_opt[0], **bcsubgrps_opt[1])
    bcsub_args.add_argument(twod_opt[0], **twod_opt[1])

    ovplt_args = parser.add_argument_group('Overplotting Arguments')
    ovplt_args.add_argument(ovpltthresh_opt[0], **ovpltthresh_opt[1])
    ovplt_args.add_argument(ovplttype_opt[0], **ovplttype_opt[1])

    misc_args = parser.add_argument_group('Miscellaneous Arguments')
    misc_args.add_argument(deepcov_opt[0], **deepcov_opt[1])
    misc_args.add_argument(numreg_opt[0], **numreg_opt[1])
    misc_args.add_argument(numbases_opt[0], **numbases_opt[1])
    misc_args.add_argument(
        pdf_opt[0], default='Nanopore_read_coverage.kmer_centered.pdf',
        **pdf_opt[1])
    misc_args.add_argument(*quiet_opt[0], **quiet_opt[1])
    misc_args.add_argument(*help_opt[0], **help_opt[1])

    return parser

def get_max_diff_parser():
    parser = argparse.ArgumentParser(
        description='Plot raw signal from from two samples where ' +
        'FAST5 files were corrected with `nanoraw genome_resquiggle`.',
        add_help=False)
    req_args = parser.add_argument_group('Required Argument')
    req_args.add_argument(fast5dir_opt[0], **fast5dir_opt[1])
    req_args.add_argument(altfast5dir_opt[0], required=True,
                          **altfast5dir_opt[1])

    fast5_args = parser.add_argument_group('FAST5 Data Arguments')
    fast5_args.add_argument(corrgrp_opt[0], **corrgrp_opt[1])
    bcsub_args = fast5_args.add_mutually_exclusive_group()
    bcsub_args.add_argument(bcsubgrps_opt[0], **bcsubgrps_opt[1])
    bcsub_args.add_argument(twod_opt[0], **twod_opt[1])

    ovplt_args = parser.add_argument_group('Overplotting Arguments')
    ovplt_args.add_argument(ovpltthresh_opt[0], **ovpltthresh_opt[1])
    ovplt_args.add_argument(ovplttype_opt[0], **ovplttype_opt[1])

    misc_args = parser.add_argument_group('Miscellaneous Arguments')
    misc_args.add_argument(numreg_opt[0], **numreg_opt[1])
    misc_args.add_argument(numbases_opt[0], **numbases_opt[1])
    misc_args.add_argument(
        pdf_opt[0], default='Nanopore_read_coverage.max_difference.pdf',
        **pdf_opt[1])
    misc_args.add_argument(*quiet_opt[0], **quiet_opt[1])
    misc_args.add_argument(*help_opt[0], **help_opt[1])

    return parser

def get_signif_diff_parser():
    parser = argparse.ArgumentParser(
        description='Plot raw signal from from two samples where ' +
        'FAST5 files were corrected with `nanoraw genome_resquiggle`.',
        add_help=False)
    req_args = parser.add_argument_group('Required Argument')
    req_args.add_argument(fast5dir_opt[0], **fast5dir_opt[1])
    req_args.add_argument(altfast5dir_opt[0], required=True,
                          **altfast5dir_opt[1])

    fast5_args = parser.add_argument_group('FAST5 Data Arguments')
    fast5_args.add_argument(corrgrp_opt[0], **corrgrp_opt[1])
    bcsub_args = fast5_args.add_mutually_exclusive_group()
    bcsub_args.add_argument(bcsubgrps_opt[0], **bcsubgrps_opt[1])
    bcsub_args.add_argument(twod_opt[0], **twod_opt[1])

    ovplt_args = parser.add_argument_group('Overplotting Arguments')
    ovplt_args.add_argument(ovpltthresh_opt[0], **ovpltthresh_opt[1])
    ovplt_args.add_argument(ovplttype_opt[0], **ovplttype_opt[1])

    misc_args = parser.add_argument_group('Miscellaneous Arguments')
    misc_args.add_argument(numreg_opt[0], **numreg_opt[1])
    misc_args.add_argument(numbases_opt[0], **numbases_opt[1])
    misc_args.add_argument(
        pdf_opt[0],
        default='Nanopore_read_coverage.significant_difference.pdf',
        **pdf_opt[1])
    misc_args.add_argument(*quiet_opt[0], **quiet_opt[1])
    misc_args.add_argument(*help_opt[0], **help_opt[1])

    return parser

def get_wiggle_parser():
    parser = argparse.ArgumentParser(
        description='Plot raw signal from from two samples where ' +
        'FAST5 files were corrected with `nanoraw genome_resquiggle`.',
        add_help=False)
    req_args = parser.add_argument_group('Required Argument')
    req_args.add_argument(fast5dir_opt[0], **fast5dir_opt[1])

    out_args = parser.add_argument_group('Output Argument')
    out_args.add_argument(wigfn_opt[0], **wigfn_opt[1])

    fast5_args = parser.add_argument_group('FAST5 Data Arguments')
    fast5_args.add_argument(corrgrp_opt[0], **corrgrp_opt[1])
    bcsub_args = fast5_args.add_mutually_exclusive_group()
    bcsub_args.add_argument(bcsubgrps_opt[0], **bcsubgrps_opt[1])
    bcsub_args.add_argument(twod_opt[0], **twod_opt[1])

    misc_args = parser.add_argument_group('Miscellaneous Arguments')
    misc_args.add_argument(*quiet_opt[0], **quiet_opt[1])
    misc_args.add_argument(*help_opt[0], **help_opt[1])

    return parser

def get_correction_parser():
    parser = argparse.ArgumentParser(
        description='Plot segments from before and after ' +
        'genome-guided re-segmentation for reads corrected ' +
        'with `nanoraw genome_resquiggle`.',
        add_help=False)
    req_args = parser.add_argument_group('Required Argument')
    req_args.add_argument(fast5dir_opt[0], **fast5dir_opt[1])

    type_args = parser.add_argument_group('Region Type Argument')
    type_args.add_argument(regtype_opt[0], **regtype_opt[1])

    fast5_args = parser.add_argument_group('FAST5 Data Arguments')
    fast5_args.add_argument(corrgrp_opt[0], **corrgrp_opt[1])
    fast5_args.add_argument(bcsubgrp_opt[0], **bcsubgrp_opt[1])

    misc_args = parser.add_argument_group('Miscellaneous Arguments')
    misc_args.add_argument(numreads_opt[0], **numreads_opt[1])
    misc_args.add_argument(numobs_opt[0], **numobs_opt[1])
    misc_args.add_argument(
        pdf_opt[0], default='Nanopore_genome_correction.pdf',
        **pdf_opt[1])
    misc_args.add_argument(*quiet_opt[0], **quiet_opt[1])
    misc_args.add_argument(*help_opt[0], **help_opt[1])

    return parser

def get_kmer_dist_parser():
    parser = argparse.ArgumentParser(
        description='Plot distribution of signal across kmers.',
        add_help=False)
    req_args = parser.add_argument_group('Required Argument')
    req_args.add_argument(fast5dir_opt[0], **fast5dir_opt[1])

    proc_args = parser.add_argument_group('Data Processing Arguments')
    proc_args.add_argument(kmerlen_opt[0], **kmerlen_opt[1])
    proc_args.add_argument(readmean_opt[0], **readmean_opt[1])
    proc_args.add_argument(trimerthresh_opt[0], **trimerthresh_opt[1])

    fast5_args = parser.add_argument_group('FAST5 Data Arguments')
    fast5_args.add_argument(corrgrp_opt[0], **corrgrp_opt[1])
    bcsub_args = fast5_args.add_mutually_exclusive_group()
    bcsub_args.add_argument(bcsubgrps_opt[0], **bcsubgrps_opt[1])
    bcsub_args.add_argument(twod_opt[0], **twod_opt[1])

    misc_args = parser.add_argument_group('Miscellaneous Arguments')
    misc_args.add_argument(
        pdf_opt[0], default='Nanopore_kmer_distribution.pdf',
        **pdf_opt[1])
    misc_args.add_argument(*quiet_opt[0], **quiet_opt[1])
    misc_args.add_argument(*help_opt[0], **help_opt[1])

    return parser


if __name__ == '__main__':
    raise NotImplementedError, 'This is a module.'
