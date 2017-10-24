import urllib


def open_url(url):
    handler = urllib.urlopen(url)
    file_handler = open("content.txt", "wb")
    while 1:
        data = handler.read(1024)
        if not data:
            break
        file_handler.write(data)

    file_handler.close()
    handler.close()

if __name__ == '__main__':
    open_url("http://www.jb51.net/article/65167.htm")
