import copy
import psycopg2
import logging
import json
from crawler.src.models import FlickrMessage
from crawler.src.models import FlickrOwner
from crawler.src.models import FlickrLocation
from crawler.src.db.DBConnection import DBConnection

class CRUD():

    def __init__(self, path_home, conn_sec):
        self.setUp(path_home, conn_sec)

    def setUp(self, path_home, conn_sec):
        try:
            self.conn = DBConnection(path_home, conn_sec).connect_database()
            self.cur = self.conn.cursor()
        except Exception as e:
            raise e

    def save(self, message=None, conn_table=None):

        raw_json = copy.deepcopy(message)

        try:
            message = message.pop('photo')
            if message:
                flickrMessage = FlickrMessage()
                flickrOwner = FlickrOwner()
                flickrLocation = FlickrLocation()

                ''' message data '''
                flickrMessage.id = message['id']
                flickrMessage.secret = message['secret']
                flickrMessage.created_at = message['dates']['taken']
                flickrMessage.date = str(message['dates']['taken'])[0:10]
                flickrMessage.isfavorite = message['isfavorite']
                flickrMessage.license = message['license']
                flickrMessage.safety_level = message['safety_level']
                flickrMessage.farm = message['farm']
                flickrMessage.title = message['title']['_content']
                flickrMessage.ispublic = message['visibility']['ispublic']
                flickrMessage.isfriend = message['visibility']['isfriend']
                flickrMessage.isfamily = message['visibility']['isfamily']
                flickrMessage.description = message['description']['_content']
                flickrMessage.views = message['views']
                flickrMessage.comments = message['comments']['_content']
                flickrMessage.media = message['media']
                ''' tags '''
                try:
                    for i, item in enumerate(message['tags']['tag']):
                        if i == 0:
                            tags = '{'
                        tags = tags + "\'" + item['raw'] + "\'"
                        if i != len(message['tags']['tag'])-1:
                            tags = tags + ','

                    tags = tags + '}'
                    flickrMessage.tags = tags
                except Exception as e:
                    pass
                ''' urls '''
                try:
                    for i, item in enumerate(message['urls']['url']):
                        if i == 0:
                            urls = '{'
                            urls = urls + "\'" + item['_content'] + "\'"
                        if i != len(message['urls']['url'])-1:
                            tags = tags + ','

                    urls = urls + '}'
                    flickrMessage.urls = urls
                except Exception as e:
                    pass

                ''' user data '''
                owner = message.pop('owner')

                if owner:
                    flickrOwner.nsid = owner['nsid']
                    flickrOwner.username = owner['username']
                    flickrOwner.location = owner['location']

                ''' location data '''
                location = message.pop('location')
                if location:
                    flickrLocation.id = location['place_id']
                    flickrLocation.accuracy = location['accuracy']
                    try:
                        flickrLocation.county = location['county']['_content']
                    except:
                        pass
                    flickrLocation.region = location['region']['_content']
                    flickrLocation.country = location['country']['_content']
                    try:
                        flickrLocation.longitude = location['longitude']
                        flickrLocation.latitude = location['latitude']
                        flickrLocation.coordinates = "POINT({} {})".format(flickrLocation.longitude, flickrLocation.latitude).replace(',', '.')
                    except:
                        pass
                    try:
                        flickrLocation.locality = location['locality']['_content']
                    except:
                        pass

                try:
                    self.cur.execute("""SET TimeZone = 'UTC' """)
                    self.cur.execute(
                        "INSERT INTO " + conn_table + " (id, secret, created_at, date, isfavorite, license, safety_level, farm, title, description, visibility_ispublic, visibility_isfriend, visibility_isfamily, "+
                        "views, comments, location_accuracy, location_locality, location_county, location_region, location_country, owner_nsid, owner_username, owner_location, media, tags, urls, coordinates, flickr)" +
                        """VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ST_GeomFromText(%s, 4326), %s)""",
                        (flickrMessage.id, flickrMessage.secret, flickrMessage.created_at, flickrMessage.date, flickrMessage.isfavorite, flickrMessage.license, flickrMessage.safety_level, flickrMessage.farm,
                         flickrMessage.title, flickrMessage.description, flickrMessage.ispublic, flickrMessage.isfriend, flickrMessage.isfamily, flickrMessage.views, flickrMessage.comments, flickrLocation.accuracy,
                         flickrLocation.locality, flickrLocation.county, flickrLocation.region, flickrLocation.country, flickrOwner.nsid, flickrOwner.username, flickrOwner.location, flickrMessage.media,
                         flickrMessage.tags, flickrMessage.urls, flickrLocation.coordinates, json.dumps(raw_json)))
                    self.conn.commit()
                except psycopg2.IntegrityError as e:
                    self.conn.rollback()
                    pass

        except Exception as e:
            logging.error(e)
            pass
