with open('/app/applet/app/src/main/java/com/example/ui/WordAnalysisBottomSheet.kt', 'r') as f:
    bot_code = f.read()

bot_code = bot_code.replace("@Composable\n@OptIn(ExperimentalLayoutApi::class)\n@Composable", "@OptIn(ExperimentalLayoutApi::class)\n@Composable")
with open('/app/applet/app/src/main/java/com/example/ui/WordAnalysisBottomSheet.kt', 'w') as f:
    f.write(bot_code)

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    main_code = f.readlines()

# find if there is an extra bracket around 362..368
# Let's print out the lines
for i in range(355, 370):
    pass
