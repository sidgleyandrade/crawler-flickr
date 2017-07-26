import copy
import psycopg2
import logging
import json
import datetime

from crawler.src.models import FlickrMessage
from crawler.src.models import FlickrOwner
from crawler.src.models import FlickrLocation
from crawler.src.db.DBConnection import DBConnection


class CRUD:

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
                flickr_message = FlickrMessage()
                flickr_owner = FlickrOwner()
                flickr_location = FlickrLocation()

                flickr_message.id = message['id']
                flickr_message.secret = message['secret']
                flickr_message.posted_created_at = datetime.datetime.\
                    fromtimestamp(int(message['dates']['posted'])).\
                    strftime('%Y-%m-%d %H:%M:%S')
                flickr_message.posted_date = str(
                    datetime.datetime.
                        fromtimestamp(int(message['dates']['posted'])).
                        strftime('%Y-%m-%d %H:%M:%S'))[0:10]
                flickr_message.taken_created_at = message['dates']['taken']
                flickr_message.taken_date = str(message['dates']['taken'])[0:10]
                flickr_message.isfavorite = message['isfavorite']
                flickr_message.license = message['license']
                flickr_message.safety_level = message['safety_level']
                flickr_message.farm = message['farm']
                flickr_message.title = message['title']['_content']
                flickr_message.ispublic = message['visibility']['ispublic']
                flickr_message.isfriend = message['visibility']['isfriend']
                flickr_message.isfamily = message['visibility']['isfamily']
                flickr_message.description = message['description']['_content']
                flickr_message.views = message['views']
                flickr_message.comments = message['comments']['_content']
                flickr_message.media = message['media']

                try:
                    for i, item in enumerate(message['tags']['tag']):
                        if i == 0:
                            tags = '{'
                        tags = tags + "\'" + item['raw'] + "\'"
                        if i != len(message['tags']['tag'])-1:
                            tags = tags + ','

                    tags = tags + '}'
                    flickr_message.tags = tags
                except Exception as e:
                    pass

                try:
                    for i, item in enumerate(message['urls']['url']):
                        if i == 0:
                            urls = '{'
                            urls = urls + "\'" + item['_content'] + "\'"
                        if i != len(message['urls']['url'])-1:
                            tags = tags + ','

                    urls = urls + '}'
                    flickr_message.urls = urls
                except Exception as e:
                    pass

                owner = message.pop('owner')
                if owner:
                    flickr_owner.nsid = owner['nsid']
                    flickr_owner.username = owner['username']
                    flickr_owner.location = owner['location']

                location = message.pop('location')
                if location:
                    flickr_location.id = location['place_id']
                    flickr_location.accuracy = location['accuracy']
                    try:
                        flickr_location.county = location['county']['_content']
                    except:
                        pass
                    flickr_location.region = location['region']['_content']
                    flickr_location.country = location['country']['_content']
                    try:
                        flickr_location.longitude = location['longitude']
                        flickr_location.latitude = location['latitude']
                        flickr_location.coordinates = "POINT({} {})".\
                            format(flickr_location.longitude,
                                   flickr_location.latitude).replace(',', '.')
                    except:
                        pass
                    try:
                        flickr_location.locality = \
                            location['locality']['_content']
                    except:
                        pass

                try:
                    self.cur.execute("""SET TimeZone = 'UTC' """)
                    self.cur.execute("""INSERT INTO """ + conn_table + """ 
                                     (id, secret, posted_created_at, 
                                     posted_date, taken_created_at, taken_date, 
                                     isfavorite, license, safety_level, farm, 
                                     title, description, visibility_ispublic, 
                                     visibility_isfriend, visibility_isfamily, 
                                     views, comments, location_accuracy, 
                                     location_locality, location_county, 
                                     location_region, location_country, 
                                     owner_nsid, owner_username, owner_location, 
                                     media, tags, urls, coordinates, flickr) 
                                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 
                                     %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                                     %s, %s, %s, %s, %s, %s, %s, %s, 
                                     ST_GeomFromText(%s, 4326), %s)""",
                                     (flickr_message.id,
                                      flickr_message.secret,
                                      flickr_message.posted_created_at,
                                      flickr_message.posted_date,
                                      flickr_message.taken_created_at,
                                      flickr_message.taken_date,
                                      flickr_message.isfavorite,
                                      flickr_message.license,
                                      flickr_message.safety_level,
                                      flickr_message.farm,
                                      flickr_message.title,
                                      flickr_message.description,
                                      flickr_message.ispublic,
                                      flickr_message.isfriend,
                                      flickr_message.isfamily,
                                      flickr_message.views,
                                      flickr_message.comments,
                                      flickr_location.accuracy,
                                      flickr_location.locality,
                                      flickr_location.county,
                                      flickr_location.region,
                                      flickr_location.country,
                                      flickr_owner.nsid,
                                      flickr_owner.username,
                                      flickr_owner.location,
                                      flickr_message.media,
                                      flickr_message.tags,
                                      flickr_message.urls,
                                      flickr_location.coordinates,
                                      json.dumps(raw_json)))
                    self.conn.commit()
                except psycopg2.IntegrityError:
                    self.conn.rollback()
                    pass
        except Exception as e:
            logging.error(e)
            pass
