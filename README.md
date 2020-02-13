# Recommendation_System
1.	CRAWLING
  Before crawling the website, I discussed with my partner about the choice of tools that we can use. We compared several tools including the choices mentioned in the description. And then pick up the “scrapy”as our final decision. Because we can set the domain of parsing and the number of webs we finally retrieve by modifying the class in the API. It is very convenient and friendly for python programmer.
 
                                                              Figure 1 Data Flow of Scrapy

A.	Procedure
Download scrapy in pycharm. Then, use the command line to create a program directory. 
The command is :scrapy startproject scrapypart.  Therefore, I got the package which contained a sub-package called spider. And in the spider, it is the basic architecture of the spider. I created a python file called CUResearchSpider. And build two class, parsing concordia/research.html and aitopic/org separately.
                                
                                             Figure 2   architecture of scrapy
In the two classes, the parsing procedure is like this: request to the url for the data that we want and save the data which is returned from the server into a json file. And save the link in <a href=”….”> as a new url and recall the function recursively until the counter equaled to the limit we set before. 
        
                                            Figure 3 Data in the web that we parsed
               
                                          Figure 4 some parameters I set for parsing
B.	Difficulties
  At first we don’t know what what we should do on each url and how to get more links. Then we learnt from many examples and found that “parse” could be  recall recursively.  
Besides, it corrupted sometimes if the server is not steady and took about 40 minutes to parse one website for 10000 results. 
C.	results 
      1000 json websites for each two websites root. 20000 json files in total.Each parsing         took more than 30 minutes.
D.	Interesting findings
   Not all the json file has content. Because the tags we set for html is stable, but some webs doesn’t has text in these tags.
   Sometimes over the limit we have set. For instance, my threshold is 10000, but it came out as 100080 pages. Because some of the web has no response in time.
 
Figure 5 record of scrapy
2.	DATA PREPROCESSING (INDEX)
A.	Procedure
   After crawling, I store 10000 json files for each root websites under two directories which is ready for indexing.  AICrawledFiles is for AIIndex, CrawledFiles is for InvertedIndex(for Concordia websites)
   Indexing: Read each json file from the directories. The two group of blocks both use the url as the key, and the text on the website as the value. Then do the SPIMI and the Merge which is same as Project1.
   I still split the diction into two segments same as Project1.
                                         
Figure 6 the directory for storing json files
B.	Troubles
Some files are empty. At first, I default all the files can be read, but it crashed on 363th file when I read files from CrawledFiles. Although just one of 10000 json file is empty, it halted. Therefore, I added the judgment of empty file before I read the file.
if os.path.getsize(
        '/Users/maxyqiu/Desktop/IR&WebSearch/Research_Analysis_System/AICrawledFiles/' + F + '.json'):


C.	results 
Two Indexes for two group json files. About 400MB for each
 
 
                                      Figure 7 a scope of raw indexes without compression


3.	RANKING AND FINDINGS FROM THE COMPARATIONS
Some query I meant to mix with capital letters to test the compression of query. My partner’s and my queries are following:
Mine: 

Lei’s: 
A.	Tf-idf vs BM25
I have three different queries which also have different information need. Learning from the top10 scores, the most obvious differences can be seen from the query ‘AI research Department’. It is apparent that the results return from TF-IDF weight scoring is less relevant than BM25. Some documents with higher relevance to the query get lower scores in TF-IDF. 
For scoring, there is also another trick which bothered me before. The shorter query it                    is, the lower marks it gets, and lower differences between files .
 
                                                      Figure 8 BM25 results
 
            				Figure 9 TF-IDF
B.	My testing queries VS My friends’ queries
i.	For the first question in 2, the number of my results is almost 3 times of my partner’s. Because he put more key word in one query. For example, ‘ai artificial intelligent department’ has just 180 results but ‘AI research Department’ has 387 results.
               
ii.	The other surprising findings happened on the second question--find the researchers. My partner use ‘working’ to present the researchers, which even has some more relevant results. 
            

iii.	The last findings: No matter which question it is searching for, ‘smart’ caused many irrelevant recalls with high scores. Therefore, information retrieval is not only tokens work, but also semantics work.
 
 


C.	My queries on my machine vs my friend’s machine
There are some apparent differences between my results and my friend’s. I think it is due to different parsing methods. He has just 1000 files for Concordia index and 2000 for AIIndex. Here are some comparations. (The white background image is from my friend)
 
 
 
 
 
 
5.	CONCLUSION
The whole project is really like a long and interesting journey. Information retrieval should really focus on the need of information. There are 3 points I have learnt by heart. 
i.	Ranking method
A reliable method should consider more about the correlation between the query token and the whole corpus. Such as BM25, the average length of documents in the corpus is one of the parameters. Therefore, it is more effective.
ii.	Diversity of Corpus
More parsing results can give more possibilities when doing the research. However, it can’t guarantee the correctness of results because there are also other reasons affect the scoring.
iii.	Keywords
It seems like my system can’t return the similar results between the queries with the same meaning. Because it is not a semantical system. Therefore, next step to improve it is probably relevant to Natural Language Processing.
