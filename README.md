# ud-validation
This tool can be used to validate UniMorph data on Treebanks of Universal Dependencies. 

## Usage
Before using this tool, we need to convert the Universal Dependencies files to UniMorph schema by using [`ud-compatibility`](https://github.com/unimorph/ud-compatibility) tool.
To validate _one_ UniMorph file on a _converted file_ of Universal Dependencies, you run `evaluate.py` as follows: 


```
python evaluate.py --unimorph um\eng-um4 --gold ud\en_ud.tsv
python evaluate.py --unimorph um\eng-um4 --gold ud\en_ud.tsv --log
```

Output:

```
----- incorrectness details -----
IMP;V NFIN;SBJV;V 276
PST;V;V.PTCP PST;V 790
NFIN;V PST;V 32
NFIN;V PST;V;V.PTCP 30
PST;V;V.PTCP NFIN;SBJV;V 34
PST;V;V.PTCP IMP;NFIN;V 34
PST;V NFIN;SBJV;V 30
PST;V IMP;NFIN;V 30
IMP;V PST;V 10
IMP;V PST;V;V.PTCP 10
3;PRS;SG;V NFIN;SBJV;V 6
3;PRS;SG;V IMP;NFIN;V 6
3;PRS;SG;V PST;V;V.PTCP 2
N;PL N;SG 55
NFIN;V PRS;V;V.PTCP 1
ADJ;SG ADJ 4
ADJ;SPRL ADJ 1
NFIN;V 3;PRS;SG;V 4
ADJ;CMPR ADJ 1
N;SG N;PL 1
3;PRS;SG;V PST;V 1
PL;V 3;PRS;SG;V 1
---------------------------------
f-measure       83.37
precision       99.70
recall  71.63
```

## License
 [Creative Commons Attribution-ShareAlike 3.0 Unported (CC BY-SA 3.0)](https://creativecommons.org/licenses/by-sa/3.0/)


