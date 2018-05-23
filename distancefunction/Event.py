from datetime import datetime


class Event:
    def __init__(self, id, lon, lat, event_date, end_date, population, socioeconomic=None, infrastructure=None, name=None):
        self.id = id
        self.lon = lon
        self.lat = lat
        self.event_date = event_date
        self.end_date = end_date
        self.population = population
        self.socioeconomic = socioeconomic
        self.infrastructure = infrastructure
        self.name = name

    def get_date_sting(self):
            return datetime.strftime(self.date, '%Y%m%d')

    def get_sociovar_count(self):
        if self.socioeconomic is None:
            return 0
        return len(self.socioeconomic)

    def get_infravar_count(self):
        if self.infrastructure is None:
            return 0
        return len(self.infrastructure["proximity"])