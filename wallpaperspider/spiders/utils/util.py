import re


def from_url_get_id(url):

    result = re.match("https://alpha\.wallhaven\.cc/wallpaper/([0-9]+)", url)
    if result:
        return result.group(1)
    else:
        return None

    pass