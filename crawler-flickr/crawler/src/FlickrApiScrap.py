import flickrapi
import json
import logging
import datetime
from datetime import timedelta

from crawler.src.CRUD import CRUD
from crawler.src.db.DBConnection import DBConnection


class FlickrApiScrap:

    def __init__(self, path_home, conn_sec, schema, table, api_key,
                 api_secret, images_path, videos_path, geo=None,
                 search_word=None, time_lag=1):
        self.geo = geo
        self.path_home = path_home
        self.conn_sec = conn_sec
        self.conn_schema = schema
        self.conn_table = table
        self.CRUD = CRUD(self.path_home, self.conn_sec)
        self.search_word = search_word
        self.api_key = api_key
        self.api_secret = api_secret
        self.images_path = images_path
        self.videos_path = videos_path
        self.running = False

        now = datetime.datetime.now() - timedelta(days=time_lag)
        self.min_upload_date = now.strftime("%Y-%m-%d %H:%M:%S")

        # Create database table if it does not exist.
        self.create_table()

        # Create the Flickr Stream object if running variable is False.
        while True:
            if not self.running:
                self.init()

    def create_table(self):
        try:
            template = open(
                self.path_home + '/template-table.sql', 'r').read() % (
                str(self.conn_schema), str(self.conn_table), str(self.conn_table),
                str(self.conn_schema), str(self.conn_table), str(self.conn_schema),
                str(self.conn_table), str(self.conn_table), str(self.conn_schema),
                str(self.conn_table))
            conn = DBConnection(self.path_home, self.conn_sec).connect_database()
            cur = conn.cursor()
            cur.execute(template)
            conn.commit()
        except Exception as e:
            raise e
        finally:
            conn.close()

    def init(self):
        try:
            api = flickrapi.FlickrAPI(self.api_key, self.api_secret, format='json')
            self.running = True
            MyStreamListener(api=api, crud=self.CRUD,
                             conn_sec=self.conn_sec,
                             conn_schema=self.conn_schema,
                             conn_table=self.conn_table,
                             geo=self.geo,
                             search_word=self.search_word,
                             min_upload_date=self.min_upload_date)
        except Exception as e:
            self.running = False
            logging.error(e)
            pass


class MyStreamListener:

    def __init__(self, api, crud, conn_sec, conn_schema, conn_table, geo,
                 search_word, min_upload_date):
        self.api = api
        self.crud = crud
        self.conn_sec = conn_sec
        self.conn_schema = conn_schema
        self.conn_table = conn_table
        self.geo = geo
        self.search_word = search_word
        self.min_upload_date = min_upload_date
        self.on_data()

    def on_data(self):
        try:
            while True:
                if self.search_word and self.geo:
                    raw_photos = self.api.photos_search(
                        bbox=str(self.geo[0]) + ',' + str(self.geo[1]) + ',' +
                             str(self.geo[2]) + ',' + str(self.geo[3]),
                        text=self.search_word, privacy_filter=1,
                        safe_search=1, min_upload_date=self.min_upload_date,
                        sort='date-posted-des', per_page=250)
                elif self.search_word:
                    raw_photos = self.api.photos_search(
                        text=self.search_word, privacy_filter=1,
                        safe_search=1, min_upload_date=self.min_upload_date,
                        sort='date-posted-des', has_geo=1, per_page=500)
                else:
                    raw_photos = self.api.photos_search(
                        bbox=str(self.geo[0]) + ',' + str(self.geo[1]) + ',' +
                             str(self.geo[2]) + ',' + str(self.geo[3]),
                        privacy_filter=1, safe_search=1,
                        min_upload_date=self.min_upload_date,
                        sort='date-posted-des', per_page=250)

                json_photos = json.loads(raw_photos.decode('utf-8'))

                # Get the total of Flickr pages.
                total_pages = int(json_photos['photos']['pages'])
                for page in range(1, total_pages + 1):
                    # Collect the photos
                    if self.search_word and self.geo:
                        raw_photos = self.api.photos_search(
                            bbox=str(self.geo[0]) + ',' + str(self.geo[1]) + ',' +
                                 str(self.geo[2]) + ',' + str(self.geo[3]),
                            text=self.search_word, privacy_filter=1,
                            safe_search=1, min_upload_date=self.min_upload_date,
                            sort='date-posted-des', page=page, per_page=250)

                    elif self.search_word:
                        raw_photos = self.api.photos_search(
                            text=self.search_word, privacy_filter=1,
                            safe_search=1, min_upload_date=self.min_upload_date,
                            sort='date-posted-des', has_geo=1, page=page,
                            per_page=500)
                    else:
                        raw_photos = self.api.photos_search(
                            bbox=str(self.geo[0]) + ',' + str(self.geo[1]) + ',' +
                                 str(self.geo[2]) + ',' + str(self.geo[3]),
                            privacy_filter=1, safe_search=1,
                            min_upload_date=self.min_upload_date,
                            sort='date-posted-des', page=page, per_page=250)

                    json_photos = json.loads(raw_photos.decode('utf-8'))

                    # Extract/get photo id to gather the info of the photos
                    for item in json_photos['photos']['photo']:
                        raw_photo = self.api.photos.getInfo(photo_id=item['id'])
                        json_photo = json.loads(raw_photo.decode('utf-8'))
                        # Save the photo info
                        self.crud.save(message=json_photo,
                                       conn_table=self.conn_schema + '.' + self.conn_table)
        except Exception as e:
            raise e
