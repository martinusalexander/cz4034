import requests
import json
from parser import reviewPageParser,searchPageParser

def get_all_hotel_review(hotel_id):

    cityid = 4064
    search_page_url = "https://www.agoda.com/pages/agoda/default/DestinationSearchResult.aspx?city=" + str(cityid)
    #
    # r = requests.get(search_page_url);
    # search_page_html = r.text.encode('utf-8')
    #
    # search_parser = searchPageParser()
    #
    # search_parser.feed(search_page_html)
    # hotel_arr = search_parser.get_hotel_arr()
    search_json_url = 'https://www.agoda.com/api/en-us/Main/GetSearchResultList'
    search_hotel_header = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept-Language': 'en-US,en;q=0.8,es;q=0.6,ja;q=0.4,zh-CN;q=0.2,zh;q=0.2,zh-TW;q=0.2',
        'Referer': search_page_url,
        'Origin': 'https://www.agoda.com',
        'Accept-Encoding': 'gzip, deflate, br'
    }
    search_hotel_payload = {
        "CityId": 4064,
        "LengthOfStay": 1,
        "PageNumber": 1,
        "PageSize": 45
    }
    incremental_review_list = []
    for i in range(1,10):
        search_hotel_payload['PageNumber'] = i
        r = requests.post(search_json_url, data=search_hotel_payload,headers=search_hotel_header)
        hotel_list = json.loads(r.text.encode('ascii', 'ignore'))['ResultList']
        incremental_review_list += get_hotel_review(hotel_list)

    return incremental_review_list




def get_hotel_review(hotel_list):
    get_review_url = 'https://www.agoda.com/NewSite/en-us/Review/ReviewComments'

    numberOfReview = 3
    payload = {"hotelId": 0,
               "providerId": 332,
               "demographicId": 0,
               "page": 1,
               "pageSize": numberOfReview,
               "sorting": 1,
               "providerIds": 332,
               "isReviewPage": False,
               "isCrawlablePage": True,
               "filters": {"language": [],
                           "room": []}
               }
    review_parser = reviewPageParser()

    # filename = "output.csv"
    # f = open(filename, "w+")
    # f.close()

    for hotel in hotel_list:
        payload["hotelId"] = int(hotel['HotelID'])
        r = requests.post(get_review_url, json=payload)
        review_data = r.text.encode('utf-8')
        print hotel['MainPhotoUrl']
        review_data = '<div data-selenium="hotel-price">' + str(hotel['DisplayPrice']) + '</div>' + review_data
        review_data = '<div data-selenium="hotel-starRating">' + str(hotel['StarRating']) + '</div>' + review_data
        review_data = '<div data-selenium="hotel-ReviewScore">' + str(hotel['ReviewScoreFormatted']) + '</div>' + review_data
        review_data = '<div data-selenium="hotel-header">' + hotel['EnglishHotelName'].encode('ascii', 'ignore') + '</div>' + review_data
        review_data = '<div data-selenium="hotel-image">' + hotel['MainPhotoUrl'].encode('ascii', 'ignore') + '</div>' + review_data
        review_parser.feed(review_data)
        # export to csv
        # review_parser.exportToCSV()

    review_list = review_parser.getReviewList()
    return review_list

get_all_hotel_review(0)