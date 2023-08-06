class RadarSatellite:
    imsradar_images: list
    radar_images: list
    middle_east_satellite_images: list
    europe_satellite_images: list

    def __init__(self,imsradar_images: list=[], radar_images: list=[],middle_east_satellite_images: list=[],europe_satellite_images: list=[]):
        self.imsradar_images = imsradar_images
        self.radar_images = radar_images
        self.middle_east_satellite_images = middle_east_satellite_images
        self.europe_satellite_images = europe_satellite_images