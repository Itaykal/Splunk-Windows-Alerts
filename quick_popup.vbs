Set objArgs = WScript.Arguments
msgText = objArgs(0)
msgContent = objArgs(1)
box = MsgBox(msgText, 1, msgContent)