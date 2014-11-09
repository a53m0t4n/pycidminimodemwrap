The fix for a minor unexpected case in callerid this project demonstrated was incorporated into the latest minimodem which you should compile from https://github.com/kamalmostafa/minimodem. 

Turns out I was using wierd flags (-a is autocarrier for poorer audio conditions as found in DXing and HAM i.e, RTTY) on minimodem, removing this as per Kamal's suggestion fixed half the problem.

The minor problem in minimodem's caller id implementation had something to do with the following scenario being unexpected:
" ...if the number and name had not been included then the parameter types for those fields would be different. These alternate parameter types are used to signify that the data contained in that parameter is the reason for its absence. The parameter type for the number section would have been a binary 00000100 (decimal 4) and the parameter type for the name section would have been a binary 00001000 (decimal 8)..."
https://hkn.eecs.berkeley.edu/~drake/callsense/callerid.html

