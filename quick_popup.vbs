Set objArgs = WScript.Arguments
msgText = objArgs(0)
msgContent = objArgs(1)
returnValue = MsgBox(msgText, vbYesNo + vbCritical + vbDefaultButton2, msgContent)
Wscript.Quit(returnValue)