import re
from HTMLParser import HTMLParser
import csv
import datetime

class reviewPageParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.classPattern = ""
        self.review_model = reviewModel()
        self.review_list = []
        self.global_hotel_name = ""
        self.global_hotel_link = ""
    def handle_starttag(self, tag, attrs):
        self.startTag = ""
        self.contentStart = False
        # print("Encountered a start tag:", tag)
        for attr in attrs:
            if(attr[0] == 'data-selenium'):
                # hotel name
                hotel_name_pattern = re.compile('hotel\-header')
                if hotel_name_pattern.match(attr[1]):
                    self.classPattern = "hotel name"
                    print('name matched.............')
                # title
                title_pattern = re.compile('comments\-title')
                if title_pattern.match(attr[1]):
                    self.classPattern = "title"
                # content
                content_pattern = re.compile('reviews\-comments')
                if content_pattern.match(attr[1]):
                    self.classPattern = "content"
                    self.contentStart = True
                # review time
                date_pattern = re.compile('review\-date')
                if date_pattern.match(attr[1]):
                    self.classPattern = "review time"
                # score
                score_pattern = re.compile('individual\-review\-rate')
                if score_pattern.match(attr[1]):
                    self.classPattern = "score"

    def handle_endtag(self, tag):
        if self.classPattern == "content":
            print "content end"
            self.classPattern = ""
        # self.classPattern = ""
        # print("Encountered an end tag :", tag)

    def handle_data(self, data):
        # print(self.flag)
        if self.classPattern == "title":
            self.review_model.title = data
            print("title :", data)
            self.classPattern = ""
        elif self.classPattern == "content":
            self.review_model.content += data
            if self.contentStart == True:
                print "content :", self.review_model.content
            else:
                print data
            # self.classPattern = ""
        elif self.classPattern == "score":
            self.review_model.content = re.sub("  +|\r\n", '', self.review_model.content)
            print "restruct content = ", self.review_model.content
            self.review_list.append(self.review_model)
            self.review_model = reviewModel()
            self.review_model.name = self.global_hotel_name
            self.review_model.link = self.global_hotel_link
            self.review_model.score = data
            print("score :", data)
            self.classPattern = ""
        # elif self.classPattern == "link":
        #     self.review_model.link = data
        #     print("link :", data)
        #     self.classPattern = ""
        elif self.classPattern == "review time":
            self.review_model.reviewTime = data
            print("review time :", data)
            self.classPattern = ""
        elif self.classPattern == "hotel name":
            self.global_hotel_name = data
            print("hotel name :", data)
            data = re.sub(' +','-',data)
            self.global_hotel_link = 'https://www.agoda.com/' + re.sub('\-+','-',data) + '/hotel/singapore-sg.html'
            print("hotel link :", self.global_hotel_link)
            self.classPattern = ""
    def getReviewList(self):
        output = []
        for record in self.review_list:
            record = list(record)
            review = {
                'hotel_name': record[0],
                'rating': record[1],
                'title': record[2],
                'content': record[3],
                'date': record[4],
                'url': record[5],
            }
            output.append(review)
        return output

class searchPageParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        # self.hotelID = []
        # self.hotelName = []
        self.hotel_arr = []
        self.hotelNameData = False
        self.hotel_model = {}
    def handle_starttag(self, tag, attrs):
        self.startTag = ""
        self.contentStart = False
        # print("Encountered a start tag:", tag)
        for attr in attrs:
            if (attr[0] == 'data-hotelid'):
                self.hotel_model = {}
                self.hotel_model['hotelid'] = attr[1]
                print "hotel id : ",attr[1]
            if (attr[0] == 'data-selenium' and attr[1] == 'hotel-name'):
                self.hotelNameData = True
    def handle_data(self, data):
        if self.hotelNameData == True:
            self.hotelNameData = False
            name = re.sub("  +|\r\n", '', data)
            self.hotel_model['hotelName'] = name
            name = re.sub(' +','-',name)
            self.hotel_model['link'] = re.sub('\-+','-',name)
            # print self.hotel_model
            self.hotel_arr.append(self.hotel_model)
    def get_hotel_arr(self):
        return self.hotel_arr

class reviewModel:
    def __init__(self):
        self.name = ""
        self.score = 0
        self.title = ""
        self.content = ""
        self.reviewTime = ""
        self.link = ""

    def __iter__(self):
        return iter([self.name,
                     self.score,
                     self.title,
                     self.content,
                     self.reviewTime,
                     self.link])






                        # for line in infile:
    #     parser.feed(line)
        # outfile.write(line.split("<_|_>")[0])
# parser.feed('<html><head><title data-selenium="comments-title">Test</title>'
#             '</head><body><h1>Parse me!</h1>'
            # '<div class="comment-text" data-selenium="reviews-comments" data-review-comment-text="">'
            #     '<span>Ok</span>'
            # '</div></body></html>')
