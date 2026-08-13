with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    lines = f.readlines()

new_lines = []
for idx, line in enumerate(lines):
    if idx + 1 == 362 and line.strip() == ")":
        continue # skip
    new_lines.append(line)

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.writelines(new_lines)
