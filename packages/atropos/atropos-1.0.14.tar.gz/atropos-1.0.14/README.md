![https://travis-ci.org/jdidion/atropos](https://travis-ci.org/jdidion/atropos.svg?branch=master)
![https://pypi.python.org/pypi/atropos](https://img.shields.io/pypi/v/atropos.svg?branch=master)

# Atropos

Atropos is tool for specific, sensitive, and speedy trimming of NGS reads. It is a fork of the venerable Cutadapt read trimmer (https://github.com/marcelm/cutadapt, [DOI:10.14806/ej.17.1.200](http://dx.doi.org/10.14806/ej.17.1.200)), with the primary improvements being:

1. Multi-threading support, including an extremely fast "parallel write" mode.
2. Implementation of a new insert alignment-based trimming algorithm for paired-end reads that is substantially more sensitive and specific than the original Cutadapt adapter alignment-based algorithm. This algorithm can also correct mismatches between the overlapping portions of the reads.
3. Options for trimming specific types of data (miRNA, bisulfite-seq).
4. A new command ('detect') that will detect adapter sequences and other potential contaminants (this is experimental).
5. A new command ('error') that will estimate the sequencing error rate, which helps to select the appropriate adapter- and quality- trimming parameter values.
5. The ability to merge overlapping reads (this is experimental and the functionality is limited).
6. The ability to write the summary report and log messages to separate files.
7. The ability to read and write interleaved FASTQ output.
8. A progress bar, and other minor usability enhancements.

## Dependencies

* Python 3.3+ (python 2.x is NOT supported)
* Cython 0.24+ (`pip install Cython`)
* progressbar or tqdm (optional, if you want progressbar support)
* khmer 2.0+ (`pip install khmer`) (optional, for detecting low-frequency adapter contamination)

## Installation

`pip install atropos`

## Usage

Atropos is almost fully backward-compatible with cutadapt. If you currently use cutadapt, you can simply install Atropos and then substitute the executable name in your command line, with one key difference: you need to use options to specify input file names. For example:

```{python}
atropos -a AGATCGGAAGAGCACACGTCTGAACTCCAGTCACGAGTTA -o trimmed.fq.gz -se reads.fq.gz
```

To take advantage of multi-threading, set the `--threads` option:

```{python}
atropos --threads 8 -a AGATCGGAAGAGCACACGTCTGAACTCCAGTCACGAGTTA -o trimmed.fq.gz -se reads.fq.gz
```

To take advantage of the new aligner (if you have paired-end reads with 3' adatpers), set the `--aligner` option to 'insert':

```{python}
atropos --aligner insert -a AGATCGGAAGAGCACACGTCTGAACTCCAGTCACACAGTGATCTCGTATGCCGTCTTCTGCTTG \
  -A AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGTAGATCTCGGTGGTCGCCGTATCATT -o trimmed.1.fq.gz -p trimmed.2.fq.gz \
  -pe1 reads.1.fq.gz -pe2 reads.2.fq.gz
```

See the [Documentation](https://atropos.readthedocs.org/) for more complete usage information.

## Links

* [Documentation](https://atropos.readthedocs.org/)
* [Source code](https://github.com/jdidion/atropos/)
* [Report an issue](https://github.com/jdidion/atropos/issues)

## Planned enhancements and experiments

Note: while we consider the command-line interface to be stable, the internal code organization of Atropos is likely to change substantially. At this time, we recommend to not directly interface with Atropos as a library (or to be prepared for your code to break). The internal code organization will be stablized as of version 1.1, which is planned for early
2017, and will also include the following enhancements:

* Currently, InsertAligner requires a single 3' adapter for each end. Adapter trimming will later be generalized so that A) the InsertAligner can handle multiple matched pairs of adapters and/or B) multiple different aligners can be used for different adapters.
* Add option to estimate bisulfite conversion rate from filled-in cytosine methylation status in reads that were MspI-digested.
* Migrate to [Screed](https://github.com/dib-lab/screed) if there is no performance penalty.
* Migrate to Versioneer for version management.
* Look at bugs/requests in https://github.com/marcelm/cutadapt/issues and see which need to be fixed in Atropos (also submit these fixes back to Cutadapt when possible).

If you would like to suggest additional enhancements, you can submit issues and/or pull requests at our GitHub page.

## Citations

The citation for the original Cutadapt paper is:
 
> Marcel Martin. "Cutadapt removes adapter sequences from high-throughput sequencing reads." EMBnet.Journal, 17(1):10-12, May 2011. http://dx.doi.org/10.14806/ej.17.1.200

A manuscript for Atropos is currently in preparation. For now, you can cite it as:

> John P Didion. "Atropos." 2016. https://github.com/jdidion/atropos
