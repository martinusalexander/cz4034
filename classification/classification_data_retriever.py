from models.models import *

import os
import csv

def retrieve():
    '''
    SQL query
    SELECT
        review.id, review.title, review.content, label.label
    FROM
        cz4034.models_hotel_review AS review,
        cz4034.models_hotel_label AS label
    WHERE
        review.label_id = label.id
        AND label.method = 'Manual';
    ORDER BY
        label.label
    '''
    reviews = Hotel_Review.objects.filter(label__method='Manual').order_by('label__label')
    folder_path = os.path.join(os.getcwd(), 'classification')
    filename = 'classification_data.csv'
    counter = 0
    with open(os.path.join(folder_path, filename), mode='w') as csv_file:
        writer = csv.writer(csv_file)
        for review in reviews:
            try:
                counter = counter + 1
                writer.writerow([review.id, review.title, review.content, review.label.label])
            except AttributeError as err:
                print(err)
            except UnicodeEncodeError as err:
                print(err)
    report = 'Retrieved ' + str(counter) + ' data.'
    return report
