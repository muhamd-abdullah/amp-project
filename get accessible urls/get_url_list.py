amp_dicts = open('Ampdicts.txt') 
amp_url_file = open('amp_urls.txt','w')
cdn_amp_url_file = open('cdn_amp_urls.txt','w')
non_amp_url_file = open('original_urls.txt','w')
overall_dict = dict()

amp_url = ""
orig_url = ""
cdn_url = ""

import urllib.request

check_url = True
for line in amp_dicts:

    if "ampUrl" in line:
        amp_url = line.split('"')[3]
        try:
            print("amp: ",amp_url,urllib.request.urlopen(amp_url).getcode())
        except:
            print("AMP Inaccessible URL=", amp_url)
            amp_url = ""
            check_url = False
            continue
        #print("AMP=",amp_url)

    if "originalUrl" in line:
        if check_url == False:
            continue

        orig_url = line.split('"')[3]

        try:
            print("original: ",orig_url,urllib.request.urlopen(orig_url).getcode())
        except:
            print("ORIGINAL Inaccessible URL=", orig_url)
            orig_url = ""
            continue
        #print("ORIGINAL=",orig_url)

    if "cdnAmpUrl" in line:
        cdn_url = line.split('"')[3]
        check_url = True
        #print("CDN=",cdn_url)

    if amp_url and orig_url and cdn_url:
        overall_dict[orig_url] = {"amp":amp_url,"cdn":cdn_url}
        
        amp_url_file.write(amp_url+"\n")
        cdn_amp_url_file.write(cdn_url+"\n")
        non_amp_url_file.write(orig_url+"\n")
        
        #print(overall_dict[orig_url])
        
        amp_url = ""
        orig_url = ""
        cdn_url = ""
        
        #exit()