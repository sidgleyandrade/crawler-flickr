import flickrapi
import json
import logging

from crawler.src.CRUD import CRUD
from crawler.src.db.DBConnection import DBConnection

from threading import Thread

class FlickrApiScrap(Thread):

    auth = ''

    def __init__(self,path_home, conn_sec, schema, table, api_key, api_secret,
                 images_path, videos_path, geo=None, searchword=None):

        Thread.__init__(self)

        ''' initial parameters '''
        self.geo = geo
        self.path_home = path_home
        self.conn_sec = conn_sec
        self.conn_schema = schema
        self.conn_table = table
        self.CRUD = CRUD(self.path_home, self.conn_sec)
        self.searchword = searchword
        self.api_key = api_key
        self.api_secret = api_secret
        self.images_path = images_path
        self.videos_path = videos_path


    def run(self):
        try:
            self.create_table()
            self.init()
        except Exception as e:
            logging.error(e)
            pass

    ''' if not exists, then to create table from cfg file '''
    def create_table(self):
        try:
            template = open(self.path_home + '/template-table.sql', 'r').read() % (str(self.conn_schema), str(self.conn_table), str(self.conn_table),
                                                                             str(self.conn_schema), str(self.conn_table), str(self.conn_schema),
                                                                             str(self.conn_table), str(self.conn_table), str(self.conn_schema), str(self.conn_table))

            conn = DBConnection(self.path_home, self.conn_sec).connect_database()
            cur = conn.cursor()
            cur.execute(template)
            conn.commit()
        except Exception as e:
            raise e
        finally:
            conn.close()


    ''' creating a stream '''
    def init(self):

        try:
            api = flickrapi.FlickrAPI(self.api_key, self.api_secret, format='json')
            myStreamListener = MyStreamListener(api=api, crud=self.CRUD, conn_sec=self.conn_sec, conn_schema=self.conn_schema, conn_table=self.conn_table, geo=self.geo, searchword=self.searchword)
        except Exception as e:
            logging.error(e)


class MyStreamListener():

    def __init__(self, api, crud, conn_sec, conn_schema, conn_table, geo, searchword):
        self.api = api
        self.crud = crud
        self.conn_sec = conn_sec
        self.conn_schema = conn_schema
        self.conn_table = conn_table
        self.geo = geo
        self.searchword =searchword
        self.on_data()

    def on_data(self):
        logging.info('Connection ' + self.conn_sec + ' established!!')

        try:
            while True:
                ''' collect photos '''
                if(self.searchword and self.geo):
                    raw_photos = self.api.photos_search(bbox=str(self.geo[0])+','+str(self.geo[1])+','+str(self.geo[2])+','+str(self.geo[3]), text=self.searchword,
                                                        privacy_filter=1, safe_search=1, sort='date-posted-des', per_page=250)
                elif self.searchword:
                    raw_photos = self.api.photos_search(text=self.searchword, privacy_filter=1, safe_search=1, sort='date-posted-des', has_geo=1, per_page=500)
                else:
                    raw_photos = self.api.photos_search(bbox=str(self.geo[0])+','+str(self.geo[1])+','+str(self.geo[2])+','+str(self.geo[3]),
                                                        privacy_filter=1, safe_search=1, sort='date-posted-des', per_page=250)

                json_photos = json.loads(raw_photos.decode('utf-8'))

                ''' extract id of photos for gathering the info '''
                for item in json_photos['photos']['photo']:

                    ''' info about each photo '''
                    raw_photo = self.api.photos.getInfo(photo_id=item['id'])
                    json_photo = json.loads(raw_photo.decode('utf-8'))

                    ''' salve the photo info '''
                    self.crud.save(message=json_photo, conn_table=self.conn_schema+'.'+self.conn_table)

        except Exception as e:
            logging.error(e)
            logging.error('Connection ' + self.conn_sec + ' lost!! : ')
            pass
