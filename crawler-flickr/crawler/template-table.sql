CREATE TABLE IF NOT EXISTS %s.%s (
    id TEXT NOT NULL,
    secret TEXT NULL,
    isfavorite INT NULL,
    license INT NULL,
    safety_level INT NULL,
    created_at TIMESTAMP NOT NULL,
    date DATE NULL,
    farm INT NULL,
    title TEXT NULL,
    visibility_ispublic INT NULL,
    visibility_isfriend INT NULL,
    visibility_isfamily INT NULL,
    description TEXT NULL,
    views INT NULL,
    comments INT NULL,
    tags TEXT[] NULL,
    location_accuracy INT NULL,
    location_locality TEXT NULL,
    location_county TEXT NULL,
    location_region TEXT NULL,
    location_country TEXT NULL,
    owner_nsid TEXT NULL,
    owner_username TEXT NULL,
    owner_location TEXT NULL,
    media TEXT NULL,
    urls TEXT[],
    flickr JSON,
    CONSTRAINT %s_pk PRIMARY KEY (id)
);

SELECT AddGeometryColumn ('%s','%s','coordinates', 4326, 'POINT', 2)
WHERE NOT EXISTS (SELECT column_name FROM information_schema.columns
		  WHERE	table_schema = '%s' AND
		        table_name ='%s' AND
			    column_name = 'coordinates');

CREATE INDEX IF NOT EXISTS date_%s_ix ON %s.%s (date);
