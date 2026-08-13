import re

with open('/app/applet/app/src/main/java/com/example/data/QuranData.kt', 'r') as f:
    code = f.read()

old = '.replace("[أإآ]".toRegex(), "ا")'
new = '.replace("[أإآٱ]".toRegex(), "ا")'
code = code.replace(old, new)

with open('/app/applet/app/src/main/java/com/example/data/QuranData.kt', 'w') as f:
    f.write(code)
