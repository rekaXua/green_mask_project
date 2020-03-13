@echo off
Color 0A 
Title Rename DCP Files to MD5 Hashes
echo(
SetLocal EnableDelayedExpansion
md decensor_input_renamed
cd decensor_input_original
for %%a in (*.png) do (
     for /f "skip=1 delims=" %%H in ('CertUtil -hashfile "%%a" MD5 ^| findstr /i /v "CertUtil"') do ( set H=%%H)
        echo "%%a" = "!H!.png"
        Ren "%%a" "!H!.png"
		Ren "..\decensor_input\%%a" "!H!.png"
		move "..\decensor_input\!H!.png" "..\decensor_input_renamed\!H!.png"
)
EndLocal
Pause & Exit