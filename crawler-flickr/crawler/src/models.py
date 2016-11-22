class FlickrMessage():
    def __init__(self):
        self.id = None
        self.secret = None
        self.created_at = None
        self.date = None
        self.isfavorite = None
        self.license = None
        self.safety_level = None
        self.farm = None
        self.title = None
        self.ispublic = None
        self.isfriend = None
        self.isfamily = None
        self.description = None
        self.views = None
        self.comments = None
        self.tags = []
        self.media = None
        self.urls = []


class FlickrOwner():
    def __init__(self):
        self.nsid = None
        self.username = None
        self.location = None


class FlickrLocation():
    def __init__(self):
        self.id = None
        self.accuracy = None
        self.locality = None
        self.county = None
        self.region = None
        self.country = None
        self.longitude = None
        self.latitude = None
        self.coordinates = None
