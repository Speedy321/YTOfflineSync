# -*- coding: utf-8 -*-

import os
import sys
import fnmatch
import shutil
import json
from youtubeapi import YoutubeAPI
import hashlib
import youtube_dl

DEBUG = False
VERBOSE = True

API_KEY_FILE = "api.key"
PLAYLISTS_INFO = "playlists.json"
VIDEO_LINK = "https://www.youtube.com/watch?v="

downloadError = False

class Logger:
    def out(self, string):
        if VERBOSE:
            print("[YT Offline Sync] "+string)

    def debug(self, string):
        if DEBUG:
            print("[YT Offline Sync](debug) "+string)

    def error(self, string):
        print("[YT Offline Sync]!!ERROR!! "+string)

def addVideo(pListsFile, pList, vTitle, vId, vPos):
    vInfo = {}
    vInfo['title'] = vTitle
    vInfo['id'] = vId
    vInfo['position'] = vPos
    Logger.out(Logger, "Video added: "+json.dumps(vInfo))
    downloadVideo(pListsFile, pList, vInfo)

def checkForNewVideos(pListsFile, pList, inputList):
    for video in inputList:
        found = False
        for vid in pList['videos']:
            if vid['id'] == video['snippet']['resourceId']['videoId']:
                found = True
                Logger.out(Logger,"Video exists: "+json.dumps(vid))

        if(not found):
            addVideo(pListsFile, pList, video['snippet']['title'], video['snippet']['resourceId']['videoId'], video['snippet']['position'])

def checkForDeletedVideo(inputList, pList):
    for video in pList['videos']:
        found = False
        for vid in inputList:
            if video['id'] == vid['snippet']['resourceId']['videoId']:
                found = True
                Logger.out(Logger,"Video still exists: "+json.dumps(video))
        
        if(not found):
            deleteVideo(pList, video['title'])
            
def deleteVideo(pList, vName):
    Logger.debug(Logger, "vName : "+vName+" vPath : "+pList['localPath'])
    files = find(vName+".*", str(pList['localPath']))
    Logger.debug(Logger, "files: "+str(files))
    for f in files:
        delDir = pList['localPath'] + "\\deleted\\"
        Logger.debug(Logger, f + " -- " + delDir + os.path.basename(f))
        
        if (not os.path.exists(delDir)):
            os.makedirs(delDir)

        shutil.move(f, delDir + os.path.basename(f))
        
        vid = {}
        for tVid in pList['videos']:
            if(tVid['title'] == vName):
                vid = tVid

        pList['videos'].remove(vid)
        

    Logger.out(Logger, vName+" doesn't exist anymore and has been move to the deleted folder.")

def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

def downloadVideo(pListsFile, pList, video):
    ydlOpts = {
        'format': 'best',
        'outtmpl': pList['localPath']+"\\%(title)s.%(ext)s",
        'retries': 2
    }

    Logger.debug(Logger, str(ydlOpts))

    try:
        with youtube_dl.YoutubeDL(ydlOpts) as ydl:
            ydl.download([VIDEO_LINK + video['id']])

    except:
        Logger.error(Logger, " Failed to download, skipping: "+video['title'])
        downloadError = True
        return
    
    pList['videos'].append(video)
    updatePlaylistsFile(pListsFile)

def updatePlaylist(pListsFile, pList):
    youtube = YoutubeAPI(API_KEY)
    pageTokens = []

    testList = youtube.get_playlist_items_by_playlist_id_paginated(pList['id'], 50, None)

    i = 0
    while(testList['info']['nextPageToken'] != None):
        pageTokens.append(testList['info']['nextPageToken'])
        tempList = youtube.get_playlist_items_by_playlist_id_paginated(pList['id'], 50, pageTokens[i])
        testList['info'].update(tempList['info'])
        for element in tempList['results']:
            testList['results'].append(element)

        i+=1

    if DEBUG:
        for token in pageTokens:
            Logger.debug(Logger, "next page: " + token)

        f = open('out.json', 'w')
        f.write(json.dumps(testList))
        f.close()
    
    sha1Hash = hashlib.sha1(json.dumps(testList['results']).encode())
    sha1Hashed = sha1Hash.hexdigest()

    Logger.out(Logger,"SHA1 - " + str(sha1Hash) + " hashed: " + str(sha1Hashed))

    if (pList['sha1'] != str(sha1Hashed)):
        checkForNewVideos(pListsFile, pList, testList['results'])
        checkForDeletedVideo(testList['results'], pList)

        if (not downloadError):
            pList['sha1'] = str(sha1Hashed)
        pList['videosNumber'] = testList['info']['totalResults']
        pList['localVersion'] = pList['localVersion']+1

        Logger.out(Logger, pList['name']+" has been updated")
    else:
        Logger.out(Logger, pList['name']+" hasn't changed")
        
    return pList

def updatePlaylistsFile(pLists):
    with open(PLAYLISTS_INFO, 'w') as f:
        f.write(json.dumps(pLists, indent=2, sort_keys=True))

if __name__== "__main__":
    with open(API_KEY_FILE) as keyFile:
        API_KEY = keyFile.read()
        Logger.debug(Logger,"API: " + API_KEY)
    
    with open(PLAYLISTS_INFO, encoding="utf8") as listsFile:
        playlists = json.loads(listsFile.read())
        Logger.debug(Logger,"LISTS: " + json.dumps(playlists))

    newPLists = []

    for pList in playlists:
        newPLists.append(updatePlaylist(playlists, pList))

    updatePlaylistsFile(newPLists)