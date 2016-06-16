import argparse
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import webbrowser

def whereImg(imageName, nogmap):
    try:
        metadata = {}
        gpsinfo= {}
        
        imageFile = Image.open(imageName)
        print("Extracting Data..")
        info = imageFile._getexif()

        if info:
            # Run through Exif data and store in dictionary
            for(tag, value) in info.items():
                tagName = TAGS.get(tag, tag)
                metadata[tagName] = value
                # If GPS Data found then extract and decode
                if(tagName == 'GPSInfo'):
                    for entry in metadata['GPSInfo'].keys():
                        decode = GPSTAGS.get(entry, entry)
                        gpsinfo[decode] = metadata['GPSInfo'][entry]
                        
                        if(decode == 'GPSLatitude'):
                            GPSLat = metadata['GPSInfo'][entry]
                        if(decode == 'GPSLongitude'):
                            GPSLong =  metadata['GPSInfo'][entry]
                        if(decode == 'GPSLatitudeRef'):
                            NS = metadata['GPSInfo'][entry]
                        if(decode == 'GPSLongitudeRef'):
                            EW = metadata['GPSInfo'][entry]                        
            # If nogmap flag is set then print Lat and Long
            if nogmap:
                print("Latitude: ", NS, GPSLat)
                print("Longitude: ", EW, GPSLong)
            else:
                extractCoOrd(GPSLat, GPSLong, NS, EW)

        else:
            print("No data found!")

    except:
        print("Failed. Probably no file exists with this name!", e)

def extractCoOrd(GPSLat, GPSLong, NS, EW):
    lat = [float(x)/float(y) for x, y in GPSLat]
    lon = [float(x)/float(y) for x, y in GPSLong]

    # Convert to decimal values from DMS for Google maps
    lat = lat[0] + lat[1]/60 + lat[2]/3600
    lon = lon[0] + lon[1]/60 + lon[2]/3600
    # Western and Southern Hemisphere corrections
    if(NS == 'S'):
        lat = -lat
    if(EW == 'W'):
        lon = -lon
    
    print(lat, lon)

    # Open location in Google maps via Browser
    googleMaps = "https://www.google.com/maps/place//@"
    latlongzoom = str(lat)+','+str(lon)+',20z'
    queryString = googleMaps + latlongzoom
    webbrowser.open(queryString, new=0, autoraise=True)

    
def Main():
    # Set argparse
    parser = argparse.ArgumentParser(description='Show Where the image was taken with the GPSInfo Exif data')
    parser.add_argument("imagePath", help="Path to the image file")
    parser.add_argument("--nogmap", action="store_true", help="Don't open coordinates in Google Maps")
    args = parser.parse_args()

    if args.imagePath:
        whereImg(args.imagePath, args.nogmap)
    else:
        print(parser.usage)

if __name__ == '__main__':
    Main()
    


