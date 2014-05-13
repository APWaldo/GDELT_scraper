from time import strptime, mktime, localtime
from csv import reader, writer
from urllib import urlretrieve
from commands import getoutput
import re
from os import system

file = open("input_syria_total.csv")
data = reader(file)

date_change = "20130401"
change_date = mktime(strptime(date_change,"%Y%m%d"))

pulled = {}

for d in data:

   print "Looking for event", d

   output = writer(open(d[0]+"_"+d[2]+".csv","w"),delimiter="\t")

   date = d[2]
   date_object = strptime(date,"%Y%m%d")

   drange = range(0,270)
      
   for r in drange:

      date = mktime(date_object)
      new_date = localtime(date+r*60*60*24)

      def pad(x,n): return("0"*(n-len(str(x)))+str(x))

      y = str(new_date.tm_year)
      m = pad(new_date.tm_mon,2)
      a = pad(new_date.tm_mday,2)
      fd = y+m+a

      if date >= change_date: 

         new_date = fd
         file = new_date+".export.CSV.zip"

      else: 

         new_date = y+m
         file = new_date+".zip"

      url = "http://data.gdeltproject.org/events/"+file

      if not url in pulled: 

         pulled[url] = 0

         urlretrieve(url,file)

         system("unzip -u "+file)
         system("rm "+file)

      if date >= change_date: file = re.sub(".zip","",file)
      else: file = re.sub(".zip","",file)+".csv"

      gdelt = reader(open(file),delimiter="\t")

      for g in gdelt:

         if g[1] == fd and (g[5] == d[1] or g[8] == d[1]): 
            print "found"
            output.writerow(g)

