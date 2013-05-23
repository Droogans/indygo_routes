#! /usr/bin/env python
"""Download all Via route files. *Really* should be a feature on the site"""

import argparse
import datetime
import os
import re
import string
import urllib2

from BeautifulSoup import BeautifulSoup as BS

SITE = 'http://www.viainfo.net/BusService/Schedules.aspx'

FS_CHARS = "-_.() %s%s" % (string.ascii_letters, string.digits)

def download_latest(destination):
    """
    Download all links pointing to a PDF of a bus schedule.
    """
    soup   = BS(urllib2.urlopen(SITE))
    attachment = re.compile('\?AttachmentId=')
    name   = re.compile('ScheduleTitle$')
    links  = [link['href'] for link in soup.findAll('a', {'href': attachment})]
    names  = [title.text for title in soup.findAll('td', {'class': name})]
    today  = datetime.date.isoformat(datetime.datetime.now())
    
    output_loc = os.path.join(destination, 'via_routes_%s' % today)
    if not os.path.exists(output_loc):
        os.makedirs(output_loc)

    parsed_url = urllib2.urlparse.urlparse(SITE)
    site_root  = '://'.join([parsed_url.scheme, parsed_url.netloc])
    for link, name in zip(links, names):
        if link.startswith('../'):
            link = link.lstrip('../')
        name = ''.join(c for c in name if c in FS_CHARS) + ".pdf"
        with open(os.path.join(output_loc, name), 'wb') as wb:
            target = urllib2.urlparse.urljoin(site_root, link)
            try:
                wb.write(urllib2.urlopen(target).read())
            except urllib2.HTTPError:
                # only a "future route" exists
                continue

if __name__ == '__main__':
    desc = "Download latest bus routes from viainfo.net"
    epil = "email issues to: droogans@gmail.com"
    parser = argparse.ArgumentParser(description=desc, epilog=epil)
    parser.add_argument("destination", type=str, help="destination")
    args = vars(parser.parse_args())
    download_latest(**args)
