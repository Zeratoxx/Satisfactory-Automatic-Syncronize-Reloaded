@ECHO OFF

REM Die Befehle 'REM' und '::' sind Kommentare!
::  Das hier ist also auch ein Kommentar!
REM Das hier ist also auch ein Kommentar!
:: Unterschied:
:: '::'-Kommentare werden auch bei @ECHO ON ausgeblendet!!
:: 'REM'-Kommentare werden bei @ECHO ON nicht ausgeblendet!!
:: @ECHO OFF





SETLOCAL EnableExtensions
SETLOCAL enabledelayedexpansion
SET checkInterval=2
SET useExperimental=false
SET exeName=FactoryGameEGS.exe
SET gitMessageFile=gitMessage.txt
SET PATHTOSAVED=C:\Users\%username%\AppData\Local\FactoryGame\Saved
SET keepDirInSaved=blueprints
SET saveGames=SaveGames
SET whichSaved=%saveGames%\common\
SET nameOfWorldlistFile=listOfWorlds.txt
SET saveChoiceFile=lastChoice.txt
SET saveWorldChoiceFile=lastWorldChoice.txt
SET counter=0
SET listOfRepos=
SET alreadyStarted=
SET workWithZip=
SET searchVal=rejected




CD /D %PATHTOSAVED%

IF EXIST %nameOfWorldlistFile% (
	REM Go on.
) ELSE (
	ECHO Cannot find %nameOfWorldlistFile%. Please set it up correctly.
	GOTO error
)

FOR /F "tokens=*" %%f IN (%nameOfWorldlistFile%) DO (
	
	SET /A counter=counter+1
	CALL :concat !counter! "%%f"
)

IF NOT EXIST %PATHTOSAVED%\%whichSaved% (
	MKDIR %PATHTOSAVED%\%whichSaved%
)





REM KEINE DEMO.
GOTO select

ECHO Anderes Programm starten?
SETLOCAL
CHOICE /n /C "JN" /m "(J / N)"
IF errorlevel 2 GOTO nein1
IF errorlevel 1 GOTO ja1






:nein1
:select
SET theGameChoice=
SET previousGameChoice=n
IF NOT EXIST %saveChoiceFile% (
	(ECHO %theGameChoice%)>%saveChoiceFile%
) ELSE (
	SET /p previousGameChoice=<%saveChoiceFile%
)
SET savedDefault=y/[n]
IF "%previousGameChoice%" == "n" (
	SET savedDefault=y/[n]
) ELSE (
	IF "%previousGameChoice%" == "y" (
		SET savedDefault=[y]/n
	) ELSE (
		ECHO Failure
	)
)

SET /p theGameChoice=Do you want to play the experimental build? (%savedDefault%): 
IF "%theGameChoice%" == "" (
	SET theGameChoice=%previousGameChoice%
)
IF "%theGameChoice%" == "n" (
	SET useExperimental=false
	(ECHO %theGameChoice%)>%saveChoiceFile%
	ECHO Stable build will be started.
) ELSE ( 
	IF "%theGameChoice%" == "y" (
		SET useExperimental=true
		(ECHO %theGameChoice%)>%saveChoiceFile%
		ECHO Experimental build will be started.
	) ELSE (
		ECHO Invalid input.
		ECHO.
		GOTO select
	)
)


SET theChoice=
SET "previousWorldChoice=-1"
IF NOT EXIST %saveWorldChoiceFile% (
	(ECHO %previousWorldChoice%)>%saveWorldChoiceFile%
) ELSE (
	SET /p previousWorldChoice=<%saveWorldChoiceFile%
)

SET savedWorldDefault=
IF "%previousWorldChoice%" == "-1" (
	SET savedWorldDefault=
) ELSE (
	SET "varTwo="&for /f "delims=0123456789" %%i in ("%previousWorldChoice%") do set varTwo=%%i
	IF defined varTwo (
		SET savedWorldDefault=
	) ELSE (
		rem echo "%previousWorldChoice% is numeric"
		IF %previousWorldChoice% LSS 1 (
			SET savedWorldDefault=
		) ELSE (
			SET "savedWorldDefault= (Default: %previousWorldChoice%)"
		)
	)
)

