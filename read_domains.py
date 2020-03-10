import json

alexa_file = open("alexa-top-1m.csv")
outfile_name = 1
urls_list = list()

for n, line in enumerate(alexa_file):
    url = "https://www."+line.split(",")[1].strip()
    n = n+1

    urls_list.append(url)

    #print(url, n, n % 50)

    if n % 50 == 0:
        urls_dict = dict()
        urls_dict["urls"] = urls_list
        outfile = open("./urls/"+str(outfile_name)+".txt", 'w')
        outfile.write(json.dumps(urls_dict, indent=4))
        outfile_name += 1
        urls_list = []

    if n == 7500:
        exit()