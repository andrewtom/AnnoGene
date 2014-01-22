from collections import defaultdict
import os
import re
import sys
try:
    import web
except ImportError, e:
    os.system("pip install web.py ")

from web import form


render = web.template.render('templates/')

urls = ('/', 'index')
app = web.application(urls, globals())

myform = form.Form(form.Textarea('Data',form.regexp(r"^(chr([1-9]|1[0-9]|2[0-2]|MT|X|Y)(\s|:)\d+(\s|-)(\d+)\n*)", ' Incorrect data format')),form.Textbox('Accuracy',form.regexp('^\d*$','Must be not negative number!')),form.Dropdown('Genome', ['mm9', 'mm10', 'hg19']))

myform2 = form.Form(form.Button('action',value='HELP',html='HELP'))
class index:
    def GET(self):
        form = myform()
        form2= myform2()
        # make sure you create a copy of the form by calling it (line above)
        # Otherwise changes will appear globally
        return render.gene(form,form2)

    def POST(self):
        form = myform()
        form2 = myform2
        # default validation
        if not form.validates():
            return render.gene(form,form2)

        # custom validation
        try:
            queries = parse_queries(form['Data'].value)
        except ValueError as e:
            return e.message

        # "mm9" or "mm10" or "hg19"

        # at this point everything is validated
        #with measure("All"):
        lista = query(queries,form['Accuracy'].value,form['Genome'].value)
        #lista = foo1(form['Data'].value.split('\n'))

        return "".join(lista)
        


QUERY_PATTERN = re.compile(r"(chr\d+|chrMT|chrX|chrY)(\s|:)(\d+)(\s|-)(\d+)")
def parse_queries(raw_queries):
    queries = []
    for i, raw_query in enumerate(raw_queries.split('\n')):
        match = re.match(QUERY_PATTERN, raw_query)
        if not match:
            raise ValueError("Wrong match: line %d" % (i+1))
        id_, start, end = match.group(1), int(match.group(3)),int(match.group(5))
        if start > end:
            raise ValueError("Error! Start>end in line nr %d" % (i+1))
        queries.append((id_, start, end))
    return queries


def parse_file(filename):
    """ Return a dict mapping from ids (like 'chr9') to tuples 
(start, end)."""
    data = defaultdict(list)
    with measure("Opening and parsing the data file"):
        with open(filename) as plik:
            for line in plik:
                id_, c1, c2 = line.split("\t")[:3]
                c1, c2 = int(c1), int(c2)
                data[id_].append((c1, c2, line))
    return data


def query(queries,accuracy,genome):
    
    if genome=="mm9":
       data = parse_file(sys.path[0]+"/geny2mm9.txt")
    if genome=="mm10":
       data = parse_file(sys.path[0]+"/geny2mm10.txt")
    if genome=="hg19":
       data = parse_file(sys.path[0]+"/geny2hg19.txt")
    #genome = form['Genome'].value
    with measure("Searching"):
        listastart, listaend = [], []
        if not accuracy:
          accuracy=0
        for id_, c1, c2 in queries:
            startmin1 = min(data[id_], key=lambda x: abs(x[0]-int(((c1+c2)/2))))
            endmin1 = min(data[id_], key=lambda x: abs(x[1]-int(((c1+c2)/2))))
            dobre=filter(lambda x: x[0]<=(c1+c2)/2 <= x[1],data[id_])   
            listka=[]
            if dobre:
             listka.append(min(dobre))                       
             listastart.append(genome+"\t%s\t%d\t%d\t%s" % (id_, c1, c2,min(listka)[2]))
            else:
             minima1=min(abs(startmin1[0]-((c1+c2)/2)),abs(startmin1[1]-int(((c1+c2)/2))))
             minima2=min(abs(endmin1[0]-((c1+c2)/2)),abs(endmin1[1]-int(((c1+c2)/2))))
             if int(accuracy)==0:
               if int(minima1) <= int(minima2):
                 listka.append(startmin1)
               else:
                 listka.append(endmin1)  
               listastart.append(genome+"\t%s\t%d\t%d\t%s" % (id_, c1, c2,min(listka)[2]))
             else:
               if (int(minima1) <= int(accuracy)) or (int(minima2) <= int(accuracy)):
                 if int(minima1) <= int(minima2):
                  listka.append(startmin1)
                 else:  
                  listka.append(endmin1)


               if listka: 
                    listastart.append(genome+"\t%s\t%d\t%d\t%s" % (id_, c1, c2,min(listka)[2]))
                     
         

    lista = listastart 
    return set(lista)
    
    
    


## helpers for time tests

import time
class measure(object):
    def __init__(self, text):
        self.text = text

    def __enter__(self):
        self.t = time.time()

    def __exit__(self, *args):
        dt = time.time() - self.t
        print "(%5.2f sek)" % dt, self.text

## end of the helpers


#def foo1(tablica, **kwargs):
#    """ Original """

#    listastart=[]
#    listaend=[]
#    for i in tablica:
#        separ = re.match(r"(chr\d+|chrMT|chrX|chrY)(\s|:)(\d+)(\s|-)(\d+)", i)

#        if bool(separ)==True:
#            if int(separ.group(3))<==int(separ.group(5)):
#                listastartow=[]
#               listaendow=[]
#                start={}
#                end={}
#                plik=open("mm9dane2.txt")
#                for line in plik:
#                    if separ.group(1)+"\t" in line:
#                        listastartow.append(line.split("\t")[1])
#                       listaendow.append(line.split("\t")[2])
#                        start[line.split("\t")[1]]=line
#                       end[line.split("\t")[2]]=line
#               startmin=min(listastartow,key=lambda x:abs(int(x)-int(separ.group(3))))
#               endmin=min(listaendow,key=lambda x:abs(int(x)-int(separ.group(5))))
#               listastart.append(separ.group(1)+"\t"+separ.group(3)+"\t"+separ.group(5)+"\t"+start[startmin])
#                listaend.append(separ.group(1)+"\t"+separ.group(3)+"\t"+separ.group(5)+"\t"+end[endmin])
#           else:
#                return "Error! Start&gt;end in line nr "+ str(tablica.index(i)+1)
#        else:
#            return "Wrong match: line "+str(tablica.index(i)+1)

#    lista=listastart+listaend
#    lista=list(set(lista))
#    return lista




if __name__=="__main__":
    web.internalerror = web.debugerror
    sys.argv.append(sys.argv[1])
    app.run()
