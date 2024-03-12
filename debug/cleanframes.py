import os


#delete all files in the folder "frames/smalllog_rg" with a number less than 2000

for file in os.listdir("frames/piggy2"):
    if file.endswith(".jpg"):
        if int(file[5:-4]) != 2724 and int(file[5:-4]) != 1957:
            os.remove(f"frames/piggy2/{file}")