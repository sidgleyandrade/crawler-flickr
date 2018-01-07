# crawler-flickr

**crawler-flickr** is an implementation multi-bounding-box using flickrapi and postgresql to collect and store Flickr messages (structured and json format).

## Dependencies

* python 2.7 or greater
* libraries available in the `requirements.txt` file
* PostgreSQL 9.5 or greater
* PostGIS 2.0 or greater

## Instalation

    $ git clone https://github.com/sidgleyandrade/crawler-flickr.git
    
## Configuration

* To create a database with the extension postgis. It is not necessary to create tables, **crawler-flickr** will create the tables from the config file parameters (`segup.cfg`).
* To configure the connections in the `setup.cfg` file, as follow:

    * __Bounding box connection__

    ```
    [connection_name]
    connection.user=nickname
    connection.api_key=1a123abcd123ab1a1a123456ab1a12a1a
    connection.api_secret=123a1231a123123a
    connection.bounding_box=-74.0,-33.9,-28.6,5.3
    connection.search_word=
    connection.images_path=.    (this feature is not available yet)
    connection.videos_path=.    (this feature is not available yet)
    connection.time_lag=1       (number of prior days to start the collection)
    database.host=MyHost
    database.schema=MyShcema
    database.name=MyDatabase
    database.table=MyTableName
    database.user=MyUserName
    database.password=MyPassword
    
    ```
        
    * __Search word connection__

    ```
    [connection_name]
    connection.user=nickname
    connection.api_key=1a123abcd123ab1a1a123456ab1a12a1a
    connection.api_secret=123a1231a123123a
    connection.bounding_box=-74.0,-33.9,-28.6,5.3
    connection.search_word=rainfall
    connection.images_path=.    (this feature is not available yet)
    connection.videos_path=.    (this feature is not available yet)
    connection.time_lag=1       (number of prior days to start the collection)
    database.host=MyHost
    database.schema=MyShcema
    database.name=MyDatabase
    database.table=MyTableName
    database.user=MyUserName
    database.password=MyPassword
    ```

**Note:** `connection.bounding_box` and `connection.search_word` are exclusive parameters.

#### Getting Flickr credentials for apps
 
See [https://www.flickr.com/services/apps/create/](https://www.flickr.com/services/apps/create/).

## Running

    $ chmod +x run.sh
    $ ./run.sh

## Known issues

See [issues](https://github.com/sidgleyandrade/crawler-twitter/issues).

## Contact

If you believe you have found a bug, or would like to ask for a feature or contribute to the project, please inform me at sidgleyandrade[at]utfpr[dot]edu[dot]br.

## License

This software is licensed under the GPLv3.
