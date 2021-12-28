import urllib.request
from bs4 import BeautifulSoup as bs 
import requests
from datetime import datetime as dt
import os
import re
from Zipper import zipAudios
mb=re.compile(r"([0-9]{1,3}(\.[0-9]*)?\s((MB)|(KB)))")


totalFiles=0
def getAllLinks(url,folder):
    res=requests.get(url)
    soup=bs(res.text, 'lxml')
    khatas=soup.find_all("table",cellpadding=4)
    khatas=khatas[4:-2]
    folderWithLinks={folder:[]}
    count=0 
    for file in khatas:
        try:
            title=file.find("font",size="2",color="0069c6").text
        except AttributeError:
            print("No Good. But we caught it!!")#It got the ALL the text from the drop down menu and those don't have a 'color=0069c6' attribute
            continue
        newUrl="http://www.gurmatveechar.com/"+file.find("a").get("href")
        if "mp3" in newUrl.lower():
            global totalFiles
            totalFiles+=1
            count+=1
            length=file.find_all("td",align="right")
            for td in length:
                if "mb" in td.text.lower() or "kb" in td.text.lower():
                    theMB=td.text
            title=f"{str(count).zfill(3)} ) {title}"+"???"+theMB #the last part contians the MBs of the file.
            folderWithLinks[folder].append(title)
            folderWithLinks[folder].append(newUrl)
        else:
            newFolder=title
            newFolderWithLinks=getAllLinks(newUrl,newFolder)
            if folder=="main": # the purpose og this statement is so that when we make the folders to download the files, the folders in the folder end up in the folder lol
                folderWithLinks.update(newFolderWithLinks)
            else:
                folderWithLinks[folder].append(newFolderWithLinks) 
                #ifthere is a folder in a folder, the MAIN folder will be the key 
                # and its keys are other dictionaies. The keys to ALL dictionaries are titles of folders 
                # and the base value is a list of links
                #the program will keep recusing as long as there is folder and will stop when there are
                #mp3 files
    return folderWithLinks

allMbSum=0
def downloadOrig(khatas,thePath):
    for khata in khatas:
        folderPath=thePath
        if khata!="main":
            folderPath=thePath+khata+"\\"
            os.mkdir(folderPath)
            if type(khatas[khata][0])==dict: #made this call so that it doesen't have to search through EACH file when the first is not a dict
                listOfDict=khatas[khata]
                for dictt in listOfDict:
                    try:
                        if type(dictt)==dict:  #somtimes there are folders and files in a folder so this will check for that. If not a dict, the won't recurse
                            download(dictt,folderPath)
                    except Exception as e:
                        print("error: "+e)
                continue #so the dict of dicts dosen't keep going down
        titles=[khatas[khata][i] for i in range(len(khatas[khata])) if i%2==0]
        links=[khatas[khata][i] for i in range(len(khatas[khata])) if i%2!=0]
        FolderMbs=""
        MBsum=0
        for i in titles:
            FolderMbs+=i
        for i in mb.findall(FolderMbs):
            a=i[0]
            if "kb" in a.lower():
                val=float(a[:-3])/1000
            elif "gb" in a.lower():
                val=float(a[:-3])*1000
            else:
                val=float(a[:-3])
            MBsum+=val
        global allMbSum
        allMbSum+=MBsum
        print("\n"+khata+" : ",MBsum)
        for i in range(len(links)):
            title=titles[i].split("???")[0]+".mp3"
            noNo='\/:*?"<>|' #cant name a file with any of these characters so if the title has any of these characters, the loop will replace them
            for bad in noNo:
                if bad in title:
                    title=title.replace(bad,"#")
            urllib.request.urlretrieve(links[i],f'{folderPath}{title}')
            print(f'{title} - {links[i]}')

def download(khatas,thePath):
    for khata in khatas:
        folderPath=thePath
        if khata!="main":
            folderPath=thePath+khata+"/"
            os.mkdir(folderPath)
            if type(khatas[khata][0])==dict: #made this call so that it doesen't have to search through EACH file when the first is not a dict
                listOfDict=khatas[khata]
                for dictt in listOfDict:
                    try:
                        if type(dictt)==dict:  #somtimes there are folders and files in a folder so this will check for that. If not a dict, the won't recurse
                            download(dictt,folderPath)
                    except Exception as e:
                        print("error: "+e)
                continue #so the dict of dicts dosen't keep going down
        titles=[khatas[khata][i] for i in range(len(khatas[khata])) if i%2==0]
        links=[khatas[khata][i] for i in range(len(khatas[khata])) if i%2!=0]
        FolderMbs=""
        MBsum=0
        for i in titles:
            FolderMbs+=i
        for i in mb.findall(FolderMbs):
            a=i[0]
            if "kb" in a.lower():
                val=float(a[:-3])/1000
            elif "gb" in a.lower():
                val=float(a[:-3])*1000
            else:
                val=float(a[:-3])
            MBsum+=val
        global allMbSum
        allMbSum+=MBsum
        # print("\n"+khata+" : ",MBsum)
        for i in range(len(links)):
            title=titles[i].split("???")[0]+".mp3"
            noNo='\/:*?"<>|' #cant name a file with any of these characters so if the title has any of these characters, the loop will replace them
            for bad in noNo:
                if bad in title:
                    title=title.replace(bad,"#")
            urllib.request.urlretrieve(links[i],f'{folderPath}{title}')
            print(f'{title} - {links[i]}')

def enterUrl(link):
    start=str(dt.now())

    # path="C:/Users/gians/Desktop/CS/WebDev/sikhStuff/GurmatVeecharDownloader/audios"
    path="./audios"
    if path[-1]!="/":
        path+="/"

    khatas=getAllLinks(link,'main')
    download(khatas,path)

    linkSplitLst=link.split('%2F')
    if len(linkSplitLst)==1:
        linkSplitLst=link.split('/')
    dirName=linkSplitLst[-1]+".zip"

    zipAudios(dirName)

    deleteAllAudios()

    end=str(dt.now())

    startSeconds=(int(start[11:13])*60*60)+(int(start[14:16])*60)+int(start[17:19])
    endSeconds=(int(end[11:13])*60*60)+(int(end[14:16])*60)+int(end[17:19])

    print(f"\nTotal MBs: {allMbSum}")
    print(f"Total MBs per Second :{allMbSum/(endSeconds-startSeconds)}")
    print("In total: "+str(totalFiles)+" total files\n")
    
    # print(f"Start: {start}")
    # print(f"End: {end}\n")
    print(f"Seconds: {endSeconds-startSeconds}")

def deleteAllAudios(dirToDelAll="C:/Users/gians/Desktop/CS/WebDev/sikhStuff/GurmatVeecharDownloader/audios/"):
    for thing in os.listdir(dirToDelAll):
        path=dirToDelAll+thing
        if os.path.isdir(path):
            deleteAllAudios(path+"/")
            os.rmdir(path)
        else:
            os.remove(path)
                     


# link='https://gurmatveechar.com/audio.php?q=f&f=%2FKeertan%2FBaba_Gurdev_Singh_%28Nanaksar_wale%29'
# link='https://gurmatveechar.com/audio.php?q=f&f=/Keertan/Bhai_Amrik_Singh_Zakhmi'
# enterUrl(link)
