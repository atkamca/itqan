with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    lines = f.readlines()

lines.insert(359, "                        )\n")

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.writelines(lines)