ECHO Please enter the number of the map you want to play.
ECHO.
ECHO The List:
SET b=%listOfRepos:,=^&ECHO.%
ECHO %b%
ECHO.
SET /p theChoice=Number%savedWorldDefault%: 

IF "%theChoice%" == "" (
	IF "%previousWorldChoice%" == "-1" (
		SET /a theChoice-=1
	) ELSE (
		SET /a theChoice=%previousWorldChoice%-1
	)
) ELSE (
	SET /a theChoice-=1
)

ECHO.

SET theChosenRepo=none

IF %theChoice% EQU 0 (
	FOR /F "tokens=*" %%l IN (%nameOfWorldlistFile%) DO SET theChosenRepo=%%l&GOTO nextline
) ELSE (
	IF %theChoice% GTR 0 (
		FOR /F "tokens=* skip=%theChoice%" %%l IN (%nameOfWorldlistFile%) DO SET theChosenRepo=%%l&GOTO nextline
	)
)


:nextline
IF "%theChosenRepo%"=="none" (
	ECHO Invalid input^^!^^!
	ECHO.
	ECHO.
	ECHO 
	GOTO select
)
ECHO.

GOTO start


:concat
SET _string=%2
SET _string=###%_string%###
SET _string=%_string:"###=%
SET _string=%_string:###"=%
SET _string=%_string:###=%
IF "%listOfRepos%"=="" (
	SET listOfRepos=%1: %_string%
) ELSE (
	SET listOfRepos=!listOfRepos!,%1: %_string%
)
::callback EXIT /B
EXIT /B





:start
SET /a theChoice+=1
(ECHO %theChoice%)>%saveWorldChoiceFile%
SET /a theChoice-=1

ECHO -----
ECHO Working with %PATHTOSAVED%\%whichSaved% ...
ECHO.
ECHO Loading files from %theChosenRepo%...
ECHO.

ECHO Deleting current sav files, keeping blueprints...
FOR /d %%a IN ("%PATHTOSAVED%\%saveGames%\*") DO IF /i NOT "%%~nxa"=="%keepDirInSaved%" RD /S /Q "%%a"
FOR %%a IN ("%PATHTOSAVED%\%saveGames%\*") DO IF /i NOT "%%~nxa"=="%keepfile%" DEL "%%a"
ECHO.

CD "%PATHTOSAVED%\%theChosenRepo%"

IF EXIST .\.git\ (
	git pull
) ELSE (
	ECHO This is not a git repository. Cannot pull.
	ECHO Trying to use local data...
)

ECHO.


IF EXIST savpackage.zip (
	SET workWithZip=y
	ECHO Working with zip file.
	IF EXIST %PATHTOSAVED%\temp\ (
		REM Do nothing.
	) ELSE (
		MKDIR %PATHTOSAVED%\temp\
	)
	
	xcopy /q/y savpackage.zip %PATHTOSAVED%\temp\
	
	CD %PATHTOSAVED%\temp
	ECHO Decompress...
	powershell.exe -command "& { Expand-Archive savpackage.zip .\ -Force; }"
	DIR /B *.sav >"%PATHTOSAVED%\Logs\%theChosenRepo%.txt"
	xcopy /q/y *.sav %PATHTOSAVED%\%whichSaved%
	CD %PATHTOSAVED%\
	RMDIR /S /Q .\temp\

) ELSE (
	ECHO Working with sav files.
	DIR /B *.sav >"%PATHTOSAVED%\Logs\%theChosenRepo%.txt"
	xcopy /q/y *.sav %PATHTOSAVED%\%whichSaved%
)


ECHO.
ECHO.


CD %PATHTOSAVED%\Logs
ECHO -----
ECHO Starting the game...
IF "%useExperimental%" == "false" (
	START com.epicgames.launcher://apps/CrabEA?action=launch
) ELSE (
	START com.epicgames.launcher://apps/CrabTest?action=launch
)

