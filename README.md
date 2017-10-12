This is a [CK](http://cKnowledge.org) repository for [pWord2Vec](https://github.com/vasupsu/pWord2Vec) project.

## Pre-requisites

See [pWord2Vec](https://github.com/vasupsu/pWord2Vec) page for pre-requisites.

## Installation

* Installing CK and this repository:

```
$ [sudo] pip install ck
$ ck pull repo --url=https://github.com/vasupsu/IA3_Paper16_ArtifactEvaluation
```

* Installing dataset packages:
```
$ ck install package --tags=words
```

Repeat until you install all required datasets (text8, billion) ...

* Compiling original program and resolving software dependencies

```
$ ck compile program:word2vec
```

If CK couldn't find your ICC installation, you can specify a full path to ICC's compilervars.sh as following:
```
$ ck detect soft:compiler.icc --full_path={FULL PATH to compilervars.sh}
```
and then try to compile above program again

* Testing original program
```
$ ck run program:word2vec
```

CK will ask you to select installed dataset and will then run this program.
