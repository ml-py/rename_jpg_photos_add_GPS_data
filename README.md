### Rename photographics made by digital cameras to TheOnlyTime format ⠀and ⠀adds GPS data to the file name.

It's changing pictures name 


```
from   20180612_154238_Burst25.jpg
to       180612wto154238 ___GPS 50.044242,19.206877 +0mnpm__Model_LG·H870_LG·G6__Burst25.jpg

from   20190731_200219.jpg
to       190731śro200219 ___GPS 50.067411,19.929245 +279mnpm__Model_LG·H870_LG·G6.jpg

from   20190918_203706_HDR.jpg
to       190918śro203706 ___GPS 50.065031,19.926411 +257mnpm__Model_LG·H870_LG·G6__HDR.jpg

from   IMG_20180114_164145.jpg
to           180114nie164145 ___NoGPS__Model_Quantum350Lite·GoClever.jpg
```

GPS coordinates are surrounded by spaces for fast selection ⠀so you just copy and paste into browser address bar. <br> 
Characters ` [ 6 : 9 ] `  are shortened names of the week days in Polish. If you want other language you need to change the dict in the ` 220415pią1327.A … ` file.

### How to proceed?

* Run the file ` 220415pią1327.A … ` in the folder with pictures. ⠀It will create two txt files. <br> 
* Than open the file ` 220415pią1327.B … ` 
* Type the name of the ` … dictionary .txt ` into ` f ` variable. ⠀⠀For example: <br>
` f  =  open(   "220415pią141358 TheOnlyTime+GPS LOG NumOfRenamedPictures452 dictionary .txt",   "r"   ) `  
* Than run ` 220415pią1327.B … ` file. ⠀⠀It will do the renaming.

The ` … HumanReadable .txt ` is for you to check by yourself how replacement will be done.  

You can try it on four sample pictures located in this repo.

TODO: ⠀Add support for SONY (` DSC_0001.JPG `) and iPhone (` IMG_0001.JPG `) <br>
Since their naming conventions are not quite the best ⠀for pictures from ⠀digital cameras with inner clock ⠀in 3<sup>rd</sup> decade of 21<sup>st</sup> century. 
⠀The date should be taken from modification date ⠀so after renaming you can put photos from many days ⠀into one folder location ⠀without names collision.
