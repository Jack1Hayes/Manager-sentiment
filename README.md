# Manager-setiment
Sentiment analysis of managers in EPL

This project contains 3 programs that can be combined but are more efficient when used separatly if outside of a personally created GUI. Use the Scrapper first to get the managers and clubs needed for the twitter accessor. The Twitter accessor will access twitter for the public tweets about the manager over the past week for weach club before using that information in the dataanal to get the sentiment for each manager.

The scrapper will access websites that contain some of the basic information needed for the program, such as managers, clubs and Twitter handles. This information onl needs to be updated when new managers are introduced into clubs and can be held and rewriten on your computer where you chose.

Scrapper prerequisits:

pandas
requests
BeautifulSoup
seaborn

The Twitter accessor will acess tweets about managers of different clubs for later analysis. You will reqire a tweepy account and cdes to use this step.

Twitter accessor prerequisits:

tweepy
pandas
datetime

The dataanal will analyse the data from the tweets and produce the percentage of tweets which are positive, negative or netural about the managers of each of the teams in the EPL. This is a vader analysis and can be changed into TEXTBLOB or ones own fairly simply

dataanal prerequisits:

numpy
pandas
vaderSentiment
seaborn
datetime

I also changed some of the words in the database of Vader so that database reflects better the words used in the real tweets.
