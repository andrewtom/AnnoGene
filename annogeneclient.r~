#!/usr/bin/env Rscript
#R REST client for Gene Annotator
#libcurl is needed before(sudo apt-get install libcurl4-openssl-dev)
require('RCurl')

args <- commandArgs(TRUE)
library('RCurl')

url <- "http://bedanno.cremag.org"
#result <- postForm(url,Data="chr2 10000 10000000",Accuracy="100000",Genome="mm9")
#result <- postForm(url,Data=args[1],Accuracy=args[2],Genome=args[3])
if (args[2] !=""){
 if (as.integer(args[2])<0)
   {cat('Accuracy must be positive!\n');quit(save='no')}
}
tryCatch({result <- postForm(url,Data=args[1],Accuracy=args[2],Genome=args[3])},error=function(e) {cat('Genome not available!\n');quit(save='no')})
#wynik=as.character(result)
#map=setNames(c("A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","\n","0","1","2","3","4","5","6","7","8","9","\t","-", 
#".","\r"),c#("41","42","43","44","45","46","47","48","49","4a","4b","4c","4d","4e","4f","50","51","52","53","54","55","56","57","58","59","5a","61","62","63","64","65","66","67","68","69","6a","6b","6c","6d","6e",
#"6f","70","71","72","73","74","75","76","77","78","79","7a","0a","30","31","32","33","34","35","36","37","38","39","09","2d","2e",
#"0d"))
#wynik[]=map[unlist(wynik)]
#paste(wynik,collapse="")
tryCatch({cat(rawToChar(result))},error=function(e) {cat('Wrong match: line 1\n')})
#cat(rawToChar(result))
