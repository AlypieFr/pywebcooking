import re
import unicodedata


class Functions:

    @staticmethod
    def remove_accents(input_str):
        nfkd_form = unicodedata.normalize('NFKD', input_str)
        return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

    @staticmethod
    def insert_picture(item: str, author_url: str):
        pict_iter = re.finditer(r"\[PICT:(\w+):(\d+):(\d+)(:center)?:([^]]+)]", item)
        for pict in pict_iter:
            bal_img = pict.group(0)
            printable = pict.group(1)
            width = pict.group(2)
            height = pict.group(3)
            center = pict.group(4) is not None
            img = pict.group(5)
            url = "/media/" + author_url + "/" + img
            img_html = "<a href=\"" + url + "\" data-lightbox='illustration'><img src=\"" + url + "\" width=\"" + width + \
                       "\" alt=\"Illustration\" class=\""
            if printable == "print-only":
                img_html += "print-only "
            if printable == "no-print":
                img_html += "no-print "
            if center:
                img_html += "center "
            img_html += "autoresize\"/></a>"
            item = item.replace(bal_img, img_html)
        return item

    @staticmethod
    def replace_files(text: str, files_replace: dict):
        pict_iter = re.finditer(r"\[PICT:(\w+):(\d+):(\d+)(:center)?:([^]]+)]", text)
        for pict in pict_iter:
            img = pict.group(5)
            if img in files_replace:
                old_pict_bal = pict.group(0)
                new_pict_bal = old_pict_bal.replace(img, files_replace[img])
                text = text.replace(old_pict_bal, new_pict_bal)
        return text
