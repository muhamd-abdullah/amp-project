import random

orig_urls = open('original_urls.txt').readlines()
amp_urls = open('amp_urls.txt').readlines()
cdn_urls = open('cdn_amp_urls.txt').readlines()

orig_urls_random_25 = random.sample(orig_urls, 25)
open('orig_urls_25.txt','w').writelines(orig_urls_random_25)

# creates original url to amp, cdn url mapping
overall_dict = dict()
for i, orig_url in enumerate(orig_urls):
    overall_dict[orig_url] = {"amp":amp_urls[i],"cdn":cdn_urls[i]} 

amp_urls_random_25 = [overall_dict[orig_url]["amp"]  for orig_url in orig_urls_random_25]
open('amp_urls_25.txt','w').writelines(amp_urls_random_25)

cdn_urls_random_25 = [overall_dict[orig_url]["cdn"]  for orig_url in orig_urls_random_25]
open('cdn_amp_urls_25.txt','w').writelines(cdn_urls_random_25)




