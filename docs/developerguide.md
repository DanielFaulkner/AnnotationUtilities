## Developer guide:

All the utilites have been written in Python, using only the standard builtin libraries. To avoid adding additional installation steps where practical contibutions using builtin libraries should be used preferentially.

To enable code reuse each utiliy has a corresponding module in the 'lib' folder which contains functions and objects which are suitable for reuse either in other utilities or in other interface types. Those functions which are shared between utilites are the module libAnnoShared.py. Comments and docstrings have been used to give indications of usage within those modules.


# File specifications:
- [BED and GTF](https://genome.ucsc.edu/FAQ/FAQformat.html)
- [GTF](https://mblab.wustl.edu/GTF22.html)
- [DFAM](https://www.dfam.org/releases/Dfam_3.3/userman.txt)
- [UCSC Table browser](https://genome.ucsc.edu/cgi-bin/hgTables)
-- See userguide for the settings required to both download and view UCSC Table browser annotations.
