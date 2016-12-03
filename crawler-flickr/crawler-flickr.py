__title__ = 'crawler-flickr'
__author__ = 'Sidgley Camargo de Andrade'
__license__ = 'GPLv3'

import configparser
import os
import sys
import logging
import time

from crawler.src.FlickrApiScrap import FlickrApiScrap

''' main function '''
if __name__ == '__main__':

    path_home = os.getcwd() + '/crawler'

    cfg = configparser.ConfigParser()
    cfg.read(path_home + '/setup.cfg')

    ''' creates log file '''
    logging.basicConfig(filename=sys.argv[0].split(".")[0] + '.log',
                        format='%(asctime)s\t %(name)s\t [%(process)d] %(processName)s\t %(threadName)s\t %(module)s\t %(funcName)s\t %(lineno)d \t %(levelname)s:%(message)s',
                        level=logging.ERROR)

    ''' initial variables of connections '''
    api_key = []
    api_secret = []
    bounding_box = []
    search_word = []
    images_path = []
    videos_path = []
    conn_table = []
    conn_schema = []
    time_lag = []
    
    try:
        ''' get parameters from config file '''
        for conn in cfg.sections():
            params = cfg.items(conn)
            bounding_box_format = ''

            for param in params:
                if param[0] == 'connection.api_key': api_key.append(param[1])
                if param[0] == 'connection.api_secret': api_secret.append(param[1])                
                if param[0] == 'connection.bounding_box': bounding_box_format = param[1].split(',')
                if param[0] == 'connection.search_word': search_word.append(param[1].split(',')[0]) if param[1].split(',')[0] != '' else search_word.append(None)                
                if param[0] == 'connection.images_path': images_path.append(param[1])
                if param[0] == 'connection.videos_path': videos_path.append(param[1])
                if param[0] == 'connection.time_lag': time_lag.append(int(param[1]))
                if param[0] == 'database.table': conn_table.append(param[1].split(',')[0])
                if param[0] == 'database.schema': conn_schema.append(param[1].split(',')[0])

            ''' format bounding box '''
            if (len(bounding_box_format)>2):
                for k, geo in enumerate(bounding_box_format):
                    bounding_box_format[k] = (float(geo))
            else:
                bounding_box_format = None
            bounding_box.append(bounding_box_format)

        crawler = list()

        for i, conn in enumerate(cfg.sections()):
            crawler.append(
                FlickrApiScrap(path_home=path_home, conn_sec=conn, schema=conn_schema[i], table=conn_table[i],
                               api_key=api_key[i], api_secret=api_secret[i], images_path=images_path[i],
                               videos_path=videos_path[i], geo=bounding_box[i], searchword=search_word[i], time_lag=time_lag[i]))
        while True:
            for i, conn in enumerate(cfg.sections()):
                if not crawler[i].isAlive():
                    crawler[i].start()
            time.sleep(10)

    except Exception as e:
        logging.error(e)
        exit(0)