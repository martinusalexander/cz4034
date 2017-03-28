import requests
from parser import reviewPageParser,searchPageParser

def get_all_hotel_review(hotel_id):
    # crawl all hotel review
    cityid = 8691
    search_page_url = "https://www.agoda.com/pages/agoda/default/DestinationSearchResult.aspx?city=" + str(cityid)

    r = requests.get(search_page_url);
    search_page_html = r.text.encode('utf-8')
    # print search_page_html
    search_parser = searchPageParser()
    hotel_arr = []
    # for i in rang
    search_parser.feed(search_page_html)
    hotel_arr = search_parser.get_hotel_arr()

    get_review_url = 'https://www.agoda.com/NewSite/en-us/Review/ReviewComments'

    payload = {"hotelId": 0,
               "providerId": 332,
               "demographicId": 0,
               "page": 1,
               "pageSize": 100,
               "sorting": 1,
               "providerIds": 332,
               "isReviewPage": False,
               "isCrawlablePage": True,
               "filters": {"language": [],
                           "room": []}
               }
    review_parser = reviewPageParser()

    for hotel in hotel_arr:
        payload["hotelId"] = int(hotel['hotelid'])
        r = requests.post(get_review_url, json=payload)
        review_data = r.text.encode('utf-8')
        # print review_data
        review_data = '<div data-selenium="hotel-header">' + hotel['hotelName'] + '</div>' + review_data
        # print review_data
        # review_data +
        review_parser.feed(review_data)

    # Export to CSV
    # review_parser.exportToCSV(hotel_arr)

    review_list = review_parser.getReviewList()
    return review_list