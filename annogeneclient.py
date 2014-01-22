import urllib
import urllib2
import sys

url="http://bedanno.cremag.org"
params=urllib.urlencode({'Data':sys.argv[1],'Accuracy':sys.argv[2],'Genome':sys.argv[3]})
if sys.argv[3] in ['mm9','mm10','hg19']:
    response=urllib2.urlopen(url,params).read()
    if "negative" in response:
      print "Accuracy must be positive!"
    elif "Incorrect" in response:
      print "Wrong match: line 1"
    else:
      print response
else:
    print 'Genome not available. Try again!'


