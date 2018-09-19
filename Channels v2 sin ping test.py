import urllib.request 
import re
from operator import itemgetter
import time

list_channels_string = ""

#lists_of_channels_files = ['http://tecnotv.xyz/lista.m3u', 'http://tecnotv.xyz/singeo.m3u', 'http://tecnotv.xyz/lista2.m3u', 'http://tecnotv.xyz/esp.m3u', 'http://tecnotv.xyz/kids.m3u']
lists_of_channels_files = ['http://tecnotv.xyz/lista.m3u', 'https://www.nibbletv.info/TV-TAU.m3u']

counter = 0
functional_channels = []

ti  = time.time()
print("Loading lists...")
for list_of_channels in lists_of_channels_files:
        channels_raw = urllib.request.urlopen(list_of_channels)
        print(".", end="")

        #Extrayendo informacion de archivo
        for channel_raw in channels_raw:
#                print(channel_raw)
                channel_raw = channel_raw.decode("utf-8").replace('\n', ' ').replace('\r',' ').replace('\r\n',' ')
                list_channels_string = list_channels_string + channel_raw
        channels_raw.close()

print("\nTesting channels...")
for channel_string in re.split('#EXTINF:-1|#EXTINF:1|#EXTINF:0|EXTINF:0|#EXTINF:-0|#EXTINF: -1', list_channels_string):
        channel_data_list = re.split(' |,', channel_string)
        for channel_data in channel_data_list:
#                print(channel_data)
#                if channel_data.endswith('m3u8') or channel_data.endswith('m3u8?'):
                if '.m3u8' in channel_data:
                        print(".", end="")
#                        print(channel_data)
#                        try:                                        
#                                urllib.request.urlopen(channel_data)
                        functional_channel_data_list = channel_data_list
                        name = ""
                        counter = counter + 1
                        for functional_channel_data in functional_channel_data_list:
                                        
                                if functional_channel_data.startswith(('http', 'tvg-logo', 'group-title', 'tvg-id', 'tvg-name', 'type', 'tvg-shift', '*', 'title')) == False and functional_channel_data.endswith(('"', '*', '-')) == False:
                                        name = name + functional_channel_data + ' '
                                       
                                if functional_channel_data.startswith('tvg-logo'):
                                        try:
                                                urllib.request.urlopen(functional_channel_data[10:-1], timeout=1)
                                                logo = functional_channel_data[10:-1]
                                        except:
                                                logo = None
                                                
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
#                       print('name:', name)
#                        print('link:', link)
#                        print('logo:', logo)
                        functional_channels.append({'name': name, 'link': link, 'logo': logo})
#                        except:
#                                print("link no functional")
#                                pass
                                

values_funtional_channel = []
channels_final=[]

for functional_channel in functional_channels:
    if not functional_channel['link'] in values_funtional_channel:
        channels_final.append(functional_channel)
        values_funtional_channel.append(functional_channel['link'])

final_channels_sorted = sorted(channels_final, key=itemgetter('name'))

counter_2 = 0
print("\n")
for channel in final_channels_sorted:
        counter_2=counter_2+1
#        print('------------------------------------------------')
        print(counter_2)
        print('Name:', channel['name'])
        print('Link:', channel['link'])
        print('Logo:', channel['logo'])
        
tf =time.time()
print("Quantity: ", len(final_channels_sorted))
print("Execution time", (tf-ti)/60, 'min.')
print("process finished!!!")
