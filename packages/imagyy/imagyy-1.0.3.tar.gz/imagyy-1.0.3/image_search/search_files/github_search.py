__author__ = 'tusharmakkar08'

try:
    from urllib.parse import urlparse, urlencode
    from urllib.request import urlopen, Request, urlretrieve
    from urllib.error import HTTPError
except ImportError:
    from urlparse import urlparse
    from urllib import urlencode
    from urllib2 import urlopen, Request, HTTPError
    from urllib import urlretrieve

import re
import os

URL_REGEX = r'https?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
LINK_END = '.githubusercontent.com'
DEFAULT_DIRECTORY = os.path.join(os.getcwd(), "github_images")


def github_image_downloader(url, directory_to_download=None):
    """
    Downloads Github images in a particular directory
    :param url: Github username url eg: https://github.com/tusharmakkar08
    :param directory_to_download: Directory where files will be downloaded ,
    if this is none then files downloaded to default directory
    :return:
    """
    response = urlopen(url)
    html = response.read().decode('utf-8')
    image_links = {link for link in re.findall(URL_REGEX, html) if LINK_END in link}
    user_name = url.split(".com/")[1].strip("/")
    download_directory = os.path.join(DEFAULT_DIRECTORY, directory_to_download) if directory_to_download else \
        os.path.join(DEFAULT_DIRECTORY, user_name)
    if not os.path.exists(download_directory):
        os.makedirs(download_directory)
    for index, image_link in enumerate(image_links):
        download_location = os.path.join(download_directory, user_name + "_" + str(index) + ".jpg")
        urlretrieve(image_link, download_location)

