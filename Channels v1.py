import urllib.request 
import re

list_string_channel = ""
filenames= ['http://tecnotv.xyz/lista.m3u', 'http://tecnotv.xyz/tvmex.m3u', 'http://tecnotv.xyz/singeo.m3u']
funcional_channels = []

c = 0

print("Loading of resources")
for fname in filenames:
        data_m3u = urllib.request.urlopen(fname)

        #Extrayendo informacion de archivo
        for line in data_m3u:
                line = line.decode("utf-8").replace('\n', ' ').replace('\n', '  ').replace('\n', '   ') 
                list_string_channel = list_string_channel + line
        data_m3u.close()


print("testeing")


#Separando canales del string gigante
for string_channel in re.split('#EXTINF:-1|#EXTINF:1|#EXTINF:0', list_string_channel):
        data_channel = re.split(' |,', string_channel)
        for data in data_channel:
                if data.endswith('m3u8'):
                        try:
                                urllib.request.urlopen(data, timeout=1)
                                funcional_channels.append(data_channel)
                                print("yes")
                        except:
                                pass

        #for de string funcionales
for data_functional_channel in funcional_channels:
        name = ''
        c=c+1
        for data_functional in data_functional_channel:
                        
                if data_functional.startswith('http') == False and data_functional.startswith('tvg-logo') == False and data_functional.startswith('group-title') == False and data_functional.startswith('tvg-id') == False and data_functional.startswith('tvg-name') == False and data_functional.startswith('type') == False:
                        name = name + data_functional + ' '
                if data_functional.startswith('tvg-logo'):
                        try:
                                urllib.request.urlopen(data_functional[10:-1], timeout=1)
                                logo = data_functional[10:-1]
                                c3=c3+1
                        except:
                                logo = None
                        
                if data_functional.startswith('http'):
                        link = data_functional

        print(c)
        print('name:', name[1:])
        print('link:', link)
        print('logo:', logo)
                
print("process finished!!!")                
