"""This input filter will filter out certain blog posts based on the <category>
element.

This is not totally dissimilar to the function of the xpath_sifter.py plugin.
The main difference are that this one uses minidom instead of xpath and instead
of using global requires and excludes, this plugin looks for a feed-level
configuration parameter called filter_categories, which is a comma-separated
list of categories that are allowed.  If at least one of the categories is not
found in the blog entry then the entry is rejected.
"""

import sys
import re
from xml.dom import minidom

def is_youtube(object):
    # try to find youtube videos
    for regex in [ 'www\.youtube\.com/v/(\w*)', 'www\.youtube\.com/embed/(\w*)' ]:
        youtube = re.findall(regex, object, flags=re.DOTALL)
        if youtube:
            f=open('/tmp/toto','w')
            f.write(str(youtube))
            f.write(object)
            f.close()
            ans = '<div class="separator" style="clear: both; text-align: center;">'
            ans += '<iframe width="420" height="315" src="http://www.youtube.com/embed/' +\
                youtube[0] + '" frameborder="0"></iframe>'
            ans += '</div>'
            return ans
    return ''

if __name__ == '__main__':
    entry = sys.stdin.read()
    #f=open('/tmp/toto','w')
    #f.write(entry)
    #f.close()
    if not entry:
        sys.stdout.write(entry)
        sys.exit(0)
    
    entry_dom = minidom.parseString(entry)

    # Collect all the <category> elements from the entry and then see
    # if it also happens to be in our required categories list.  If there aren't
    # any <category> elements in the entry then skip it
    description = entry_dom.getElementsByTagName('description')
    description = entry
    #if not description:
    #    sys.stdout.write(entry)
    #    sys.exit(0)

    for regex in ['(&lt;object.*?&lt;/object&gt;)', '(&lt;iframe.*?&lt;/iframe&gt;)']:
        object_list = re.split(regex, description, flags=re.DOTALL)
        final_description = ''
        for object in object_list:
            if not re.findall(regex, object, flags=re.DOTALL):
                final_description += object
                continue
            sanitized_object = is_youtube(object)
            if sanitized_object:
                final_description += sanitized_object
                continue
            else:
                # do not display the content, maybe we'll need more rules to override certain defaults
                #final_description += object
                pass
        description = final_description

    sys.stdout.write(description)
    sys.exit(0)
