import configparser
import os
import sys
import logging
import multiprocessing
from itertools import repeat

from crawler.src.FlickrApiScrap import FlickrApiScrap


def warp(args):
    FlickrApiScrap(*args)

def main():
    # Get the parameters from setup.cfg.
    path_home = os.path.dirname(os.path.realpath(__file__)) + '/crawler'
    cfg = configparser.ConfigParser()
    cfg.read(path_home + '/setup.cfg')

    # Create error log file.
    logging.basicConfig(filename=sys.argv[0].split(".")[0] + '.log',
                        format='%(asctime)s\t%(name)s\t[%(process)d]\t'
                               '%(processName)s\t%(threadName)s\t'
                               '%(module)s\t%(funcName)s\t%(lineno)d\t'
                               '%(levelname)s:%(message)s',
                        level=logging.ERROR)

    # List of parameters of configuration to create the connections threads.
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

            # Format bounding box.
            if len(bounding_box_format) > 2:
                for k, geo in enumerate(bounding_box_format):
                    bounding_box_format[k] = (float(geo))
            else:
                bounding_box_format = None
            bounding_box.append(bounding_box_format)

        pool = multiprocessing.Pool(len(cfg.sections()))
        crawler_args = zip(repeat(path_home), cfg.sections(), conn_schema,
                           conn_table, api_key, api_secret, images_path,
                           videos_path, bounding_box, search_word, time_lag)
        pool.map(warp, crawler_args)

    except Exception as e:
        logging.error(e)
        exit(0)

if __name__ == '__main__':
    main()
