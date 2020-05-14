amp_urls = open('amp_urls.txt').readlines()
cdn_amp_urls = open('cdn_amp_urls.txt').readlines()
non_amp_urls = open('original_urls.txt').readlines()


amp_url_file = open('amp_urls.txt','w')
cdn_amp_url_file = open('cdn_amp_urls.txt','w')
non_amp_url_file = open('original_urls.txt','w')


def write_to_all(line):
    amp_url_file.write(line)
    cdn_amp_url_file.write(line)
    non_amp_url_file.write(line)

urls = set()
for i, url in enumerate(non_amp_urls):

    if url not in urls:
        urls.add(url)
        write_to_all(url)