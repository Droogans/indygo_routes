#! /usr/bin/env python
"""Download all IndyGo route files. *Really* should be a feature on the site"""

import argparse
import datetime
import os
import re
import urllib2

from BeautifulSoup import BeautifulSoup as BS

SITE = 'http://indygo.net/pages/local-service-fixed-routes'

def download_latest(destination, filetype="PDF"):
    """Download all links ending in `.{filetype}` to `destination`
    filetype='XLS' is another option for download"""
    soup   = BS(urllib2.urlopen(SITE))
    search = re.compile('.{}$'.format(filetype.lower()))
    links  = [link['href'] for link in soup.findAll('a', {'href': search})]
    today  = datetime.date.isoformat(datetime.datetime.now())
    
    output_loc = os.path.join(destination, 'indygo_routes_%s' % today)
    if not os.path.exists(output_loc):
        os.makedirs(output_loc)

    parsed_url = urllib2.urlparse.urlparse(SITE)
    site_root  = '://'.join([parsed_url.scheme, parsed_url.netloc])
    for link in links:
        with open(os.path.join(output_loc, link.split('/')[-1]), 'wb') as wb:
            target = urllib2.urlparse.urljoin(site_root, link)
            wb.write(urllib2.urlopen(target).read())

if __name__ == '__main__':
    desc = "Download latest bus routes from indygo.net"
    epil = "email issues to: droogans@gmail.com"
    parser = argparse.ArgumentParser(description=desc, epilog=epil)
    parser.add_argument("destination", type=str, help="destination")
    parser.add_argument("-t", dest="filetype", required=False,
                        type=str, default="PDF", help="filetype")
    args = vars(parser.parse_args())
    download_latest(**args)