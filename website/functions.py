import re

class Functions:

    @staticmethod
    def insert_picture(item: str, author_url: str):
        pict = re.search(r"\[PICT:(\w+):(\d+):(\d+)(:center)?:([^]]+)]", item)
        if pict:
            bal_img = pict.group(0)
            printable = pict.group(1)
            width = pict.group(2)
            height = pict.group(3)
            center = pict.group(4) is not None
            img = pict.group(5)
            url = "/media/" + author_url + "/" + img
            img_html = "<a href=\"" + url + "\"><img src=\"" + url + "\" width=\"" + width + "px\" class=\""
            if printable == "print-only":
                img_html += "print-only "
            if printable == "no-print":
                img_html += "no-print "
            if center:
                img_html += "center "
            img_html += "autoresize\"/></a>"
            item = item.replace(bal_img, img_html)
        return item
