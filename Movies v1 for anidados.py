import urllib.request 
import re
import requests

list_movies_string = ""
lists_of_movies_files = ['http://tecnotv.xyz/peliculas.m3u']
funcional_movies = []
counter = 0

print("Loading lists...")
for list_of_movies in lists_of_movies_files:
        if list_of_movies.endswith('m3u'):
                movies_raw = urllib.request.urlopen(list_of_movies)
                
        #Extrayendo informacion de archivo
        for movie_raw in movies_raw:
                movie_raw = movie_raw.decode("utf-8").replace('\n', ' ').replace('\n', '  ').replace('\n', '   ') 
                list_movies_string = list_movies_string + movie_raw
        movies_raw.close()

print("Testing movies")
for movie_string in re.split('#EXTINF:-1|#EXTINF:1|#EXTINF:0|#EXTINF-0|#EXTINF-1', list_movies_string):
        movie_data_list = re.split(' |,', movie_string)
        for movie_data in movie_data_list:
                if movie_data.endswith('mp4') or movie_data.endswith('mkv'):
                        try:
                                urllib.request.urlopen(movie_data, timeout=1)
                                functional_movie_data_list = movie_data_list
                                name = ""
                                counter = counter + 1
                                for functional_movie_data in functional_movie_data_list:
                                        if functional_movie_data.startswith('http') == False and functional_movie_data .startswith('tvg-logo') == False and functional_movie_data.startswith('group-title') == False and functional_movie_data.startswith('tvg-id') == False and functional_movie_data.startswith('tvg-name') == False and functional_movie_data.startswith('type') == False:
                                                name = name + functional_movie_data + ' '

                                        if functional_movie_data.startswith('tvg-logo'):
                                                try:
                                                        urllib.request.urlopen(functional_movie_data[10:-1], timeout=1)
                                                        logo = functional_movie_data[10:-1]
                                                except:
                                                        logo = None
                                                        
                                        if functional_movie_data.startswith('http'):
                                                link = functional_movie_data

                                print(counter)
                                print('name:', name)
                                print('link:', link)
                                print('logo:', logo)

                                
                        except:
                                pass
print("process finished!!!")
