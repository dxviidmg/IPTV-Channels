from urllib.request import urlopen 
import re
from operator import itemgetter
from time import time
from datetime import datetime, timedelta
import os
import csv
from collections import OrderedDict

#lists_of_channels_files2 = ['http://tecnotv.xyz/lista.m3u', 'http://tecnotv.xyz/singeo.m3u', 'http://tecnotv.xyz/lista2.m3u', 'http://tecnotv.xyz/esp.m3u', 'http://tecnotv.xyz/kids.m3u']
#lists_of_channels_files = ['http://tecnotv.xyz/lista.m3u', 'https://www.nibbletv.info/TV-TAU.m3u', 'https://pastebin.com/raw/P7BEGxd0']
#lists_of_channels_files = ['https://pastebin.com/raw/P7BEGxd0']
#lists_of_channels_files = ['http://tecnotv.xyz/lista.m3u', 'https://pastebin.com/raw/P7BEGxd0']

def check_connection(url):
        try:
                url_open  = urlopen(url, timeout=10)
                code = url_open.getcode()
                content_type = url_open.getheader('Content-Type')
                if content_type == "video/mp4":
                        print("is video")
                        return False
                return True
        except Exception as e:
                print(e)
                return False
                                
def get_functional_urls_lists_channels():
        print("Opening file and checking channels lists urls...")

        functional_channel_lists_urls = []

        file_with_channel_lists_urls = open("channel_list.txt", "r")
        for channel_list_url in file_with_channel_lists_urls:
#        print(channel_list_url)
                channel_list_url = channel_list_url[:-1]
                if not channel_list_url.startswith(('#', ' ')):
                        if check_connection(channel_list_url) is True and not channel_list_url in functional_channel_lists_urls:
                                print("Successful connection:", channel_list_url)
                                functional_channel_lists_urls.append(channel_list_url)
                        else:
                                print("Unsuccessful connection or repeated url:", channel_list_url)

        list(OrderedDict.fromkeys(functional_channel_lists_urls))
        return functional_channel_lists_urls

def get_dirty_channels(channel_lists_urls):
        print("Loading lists...")

        dirty_channels=[]
        pieces_channels_aux = []

        for channel_list_url in channel_lists_urls:
#                print(channel_list_url)
                channel_list_url_content = urlopen(channel_list_url)
#                print(".", end="")
                for content in channel_list_url_content:
                        content = content.decode("utf-8").replace('\n', ' ').replace('\r',' ').replace('\r\n',' ').replace(',',' ').replace('|',' ')
                        if not content.isspace():
                                pieces_channels_aux.append(content)
                                
        print("Finding possibles channels...")
        for i, pieces_channels in enumerate(pieces_channels_aux):
#                print(pieces_channels)
                if pieces_channels.startswith(("#EXT")):
#                        print(pieces_channels)
                        accum_pieces_channels_2 = ""
                        for i2, pieces_channels_2 in enumerate(pieces_channels_aux[i+1:]):
#                                print(i2)
                                if not pieces_channels_2.startswith("#EXT"):
#                                        print(pieces_channels_2)
                                        accum_pieces_channels_2 = accum_pieces_channels_2 + pieces_channels_2
                                else:
                                        break
                        dirty_channel = pieces_channels + accum_pieces_channels_2
                        if dirty_channel.count('#EXT') == 1:
                                dirty_channel = dirty_channel.split(" ")
#                                print(dirty_channel)
                                dirty_channels.append(dirty_channel)

        return dirty_channels

def get_clean_channels(dirty_channels):
        print("Finding and cleaning channels...")

        channels_aux = []
        channels = []
        aux = []

        prefixes = ['#', '-', '24/', 'group-', 'tvg-', '(', 'title', 'type', '=', 'http', 'X-F', '_', '*', '[', 'www', '0/', 'EXT']
        suffixes = ['"', ')', ']', ';']
        
        for dirty_channel in dirty_channels:
#                print(dirty_channel)
                for channel_data in dirty_channel:
                        if '.m3u8' in channel_data and channel_data.startswith('http'):
