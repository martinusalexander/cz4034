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
        self.global_image_url = ""
        self.global_price = ""
        self.global_starRating = ""
        self.global_hotelReviewScore = ""
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
                # hotel price
                hotel_name_pattern = re.compile('hotel\-price')
                if hotel_name_pattern.match(attr[1]):
                    self.classPattern = "hotel price"
                # hotel starRating
                hotel_name_pattern = re.compile('hotel\-starRating')
                if hotel_name_pattern.match(attr[1]):
                    self.classPattern = "hotel starRating"
                # hotel ReviewScore
                hotel_name_pattern = re.compile('hotel\-ReviewScore')
                if hotel_name_pattern.match(attr[1]):
                    self.classPattern = "hotel ReviewScore"
                # imageUrl
                imageUrl_pattern = re.compile('hotel\-image')
                if imageUrl_pattern.match(attr[1]):
                    self.classPattern = "imageUrl"
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
            self.review_model.imageUrl = self.global_image_url
            self.review_model.price = self.global_price
            self.review_model.starRating = self.global_starRating
            self.review_model.hotelReviewScore = self.global_hotelReviewScore
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
        elif self.classPattern == "imageUrl":
            self.global_image_url = data
            print("imageUrl :", self.global_image_url)
            self.classPattern = ""
        elif self.classPattern == "hotel ReviewScore":
            self.global_hotelReviewScore = data
            print("hotel review score :", self.global_hotelReviewScore)
            self.classPattern = ""
        elif self.classPattern == "hotel price":
            self.global_price = data
            print("price :", self.global_price)
            self.classPattern = ""
        elif self.classPattern == "hotel starRating":
            self.global_starRating = data
            print("star rate :", self.global_starRating)
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
                'imageUrl': record[6],
                'price': record[7],
                'starRating': record[8],
                'hotelReviewScore': record[9]
            }
            output.append(review)
        return output
    def exportToCSV(self):
        with open('output.csv', 'a') as csv_file:
            wr = csv.writer(csv_file, delimiter=',')
            for record in self.review_list:
                wr.writerow(list(record))
        self.review_list = []
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
            if (attr[0] == 'srcset'):
                print attr
                print "src...............",attr[1].encode('utf-8').split()[0]
                img_url_pattern = re.compile('\/\/pix6\.agoda\.net\/hotelImages.+')
                if img_url_pattern.match(attr[1]):
                    self.hotel_model['imageUrl'] = attr[1].encode('utf-8').split()[0]
                    print "src...............",self.hotel_model['imageUrl']

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
        self.imageUrl = ""
        self.price = ""
        self.starRating = ""
        self.hotelReviewScore = ""

    def __iter__(self):
        return iter([self.name,
                     self.score,
                     self.title,
                     self.content,
                     self.reviewTime,
                     self.link,
                     self.imageUrl,
                     self.price,
                     self.starRating,
                     self.hotelReviewScore])






                        # for line in infile:
    #     parser.feed(line)
        # outfile.write(line.split("<_|_>")[0])
# parser.feed('<html><head><title data-selenium="comments-title">Test</title>'
#             '</head><body><h1>Parse me!</h1>'
            # '<div class="comment-text" data-selenium="reviews-comments" data-review-comment-text="">'
            #     '<span>Ok</span>'
            # '</div></body></html>')
