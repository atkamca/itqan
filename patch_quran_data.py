import re

with open('/app/applet/app/src/main/java/com/example/data/QuranData.kt', 'r') as f:
    code = f.read()

old_regex = 'return text.replace(Regex("[\\\\u0617-\\\\u061A\\\\u064B-\\\\u0652\\\\u0670]"), "")'
new_regex = 'return text.replace(Regex("[\\\\u0610-\\\\u061A\\\\u064B-\\\\u065F\\\\u0670\\\\u06D6-\\\\u06ED]"), "")'
code = code.replace(old_regex, new_regex)

with open('/app/applet/app/src/main/java/com/example/data/QuranData.kt', 'w') as f:
    f.write(code)
print("Replaced successfully")
