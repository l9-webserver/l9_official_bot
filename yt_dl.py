import urllib.request, json

def getLatestID(videos: str) -> str:
    opener = urllib.request.FancyURLopener({})
    url = videos
    f = urllib.request.urlopen(url)
    blob=f.read().decode("utf-8")
    json_file=blob.split("var ytInitialData =")[1].split(";</script><link rel=\"canonical\" href=\"")[0].strip()
    dict=json.loads(json_file)
    open("milan.json", "w").writelines(json.dumps(dict, indent=4))
    videoID=dict["contents"]["twoColumnBrowseResultsRenderer"]["tabs"][1]["tabRenderer"]["content"]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"][0]["gridRenderer"]["items"][0]["gridVideoRenderer"]["videoId"]
    return videoID

