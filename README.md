# crawler-flickr

crawler-flickr is an implementation multi-bounding-box using flickrapi and postgresql to collect and store Flickr messages (structured and json format)

## Dependencies

* python 2.7
* libraries available in the file requirements.txt
* postgresql
* postgis

### Installation

* To create a database with the extension postgis. It is not necessary to create tables, the crawler-flickr creates the tables from template (crawler/template-table.sql)
* To configure the file setup.cfg (connections with bounding box or search word)

## Environment configuration

### with Virtual Environment

    $ chmod +x crawler-flickr-cfg-env.sh
    $ ./crawler-flickr-cfg-env.sh
    $ source .virtual/bin/activate

### without Virtual Environment

* To install all python libraries  (requirements.txt)

## Usage

     $ python crawler-flickr.py
     
## Contact

If you believe you have found a bug, or would like to ask for a feature, please inform me at sidgleyandrade@utfpr.edu.br.

## License

This software is licensed under the GPLv3.
