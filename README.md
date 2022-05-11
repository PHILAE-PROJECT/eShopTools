# eShopTools

Directory eShopTools includes several tools to handle the files of the e-shop project. 

The current tools are:
- *OpenCartAction2Agilkia.py* takes a log of the e-shop case study and translates it into an Agilkia TraceSet stored in a json file.


Additional documentation is provided in the headers of these python files. 
The `traces` directory stores small examples of input files.


## Examples

### Translating a log into Agilkia

`OpenCartAction2Agilkia.py` takes a `.txt` file, storing a log of the e-shop
and generates an agilkia json file and several statistics about the input file.
The traces of the output file are grouped according to the sessionIDs of the input file.
If its argument is a directory, it processes all `.txt` files of the directory.
The resulting file is stored in the same directory as the input file. It 
has the suffix `.AgilkiaTraces.json` .

Example:

```
OpenCartAction2Agilkia.py traces\20210315_OpenCartAction.txt
```

 generates file `traces\20210315_OpenCartAction.AgilkiaTraces.json` which stores 228 events stored in 13 traces.


 