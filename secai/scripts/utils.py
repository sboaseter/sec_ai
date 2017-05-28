def replace_trash(unicode_string):
    for i in range(0, len(unicode_string)):
        try:
            unicode_string[i].encode("ascii")
        except:
            #means it's non-ASCII
            try:
                unicode_string=unicode_string[i].replace(" ") #replacin
            except:
                pass
    return unicode_string

