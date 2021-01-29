__version__ = '0.1'
__author__ = 'Paul Millar'
__description__ = """

location.py
-----------

Contains functions and classes for dealing with Androids Location API
 Features include:

 GPSListener - A class for retrieving GPS location data
"""

from jnius import autoclass
from jnius import PythonJavaClass
from jnius import java_method

# reflect our Android classes from the Android SDK

LocationManager = autoclass("android.location.LocationManager")
Looper = autoclass("android.os.Looper")
PythonActivity = autoclass('org.kivy.android.PythonActivity')
Context = autoclass("android.content.Context")


class GpsListener(PythonJavaClass):

    __javainterfaces__ = ["android/location/LocationListener"]

    def __init__(self, func_callback, **kwargs):
        super().__init__(**kwargs)
        self.func_callback = func_callback
        self.location_manager = PythonActivity.mActivity.getSystemService(
            Context.LOCATION_SERVICE
        )
    
    def start_gps_updates(self, time_interval, min_dist):
        """
        time_interval - int
            minimum time interval between location updates in milliseconds
        min_dist - float
            minimum distance between location updates in meters
        """
        self.location_manager.requestLocationUpdates(
            LocationManager.GPS_PROVIDER,
            time_interval,
            min_dist,
            self,
            Looper.getMainLooper()
        )
    
    def stop_gps_updates(self):
        """
        stop listening for GPS updates
        """
        self.location_manager.removeUpdates(self)
    
    @java_method('()I')
    def hashCode(self):
        """
        should be return id(self) but gives int to large for C long type
        error. return 1 instead
        """
        return 1
    
    @java_method('(Landroid/location/Location;)V')
    def onLocationChanged(self, location):
        self.func_callback(self, "location", location)
    
    @java_method('(Ljava/lang/String;)V')
    def onProviderEnabled(self, provider):
        self.func_callback(self, "provider_disabled", provider)
    
    @java_method('(Ljava/lang/String;)V')
    def onProviderDisabled(self, provider):
        self.func_callback(self, "provider_disabled", provider)
    
    @java_method('(Ljava/lang/Object;)Z')
    def equals(self, obj):
        return obj.hashCode() == self.hashCode()