import os

import lyricsgenius
from string import punctuation
from PIL import Image
import time



def to_image(matrix,title,artist):
    title = ''.join(c for c in title if c not in "*.”/\[]:;|=,?")
    size = len(matrix)
    if size < 1000 and size >0:
        scale = 1000/size
        print(scale)
    else:
        scale = 1
    if size>0 and scale <2:
        img = Image.new('RGB', (size, size))  # create a new black image
        pixels = img.load()  # create the pixel map
        for i in range(img.size[0]):  # for every col:
            for j in range(img.size[1]):  # For every row
                if matrix[i][j]==True:
                    pixels[i, j] = (0, 0, 0) # set the colour accordingly
                else:
                    pixels[i, j] = (255, 255, 255)
        outfile = 'C:\\Users\\GMagee1\\PycharmProjects\\genius\\dump\\{1}\\{0}_{1}.jpg'.format(str(title), str(artist))
        directory = os.path.dirname(outfile)
        if not os.path.exists(directory):
            os.makedirs(directory)
        print(outfile)
        print(os.path.isfile(directory))
        if not os.path.isfile(directory):
            img.save(outfile)
    else:
        size = size*scale
        img = Image.new('RGB', (size, size))  # create a new black image
        pixels = img.load()  # create the pixel map
        for i in range(img.size[0]/scale):  # for every col:
            for j in range(img.size[1]/scale):  # For every row
                if matrix[i][j] == True:
                    pixels[i, j] = (0, 0, 0)  # set the colour accordingly
                else:
                    pixels[i, j] = (255, 255, 255)
        outfile = 'C:\\Users\\GMagee1\\PycharmProjects\\genius\\dump\\{1}\\{0}_{1}.jpg'.format(str(title), str(artist))
        directory = os.path.dirname(outfile)
        if not os.path.exists(directory):
            os.makedirs(directory)
        print(outfile)
        print(os.path.isfile(directory))
        if not os.path.isfile(directory):
            img.save(outfile)

def strip_punctuation(s):
    return ''.join(c for c in s if c not in punctuation.replace("'",""))

def process(list):
    blank = []
    for x in list:
        if "[" in x and "]" in x:
            list.remove(x)
        else:
            blank = blank + x.split(" ")
    blank_two = []
    for x in blank:
        if "-" in x:
            blank_two = blank_two+ x.split("-")
        else:
            blank_two = blank_two + [x]
    i =0
    while(i<len(blank_two)):
        if blank_two[i]=="":
            blank_two.remove("")
        else:
            blank_two[i] = strip_punctuation(blank_two[i]).lower()
            i = i+1
    return blank_two

def search_for(artist, title, api):
    search = api.search_song(title, artist)
    try:
        song = search.lyrics.splitlines()
        lyrics = process(song)
        matrix = []
        for x in range(0, len(lyrics)):
            sublist = []
            matrix.append(sublist)
            for y in range(0, len(lyrics)):
                if lyrics[x] == lyrics[y]:
                    sublist.append(True)
                else:
                    sublist.append(False)
        return to_image(matrix, title, artist)
    except AttributeError:
        print("Your Query was not found in a search. Please start the program over.")

def all_songs_by_to_txt(artist, api):
    print("fetching songs")
    path = 'C:\\Users\\GMagee1\\PycharmProjects\\genius\\dump\\{0}\\'.format(str(artist))
    if not os.path.exists(path):
        os.makedirs(path)
    directory = os.path.dirname(path)
    print(os.path.isfile(directory))
    #if not os.path.isfile(directory):
    t0 = time.time()
    songs = api.search_artist(artist).songs
    t1 = time.time()
    print(t1-t0)
    file = open(path+str(artist)+".txt","w+")
    for x in songs:
        file.write(x.title.strip('u\u200b').strip('u\U0001f409')+"\n")

def from_txt(artist,api):
    print("From txt")
    text_file = open("C:\\Users\\GMagee1\\PycharmProjects\\genius\\dump\\{0}\\{0}.txt".format(str(artist)), "r")
    list = text_file.readlines()
    for x in list:
        search_for(artist, x[:-1], api)

def main():
    api = lyricsgenius.Genius('8b9e3NKxtASuUliLIygQ0RKDES7w4JIEu4wdxfHdrNLOdutTquJtnJSDif6MAU1E')
    prompt = input("Would you like to process all of an artist's songs, or just a particular one? enter 1 for all and 0 for a particulatr song: ")
    if prompt=="0":
        while (prompt != "n"):
            artist = input("What artist would you like to search? ")
            title = input("What song title would you like to search? ")
            search_for(artist,title,api)
            prompt = input("Would you like to search again? (y/n): ")
    elif prompt=="1":
        while(prompt!="n"):
            artist = input("What artist would you like to search? ")
            path = 'C:\\Users\\GMagee1\\PycharmProjects\\genius\\dump\\{0}\\{0}.txt'.format(str(artist))
            if not os.path.isfile(path):
                all_songs_by_to_txt(artist,api)
            from_txt(artist,api)
            prompt = input("Would you like to search again? (y/n): ")

if __name__ == '__main__':
    main()