#                                print(".", end="")
                                channel_url = channel_data
                                channel_name = ""
                                for channel_data_2 in dirty_channel:
                                        if channel_data_2 != channel_url and not channel_data_2.startswith(tuple(prefixes)) and not channel_data_2.endswith(tuple(suffixes)) and len(channel_data_2) < 50:
                                                channel_name = channel_name + channel_data_2 + " "
#                                print(channel_name)
                                if ':' in channel_name:
                                        new_begging = channel_name.index(':') + 1
#                                        print(new_begging, channel_name[new_begging:])
                                        channel_name = channel_name[new_begging:]
                                channel_name = " ".join(channel_name.split()).upper()

                                if len(channel_name) > 35:
                                        channel_name = channel_name[:35]
                                        
                                channel = {'name': channel_name, 'url': channel_url}
#                                print(channel)
                                channels_aux.append(channel)

        # Show channel names
#        channels_aux.sort(key=itemgetter('name'))
#        for test in channels_aux:
#                if "micine" in test['url']:
#                        print(test)

        print("Deleting channels repeated...")
        channels_aux.sort(key=itemgetter('url', 'name'), reverse=True)
        for channel_aux in channels_aux:
#                print(channel_aux)
                if not channel_aux['url'] in aux:
                        channels.append(channel_aux)
#                        print(channel_aux)
                        aux.append(channel_aux['url'])

        channels.sort(key=itemgetter('name', 'url'))

        #Show clean channel
#        for channel in channels:
#               if "micine" in channel['url']:
#                        print(channel)

        return channels

def get_channels_ping_test(channels):
        print("Testing channels...")
        
        channels_ping_test = []
        porcentual_point = 100/len(channels)
        
        for i, channel_to_test in enumerate(channels):
#                print(i)
#                print(channel_to_test)
#                print(".", end="")

                if i%10 == 0:
                        percentage = i*porcentual_point
                        percentage = str(percentage)
                        print(percentage[:5] + '%')
                ping_test = check_connection(channel_to_test['url'])
#                ping_test2 = check_connection(channel_to_test['url'])

#                print(ping_test, ping_test2)
                if ping_test == True:# and ping_test2 == True:
#                        print(ping_test, ping_test_2)
                        print(str(channel_to_test))
                        channels_ping_test.append(channel_to_test)
#                else:
#                        print(".", end="")
        return channels_ping_test

def export_to_csv(channels, option_ping_test):
        now = datetime.now()
        today = now.strftime('%B %d, %Y')
        current_time = now.strftime('%H-%M-%S')
        out = ""

        if option_ping_test != "1":
                out = "out"
                
        csv_name = 'Channels with' + out + ' ping test to ' + today + ' at '+current_time + '.csv'
        
        with open(csv_name, 'w', newline='', encoding="utf-8") as csvfile:
                fieldnames = ['name', 'url']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()     
                writer.writerows(channels)

def start():
        option_ping_test = input("If you want to do ping tests, press 1: ")
        
        if check_connection("https://www.google.com/") == True:
                start_datetime = datetime.now()
                print("Start datetime:", str(start_datetime)[:19])
                try:
                        urls_lists_channels = get_functional_urls_lists_channels()
                        dirty_channels = get_dirty_channels(urls_lists_channels)
                        print("Number of possible channels found:", len(dirty_channels))
                        channels = get_clean_channels(dirty_channels)
                        print("Number channels with unique url:", len(channels))
                        if option_ping_test == "1":
                                channels = get_channels_ping_test(channels)
                                print("Number of channels that passed the ping test:", len(channels))
                        export_to_csv(channels, option_ping_test)
                        end_datetime = datetime.now()
                        run_time = str((end_datetime - start_datetime))
                        print("End datetime:", str(start_datetime)[:19])
                        print('Run time', run_time[:7])
                except:
                        print("channel_list.txt not found")
        else:
                print("Error, check your internet connection")
        os.system("pause")
                
start()
