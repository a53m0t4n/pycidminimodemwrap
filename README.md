The fix for the minor callerid bug this project demonstrated was incorporated into the latest minimodem which you should compile from https://github.com/kamalmostafa/minimodem. 

Turns out I was using wierd flags on minimodem, which fixed half the problem.

Everything was implemented almost perfect in minimodem as is except for a case unencountered by minimodem's author, on my verizon landline (Bridge St. DS0, is this common everywhere or specific to me?) in which a CPN number is passed, but since the name is unavailable, an 0x08 ascii backspace char is passed in lieu of a name. Problem solved.





====================================================================================


This project is wrapped around minimodem by Kamal Mostafa.
http://www.whence.com/minimodem/


Ever since I was a kid I wondered specifically how caller id worked. This weekend I was able to learn
more about it in great detail.

How is caller id passed in North America?

Caller ID is passed through the phone switch in an audio burst of Frequency Shift Modulation after the first ring before the 
receiving end of the call picks up their line. 
specifically the Bellcore FSK specification which is almost identical to Bell Type 202 (1200 baud ascii).

What differs in the Bell 202 and Bellcore FSK specs?

As detailed in https://hkn.eecs.berkeley.edu/~drake/callsense/callerid.html Bellcore FSK uses the same 
frequencies, modulation, and data format as Bell type 202 modems, but once demodulated the bytes are partially
ascii and partially checksum + flags for the message type, and MDMF (or CNAM) includes further specifications
on the included parameters which include the calling party's name (an improvement over SDMF).

I wrote this pythonic wrapper around minimodem's --binary-output flag to get multiple callerids out of one .wav file.

Minimodem is one of my favorite programs in existence, and I have done 2 cool projects with it so far. This weekend, when I tried recording
my phone getting incoming phone calls while on the hook (with my $20 RJ411 to audio out bridge + voice recorder from ali express) 
and using minimodem's '-a callerid' flag I had spotty results since my sound files contained multiple FSK databursts, or did not 
always come around with the results expected by minimodem to pass as "callerid" specifically, but the bytes were being properly demodulated on
minimodem's 1200 bell 202 mode. This script just interprets the binary output and handles it differently (?) than minimodem.


python ReadCIDTone.py [file.wav]
