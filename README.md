# AHUS

## What is this all about?

This project is a prototype implementation of the AHUS algorithm for mining high-utility sequential patterns.

Notes:

* The prime purpose is to study how the algorithm works, it is absolutely not optimized enough for running with any real datasets.

* Make sure you have __docopt__ available on your machine (just a Python packge which helps parsing CLI arguments easily).

## How am I supposed to execute it?

```text
Usage:
    ahus -h | --help
    ahus --data-folder PATH --threshold VALUE

Options:
    -h --help       Show this screen.
    --data-folder   Either a relative or absolute path to a folder which contains three files: sequences.txt, utilities.txt and items.txt.
    --threshold     A utility threshold.
```

There are three files under the data folder, those are places where we feed data to the program. Feel free to update the folder name (e.g. data -> data-v1) but please do not change the filenames inside it.

## I want to see an example

```bash
$ ./ahus --data-folder data --threshold 10
['a', 'e', '0'] - 160
['a', 'b', '0'] - 117
['a', 'b', 'c', '0'] - 39
['a', 'b', 'e', '0'] - 57
['a', 'b', '0', 'e', '0'] - 57
['a', 'c', '0'] - 14
['a', 'd', '0'] - 306
['a', 'd', 'e', '0'] - 212
['a', 'd', '0', 'e', '0'] - 212
['a', '0', 'b', '0'] - 117
['a', '0', 'b', 'c', '0'] - 39
['a', '0', 'b', 'e', '0'] - 57
['a', '0', 'b', '0', 'e', '0'] - 57
['a', '0', 'c', '0'] - 14
['a', '0', 'd', '0'] - 306
['a', '0', 'd', 'e', '0'] - 212
['a', '0', 'd', '0', 'e', '0'] - 212
['a', '0', 'e', '0'] - 160
['b', 'c', '0'] - 33
['b', 'e', '0'] - 120
['b', '0', 'e', '0'] - 120
['c', 'f', '0'] - 14
['d', 'e', '0'] - 164
['d', '0', 'e', '0'] - 164
```
Each line shows a pattern whose utility (at the end of each line) is higher than the provided threshold.

## Research papers

A pure array structure and parallel strategy for high-utility sequential pattern mining - Bac Le, Ut Huynh a, Duy-Tai Dinh.

On efficiently mining high utility sequential patterns - Jun-Zhe Wang, Jiun-Long Huang, Yi-Cheng Chen.

USpan: An Efficient Algorithm for Mining High Utility Sequential Patterns - Junfu Yin, Zhigang Zheng, Longbing Cao.