:checkIfRunning
IF EXIST search.log (
	DEL /Q search.log
) ELSE (
	REM Do nothing.
)
FOR /F %%x IN ('tasklist /NH /FI "IMAGENAME eq %exeName%"') DO (
	IF %%x == %exeName% (
	
		IF NOT DEFINED alreadyStarted (
			ECHO.
			SET alreadyStarted=y
		)
		
		ECHO Satisfactory is running^^!
		timeout /T %checkInterval% /nobreak >NUL
		GOTO checkIfRunning
		
	) ELSE (
		IF DEFINED alreadyStarted (
			ECHO.
			ECHO Satisfactory has been closed^^! Starting to synchronize^^!
			GOTO continue
		
		) ELSE (
			ECHO Satisfactory was not started yet..
			timeout /T %checkInterval% /nobreak >NUL
			GOTO checkIfRunning
		)
	)
)


:continue
IF EXIST search.log (
	REM Clear cache, program should not get bigger and bigger.
	DEL /Q search.log
) ELSE (
	REM Do nothing.
)
ECHO.
ECHO.
ECHO -----
ECHO Working with %PATHTOSAVED%\%whichSaved% ...
ECHO.
ECHO Saving files...
ECHO.

CD %PATHTOSAVED%\%saveGames%\

IF DEFINED workWithZip (
	ECHO Working with zip file.
	IF EXIST %PATHTOSAVED%\temp\ (
		REM Do nothing.
	) ELSE (
		MKDIR %PATHTOSAVED%\temp\
	)
	
	forfiles /s /m "*.sav" /c "cmd /c xcopy @path %PATHTOSAVED%\temp\ /q /y"
	
	CD %PATHTOSAVED%\temp
	ECHO Compress...
	powershell.exe -command "& { Compress-Archive *.sav savpackage.zip -CompressionLevel Optimal -Update; }"
	xcopy /q/y savpackage.zip "%PATHTOSAVED%\%theChosenRepo%\"
	CD %PATHTOSAVED%\
	RMDIR /S /Q .\temp\
	
	
) ELSE (
	ECHO Working with sav files.
	forfiles /s /m "*.sav" /c "cmd /c xcopy @path "%PATHTOSAVED%\%theChosenRepo%\" /q /y"
)



DEL "%PATHTOSAVED%\Logs\%theChosenRepo%.txt"
ECHO.
ECHO.



SET gitMessage=Spielupdate %COMPUTERNAME%
IF EXIST %PATHTOSAVED%\%gitMessageFile% (
	FOR /F %%m IN (%PATHTOSAVED%\%gitMessageFile%) DO (
		SET gitMessage=!gitMessage! %%m
	)
)


CD "%PATHTOSAVED%\%theChosenRepo%"
IF EXIST .\.git\ (
	git add .
	git commit -m "%gitMessage%"
	GOTO gitPush
	
) ELSE (
	ECHO This is not a git repository. Cannot commit and push.
	ECHO Saves are now only local data.
)

:noError
ECHO.
ECHO.
ECHO Complete. Closing...
timeout /T 10 /nobreak >NUL
EXIT

:error
ECHO.
ECHO An error occured^^! Cancelling...
PAUSE
EXIT



:ja1
:test
@ECHO OFF

xcopy %PATHTOSAVED%\backupBeforeTest %PATHTOSAVED%\%saveGames% /s /e /i
DEL /S/Q %PATHTOSAVED%\TESTTTT
RD /S/Q %PATHTOSAVED%\backupBeforeTest
xcopy %PATHTOSAVED%\%saveGames% %PATHTOSAVED%\backupBeforeTest /s /e /i

PAUSE

CD %PATHTOSAVED%\%saveGames%\
forfiles /s /m "*.sav" /c "cmd /c xcopy @path %PATHTOSAVED%\TESTTTT\&DEL /Q @path"

PAUSE
EXIT


:gitPush
cmd /E:OFF /C "git push --porcelain" > %PATHTOSAVED%\Logs\tmp.log
FOR /F "tokens=1*delims=:" %%G IN ('findstr /n "^" %PATHTOSAVED%\Logs\tmp.log') DO (
	IF %%G EQU 2 (
		SET VAR=!VAR!%%H
	)
)
DEL /Q %PATHTOSAVED%\Logs\tmp.log

IF NOT "x!VAR:%searchVal%=!"=="x%VAR%" (
	ECHO.
	ECHO Push to external repository failed^^!
	ECHO Fix the issue manually^^!^^!
	GOTO error
) ELSE GOTO noError
