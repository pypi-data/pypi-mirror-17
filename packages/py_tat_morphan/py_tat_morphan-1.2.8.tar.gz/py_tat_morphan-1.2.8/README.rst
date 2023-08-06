Morphological Analyser of Tatar language
========================================

Morphological Parser of Tatar language. Uses HFST-tool.
Web form which uses this tool: http://tatmorphan.pythonanywhere.com/


To install:
-----------

$ pip install py_tat_morphan


To use lookup:
--------------

$ tat_morphan_lookup


To process text:
----------------

$ tat_morphan_process_text <filename>


To process whole folder:
------------------------

$ tat_morphan_process_folder <path_from>

or

$ tat_morphan_process_folder <path_from> <path_to>

Note: if you do not provide <path_to>, programm puts analyzed texts into folder near initial with '_analyzed' postfix. Eg, if <path_from>='/home/ramil/mytexts/', then <path_to>='/home/ramil/mytexts_analyzed/'.


To use as python module:
------------------------

>>> from py_tat_morphan.morphan import Morphan
>>> morphan = Morphan()
>>> print(morphan.analyse('урманнарга'))
>>> print(morphan.lemma('урманнарга'))
>>> print(morphan.pos('урманнарга'))
>>> print(morphan.process_text('Без урманга барабыз.'))
>>> print(morphan.analyse_text('Без урманга барабыз.'))
>>> print(morphan.disambiguate_text('Язгы ташуларда көймә йөздерәбез.'))

For feedback:
-------------

ramil.gata@gmail.com


Versions:
---------

1.2.1 
|    Uses HFST python package

1.2.2 
|    Add tat_morphan_lookup and tat_morphan_process_text scripts to bin/

1.2.3 
|    Fixed exception dictionary

1.2.4 
|    Fixed to use C HFST package 
|    Added tat_morphan_process_folder script to bin/
|    Added Russain Morphological Analyser (pymorphy2 package) to detect russian words in text

1.2.5
|   Fixed morphophonetic and morphotacktic rules
|   Added tat_morphan_stats_of_folder script to bin/

1.2.6
|   Fixed dictioray collection

1.2.7
|   Added morphological disambiguation stage using contextual rules methods
|   Fixed Russian word detection
|   Fixed tat_morphan_stats_of_folder script

1.2.8
|   Fixed bug with '-'
|   Added fifth type for contextual rules. Now you can check if word starts with capital letter
|   Added is_amtype_pattern method to check if amtype is formed properly
