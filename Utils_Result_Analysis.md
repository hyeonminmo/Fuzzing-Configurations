# Utils for fuzzing result analysis

## 1. Rename inputs in a corpus
```
$ /path/to/this/repo/UtilsResultAnalysis/tCaseRename.sh /path/to/a/corpus/inputs/ renamedinputs
```

## 2. Extract stack traces of inputs in a renamed corpus
```
$ /path/to/this/repo/UtilsResultAnalysis/tCaseStackTrace.sh executable renamedinputs stacktraces 
```
`executable` is the executable binary of the target program.
`stacktraces` is the directory storing stack traces of each renamed inputs.
