import os


for j in range (1,6):
        path = "/home/sfilatov96/live_dataset/%s/" % j

        listOfFiles = os.listdir(path)

        countOfFiles = len(listOfFiles)

        print("Всего файлов : %s" % countOfFiles)

        os.chdir(path)

        for i in range(0, countOfFiles):
            os.rename(path+listOfFiles[i], str(j) + "_" + str(i+1)+'.jpg')