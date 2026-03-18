# https://github.com/boo-lang/boo/wiki/Invoke-Native-Methods-with-DllImport

[Skip to content](https://github.com/boo-lang/boo/wiki/Invoke-Native-Methods-with-DllImport#start-of-content)

You signed in with another tab or window. [Reload](https://github.com/boo-lang/boo/wiki/Invoke-Native-Methods-with-DllImport) to refresh your session.You signed out in another tab or window. [Reload](https://github.com/boo-lang/boo/wiki/Invoke-Native-Methods-with-DllImport) to refresh your session.You switched accounts on another tab or window. [Reload](https://github.com/boo-lang/boo/wiki/Invoke-Native-Methods-with-DllImport) to refresh your session.Dismiss alert

{{ message }}

[boo-lang](https://github.com/boo-lang)/ **[boo](https://github.com/boo-lang/boo)** Public

- [Notifications](https://github.com/login?return_to=%2Fboo-lang%2Fboo) You must be signed in to change notification settings
- [Fork\\
150](https://github.com/login?return_to=%2Fboo-lang%2Fboo)
- [Star\\
905](https://github.com/login?return_to=%2Fboo-lang%2Fboo)


# Invoke Native Methods with DllImport

[Jump to bottom](https://github.com/boo-lang/boo/wiki/Invoke-Native-Methods-with-DllImport#wiki-pages-box)

rollynoel edited this page on Jun 13, 2013Jun 13, 2013
·
[2 revisions](https://github.com/boo-lang/boo/wiki/Invoke-Native-Methods-with-DllImport/_history)

Added by dholton dholton

Here are some samples:

```
import System.Runtime.InteropServices

[DllImport("user32.dll")]
def MessageBeep(n as uint) as int:
	pass

def beep():
	MessageBeep(0)

beep()
```

Actually, a more cross-platform way to make a beep sound is to call Microsoft.VisualBasic.Interaction.Beep() (add a reference to the Microsoft.VisualBasic.dll in the GAC or do "import Microsoft.VisualBasic from Microsoft.VisualBasic"). This is supported in both .NET and Mono.

```
import System.Runtime.InteropServices

[DllImport("msvcrt.dll")]
def puts (c as string) as int:
	pass

[DllImport("msvcrt.dll")]
def _flushall () as int:
	pass

puts("testing...")
_flushall()
```

Here is another example with the EntryPoint specified as a named parameter. Useful I guess if you want to use a different name for the dll call.

```
import System.Runtime.InteropServices

[DllImport("User32.dll", EntryPoint:"MessageBox")]
def msgbox(hwnd as int, msg as string, caption as string, msgtype as int):
	pass

def msgbox(msg as string):
	msgbox(0,msg,"Message",0)

msgbox(0, "MessageDialog called", "DllImport Demo", 0)

msgbox("one more time")
```

For further information, see:

- [P/Invoke tutorial](http://msdn.microsoft.com/en-us/library/aa288468%28v=vs.71%29.aspx).
- [Creating a P/Invoke Library](http://msdn.microsoft.com/en-us/library/aa446550.aspx)

### Clone this wiki locally