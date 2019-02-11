from urllib.request import urlopen 
import re
from operator import itemgetter
import time
from datetime import datetime
import os
list_channels_string = ""

#lists_of_channels_files2 = ['http://tecnotv.xyz/lista.m3u', 'http://tecnotv.xyz/singeo.m3u', 'http://tecnotv.xyz/lista2.m3u', 'http://tecnotv.xyz/esp.m3u', 'http://tecnotv.xyz/kids.m3u']
#lists_of_channels_files = ['http://tecnotv.xyz/lista.m3u', 'https://www.nibbletv.info/TV-TAU.m3u', 'https://pastebin.com/raw/P7BEGxd0']
#lists_of_channels_files = ['https://pastebin.com/raw/P7BEGxd0']
#lists_of_channels_files = ['http://tecnotv.xyz/lista.m3u', 'https://pastebin.com/raw/P7BEGxd0']

counter = 0
functional_channels = []

ti  = time.time()
print("Loading lists...")

def get_list_channels():
        channels_string = [1]
        list_functional_channels_url = []
        channel_list_urls = open("channel_list.txt", "r")
        for channel_list_url in channel_list_urls:
#        print(url)
                if channel_list_url.startswith('#') is False:
#                print(url)
                        try:
                                list_url_content = urlopen(channel_list_url)
                                for channel_list_line in list_url_content:
                                        channel_list_line = channel_list_line.decode("utf-8").replace('\n', ' ').replace('\r',' ').replace('\r\n',' ')
#                                        print(channel_list_line)
#                                        channels_string=channels_string+channel_list_line
                                        
                                        list_functional_channels_url.append(channel_list_line)
                                print("successful connection:", channel_list_url)
                        except:
                                pass
                                print("unsuccessful connection:", channel_list_url)

        print(channels_string)
        print(list_functional_channels_url)

get_list_channels()
"""
for list_of_channels in lists_of_channels_files:
        channels_raw = urlopen(list_of_channels)
#        print(".", end="")

        #Extrayendo informacion de archivo
        for channel_raw in channels_raw:
#                print(channel_raw)
                channel_raw = channel_raw.decode("utf-8").replace('\n', ' ').replace('\r',' ').replace('\r\n',' ')
                list_channels_string = list_channels_string + channel_raw
        channels_raw.close()
#print(list_channels_string)

print("\nFinding channels...")
for channel_string in re.split('#EXTINF:-1|#EXTINF:1|#EXTINF:0|EXTINF:0|#EXTINF:-0|#EXTINF: -1|#EXTINF:.1', list_channels_string):
        channel_data_list = re.split(' |,', channel_string)
        for channel_data in channel_data_list:
#                print(channel_data)
                if '.m3u8' in channel_data:
                        print(".", end="")
                        functional_channel_data_list = channel_data_list
                        name = ""
                        counter = counter + 1
                        for functional_channel_data in functional_channel_data_list:
                                        
                                if functional_channel_data.startswith(('http', 'tvg-logo', 'group-title', 'tvg-id', 'tvg-name', 'type', 'tvg-shift', '*', 'title')) == False and functional_channel_data.endswith(('"', '*', '-')) == False:
                                        name = name + functional_channel_data + ' '
                                                
                                if functional_channel_data.startswith('http'):
                                        link = functional_channel_data

                        space_counter = 0
                        for space in name:
                                if space != " ":
                                        break;
                                else:
                                        space_counter = space_counter + 1
                        name = name[space_counter:-2]
                        
#                        print(counter)
#                        print('name:', name)
#                        print('link:', link)
                        functional_channels.append({'name': name, 'link': link})
                                

values_funtional_channel = []
channels_final=[]

for functional_channel in functional_channels:
    if not functional_channel['link'] in values_funtional_channel:
        channels_final.append(functional_channel)
        values_funtional_channel.append(functional_channel['link'])

final_channels_sorted = sorted(channels_final, key=itemgetter('name', 'link'))

counter_2 = 0
print("\n")

date_string = datetime.strftime(datetime.now(), '%d-%m-%Y-%H-%M-%S')
f= open("Channels of " + date_string + ".txt","w+")

for channel in final_channels_sorted:
        counter_2=counter_2+1
#        print('------------------------------------------------')
#        print(counter_2)
#        print('Name:', channel['name'])
#        print('Link:', channel['link'])
        f.write("Number: %s\r" % counter_2)
        f.write("Name: %s\r" % channel['name'])
        f.write("Link: %s\r" % channel['link'])
f.close()

tf =time.time()
print("Quantity: ", len(final_channels_sorted))
print("Execution time", (tf-ti)/60, 'min.')
os.system("pause")
"""
