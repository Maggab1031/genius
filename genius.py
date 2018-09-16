import os
import lyricsgenius
from string import punctuation
from PIL import Image
import time




def my_converter(mini, maxi, val):
    minimum, maximum = float(mini), float(maxi)
    ratio = 2 * (val - minimum) / (maximum - minimum)
    b = int(max(0, 255 * (1 - ratio)))
    r = int(max(0, 255 * (ratio - 1)))
    g = 255 - b - r
    return r, g, b

def grayscale(min,max, value):
    minimum, maximum = float(min), float(max)
    dif = min-max
    gradient = dif/255
    dif_two = value-min
    val = dif_two/gradient
    return val


def get_images(artist_name,size):
    base = os.getcwd()
    path = os.getcwd()+"\\dump\\"+artist_name
    os.chdir(path)
    files = os.listdir()
    list = []
    for file in files:
        if file[-4:]==".jpg":
            list.append(file)
    images_to_heatmap(list,size,artist_name)
    os.chdir(base)


def images_to_heatmap(images,size,artist):
    list = []
    for i in range(size):
        sublist = []
        for j in range(size):
            sublist.append(0)
        list.append(sublist)
    maximum = 0
    minimum = 255
    for file in images:
        img = Image.open(file)
        pixels = img.resize((size, size)).convert("1").load()
        for i in range(img.size[0]-1):
            for j in range(img.size[1]-1):
                list[i][j] = list[i][j] + pixels[i,j]
                if list[i][j] > maximum:
                    maximum = list[i][j]
                    print(maximum)
        img.close()
    for i in range(len(list)):
        for j in range(len(list)):
            if list[i][j]<minimum:
                minimum = list[i][j]
    img = Image.new('1', (size, size))  # create a new black image
    pixels = img.load()  # create the pixel map
    for i in range(img.size[0]):  # for every col:
        for j in range(img.size[1]):  # For every row
            val = list[i][j]
            print(val)
            print(minimum)
            print(maximum)
            pixels[i, j] = my_converter(minimum, maximum, val)
    outfile = '{0}\\megafile_of_all_songs_{1}.jpg'.format(os.getcwd(),str(artist))
    directory = os.path.dirname(outfile)
    if not os.path.exists(directory):
        os.makedirs(directory)
    img = img.resize((2000, 2000))
    img.save(outfile)


def to_image(matrix,title,artist):
    title = ''.join(c for c in title if c not in "*.”/\[]:;|=,?").replace('"','')
    size = len(matrix)
    if size<1:
        None
    img = Image.new('RGB', (size, size))  # create a new black image
    pixels = img.load()  # create the pixel map
    for i in range(img.size[0]):  # for every col:
        for j in range(img.size[1]):  # For every row
            if matrix[i][j]==True:
                pixels[i, j] = (0, 0, 0) # set the colour accordingly
            else:
                pixels[i, j] = (255, 255, 255)
    outfile = os.getcwd()+ '\\dump\\{1}\\{0}_{1}.jpg'.format(str(title), str(artist))
    directory = os.path.dirname(outfile)
    if not os.path.exists(directory):
        os.makedirs(directory)
    img = img.resize((2000,2000)).convert("1")
    img.save(outfile)


def strip_punctuation(s):
    return ''.join(c for c in s if c not in punctuation.replace("'",""))

def process(list):
    blank = []
    for x in list:
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
    search = api.search_song(title, artist,remove_section_headers=True)
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
    path = os.getcwd()+'\\dump\\{0}\\'.format(str(artist))
    if not os.path.exists(path):
        os.makedirs(path)
    t0 = time.time()
    songs = api.search_artist(artist).songs
    t1 = time.time()
    print("Average search time per song from artist search: "+str((t1-t0)/len(songs)))
    file = open(path+str(artist)+".txt","w+")
    for x in songs:
        title_proper = ''.join([i if ord(i) < 128 else ' ' for i in x.title.strip('u\u200b')])
        file.write(title_proper+"\n")

def from_txt(artist,api):
    print("From txt")
    text_file = open(os.getcwd() + "\\dump\\{0}\\{0}.txt".format(str(artist)), "r")
    list = text_file.readlines()
    t0 = time.time()
    for x in list:
        search_for(artist, x[:-1], api)
    t1 = time.time()
    print("Average time per song from text: "+str((t1-t0)/len(list)))



def main():
    size = 2000
    api = lyricsgenius.Genius('8b9e3NKxtASuUliLIygQ0RKDES7w4JIEu4wdxfHdrNLOdutTquJtnJSDif6MAU1E')
    dir = os.getcwd()
    prompt = input("Would you like to process all of an artist's songs, or just a particular one? enter 1 for all and 0 for a particular song: ")
    if prompt=="0":
        while (prompt != "n"):
            artist = input("What artist would you like to search? ")
            #if input("Would you like to make a heatmap? (y/n): ")=="y":
                #get_images(artist, size)
            title = input("What song title would you like to search? ")
            search_for(artist,title,api)
            prompt = input("Would you like to search again? (y/n): ")
    elif prompt=="1":
        while(prompt!="n"):
            artist = input("What artist would you like to search? ")
            path = dir + '\\dump\\{0}\\{0}.txt'.format(str(artist))
            if not os.path.isfile(path):
                all_songs_by_to_txt(artist,api)
            if input("Load from file? (y/n): ")=="y":
                from_txt(artist,api)
            all_songs_by_to_txt(artist, api)
            if input("Would you like to make a heatmap? (y/n): ")=="y":
                get_images(artist, size)
            prompt = input("Would you like to search again? (y/n): ")

if __name__ == '__main__':
    main()


