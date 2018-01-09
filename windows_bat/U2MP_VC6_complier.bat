
set spath=D:\3S_PC\sourceCode\USB_20\MP\src\

cd %spath%


msdev U3SDiskMTest.dsp /make "U3SDiskMTest - Win32 Debug" /rebuild
msdev U3SDiskMTest.dsp /make "U3SDiskMTest - Win32 Release" /rebuild
msdev U3SDiskMTest.dsp /make "U3SDiskMTest - Win32 Tester Release" /rebuild
msdev U3SDiskMTest.dsp /make "U3SDiskMTest - Win32 Tester debug" /rebuild










pause



