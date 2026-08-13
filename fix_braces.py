with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    if i+1 in [360, 362]:
        continue
    new_lines.append(line)

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.writelines(new_lines)
