''' Extract GPS & Exif Data from Images using Python
    November 21, 2017 · Justin Mitchel
    https://www.codingforentrepreneurs.com/blog/extract-gps-exif-images-python/ '''

import os
import re
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import exifread
import hachoir

def dt_from_name(  filename   )  -> str:
    x = re.search(   "20[0-9][0-9]"
                       "[0-1][0-9]"
                       "[0-3][0-9]"
                       "_"
                       "[0-2][0-9]"
                       "[0-5][0-9]"
                       "[0-5][0-9]",   filename   )
    return   x.group()
# print(  'dt_from_name()   =>   ',   end=''   )
# print(   dt_from_name( "sdkjlfh asj 180731wto200219 ___20180731_200219se .jpg_sdkj" )   )
''' dt_from_name()   =>   20180731_200219 '''
# print(  'dt_from_name()   =>   ',   end=''   )
# print(   dt_from_name(   ''' 180708nie050918 NIEBO[+++++]zborzeOwies ___20180708_050918_HDR.jpg '''   )   )
''' dt_from_name()   =>   20180708_050918 '''


def TheOnlyHumanReadableDateTimeFormatString(datetime_object): # : datetime.datetime) -> str:
    nDT = nowDayTime_string = str(datetime_object)
    dayOfWeekSlownik = {0: "pon", 1: "wto", 2: "śro", 3: "czw", 4: "pią",
                                                      5: "sob", 6: "nie"  }
    trzyLiterki = dayOfWeekSlownik[ (  datetime_object.weekday()  ) ]

    datetime_string_TheOnlyFormat =   nDT[ 2: 4] + nDT[ 5: 7] + nDT[ 8:10]  \
                                    + str(trzyLiterki)                      \
                                    + nDT[11:13] + nDT[14:16] + nDT[17:19]

    return datetime_string_TheOnlyFormat
TheOnlyTime = TheOnlyHumanReadableDateTimeFormatString


class ImageMetaData(object):
    ''' Extract the exif data from any image.
        Data includes GPS coordinates, Focal Length, Manufacture, and more. '''
    exif_data = None
    image = None

    def __init__(self, img_path):
        self.image = Image.open(img_path)
        #print(self.image._getexif())
        self.get_exif_data()
        super(ImageMetaData, self).__init__()

    def get_exif_data(self):
        """ Returns a dictionary from the exif data of an PIL Image item. Also converts the GPS Tags """
        exif_data = {}
        info = self.image._getexif()
        if info:
            for tag, value in info.items():
                decoded = TAGS.get(tag, tag)
                if decoded == "GPSInfo":
                    gps_data = {}
                    for t in value:
                        sub_decoded = GPSTAGS.get(t, t)
                        gps_data[sub_decoded] = value[t]

                    exif_data[decoded] = gps_data
                else:
                    exif_data[decoded] = value
        self.exif_data = exif_data
        return exif_data

    def get_if_exist(self, data, key):
        if key in data:
            return data[key]
        return None

    def convert_to_degress(self, value):
        """ Helper function to convert the GPS coordinates
            stored in the EXIF to degrees in float format """

        # print()
        # print(   type(        value[0][0] )                  ,end='\t'   ) # <class 'int'>	50
        # print(                value[0][0]                                )
        # print(   type( float( value[0][0] ) )                ,end='\t'   ) # <class 'float'>	50.0
        # print(         float( value[0][0] )                              )
        #
        # print(         float( value[0][0] )   /   float( value[0][1] )   ) # 50.0
        # print(         float( value[0][0] )   /   float( value[0][1] )   ) # 50.0
        ''' the same - so why floating it ? '''
        # print(   type(        value[1][0] )                  ,end='\t'   ) # <class 'int'>	6
        # print(                value[1][0]                                )
        # print(   type( float( value[1][0] ) )                ,end='\t'   ) # <class 'float'>	6.0
        # print(         float( value[1][0] )                              )
        #
        # print(         float( value[1][0] )   /   float( value[1][1] )   ) # 6.0
        # print(         float( value[1][0] )   /   float( value[1][1] )   ) # 6.0
        ''' the same - so why floating it ? '''

        deg  =    value[0][0] \
                / value[0][1]

        min  =    value[1][0] \
                / value[1][1]

        sec  =    value[2][0] \
                / value[2][1]

        return    deg  +  (min/60.0)  +  (sec/3600.0)

    def get_lat_lng(self):
        """ Returns the latitude and longitude, if available,
            from the provided exif_data (obtained through get_exif_data above) """
        lat = None
        lng = None
        exif_data = self.get_exif_data()
        # print(  str( exif_data ).replace(  r'\x00',  ''  )  )
        if "GPSInfo" in exif_data:
            gps_info = exif_data["GPSInfo"]
            gps_latitude      = self.get_if_exist(   gps_info,  "GPSLatitude"      )
            gps_latitude_ref  = self.get_if_exist(   gps_info,  'GPSLatitudeRef'   )
            gps_longitude     = self.get_if_exist(   gps_info,  'GPSLongitude'     )
            gps_longitude_ref = self.get_if_exist(   gps_info,  'GPSLongitudeRef'  )
            if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
                lat = self.convert_to_degress( gps_latitude  )
                if gps_latitude_ref  != "N":
                    lat = 0 - lat
                lng = self.convert_to_degress( gps_longitude )
                if gps_longitude_ref != "E":
                    lng = 0 - lng
            # gps_altitude = self.get_if_exist(  gps_info,  'GPSAltitude'  )

        return lat, lng # , gps_altitude


def altitude_str(  some_exif_data:object  ) -> str:
    exif_data = some_exif_data

    try:
        # print(   exif_data['GPSInfo']['GPSAltitudeRef']   )
        if exif_data['GPSInfo']['GPSAltitudeRef'] == b'\x00'  :
            znak_lustra_wody = +1   ;       znak = '+'      ;       jednostki = 'mnpm'
        else :
            znak_lustra_wody = -1   ;       znak = '-'      ;       jednostki = 'mppm(depresja)'

        GPS_Altitude = "".join(  [  str( znak                                                ),
                                    str( round(   exif_data['GPSInfo']['GPSAltitude'][0]
                                                / exif_data['GPSInfo']['GPSAltitude'][1]   ) ),
                                    str( jednostki                                           )  ]  )
        return GPS_Altitude
    except:
        return ''

def camera_model(  some_exif_data:object  ) -> str:
    exif_data = some_exif_data
    exif_data_Model = ""
    market_camera_name = ""                 #;        print(   exif_data['Model']   )

    if    exif_data['Model'] == 'LG-H870':
        exif_data_Model     =  exif_data[ 'Model' ].replace(  '-',  '·'  )
        market_camera_name  =  "_LG·G6"    #;        print(   'LG-H870 ≈ LG-G6'      )

    elif  exif_data['Model'] == 'Quantum_350Lite':
        exif_data_Model     =  exif_data[ 'Model' ].replace(   '_',   ''   )
        market_camera_name  =  "·GoClever" #;        print(   'Quantum_350Lite ≈ GoClever'   )

    return f"Model_{  exif_data_Model  }{  market_camera_name  }"




dictionary = {}

def main():
    files = os.listdir(".")
    # for file in files:    print( file )
    index = 0

    for file_name in files:
        if         file_name[ -4 : ].lower() == '.jpg' :
              # or   file_name[ -4 : ].lower() == '.gif'
            ''' PIL.UnidentifiedImageError: cannot identify image file '20181018_224418.mp4' '''
              # or   file_name[ -4 : ].lower() == '.mp4' :
            ''' AttributeError: 'GifImageFile' object has no attribute '_getexif' '''
            print(   '\n\t\t\t\t  ',   file_name    )
            ''' 180708nie052739 ___20180708_052739_HDR.jpg '''
            index += 1

            # print('  nameTime:',                                                        end='   ')
            current_datetime_str = dt_from_name(  file_name  )
            # print(   current_datetime_str,                                              end='   ')
            # print(                    datetime.strptime(  current_datetime_str, '%Y%m%d_%H%M%S'  )   ) ;''' 2018-07-08 05:27:39 '''
            datetime_object_from_name = datetime.strptime(  current_datetime_str, '%Y%m%d_%H%M%S'  )
            # print(   datetime_object_from_name,                                                  )


            ### Times from OS Operating System ###
            ''' # mod tend to be close to the true but not enough ! ! !
                # photo was   ctrl+X  &  ctrl+V                             '''
            # print('  mod_time:',                                                      end='   ')
            current_from_mod_time_stamp = os.path.getmtime(  file_name  )                           ; ''' 1531020460.0 '''
            # print(   current_from_mod_time_stamp,                                     end='   ')  ; ''' 1531020460.0 '''
            datetime_object_mod_time = datetime.fromtimestamp(  current_from_mod_time_stamp  )      ; ''' 2018-07-08 05:27:40 '''
            # print(   datetime_object_mod_time                                                  )  ; ''' 2018-07-08 05:27:40 '''

            # print('  cre_time:',                                                      end='   ')
            current_from_creation_time_stamp = os.path.getctime(  file_name  )                      ; ''' 1580918846.2050345 '''
            # print(   current_from_creation_time_stamp,                                end='   ')  ; ''' 1580918846.2050345 '''
            datetime_object_cre_time = datetime.fromtimestamp(  current_from_creation_time_stamp  ) ; ''' 2020-02-05 17:07:26.205034 '''
            # print(   datetime_object_cre_time                                                  )  ; ''' 2020-02-05 17:07:26.205034 '''

            # print('  acc_time:',                                                      end='   ')  ; """Return the last access time of a file, reported by os.stat()."""
            current_from_access_time_stamp = os.path.getatime(  file_name  )                        ; ''' 1583826197.3921168 '''
            # print(   current_from_access_time_stamp,                                  end='   ')  ; ''' 1583826197.3921168 '''
            datetime_object_access_time = datetime.fromtimestamp(  current_from_access_time_stamp  ); ''' 2020-03-10 08:43:17.392117 '''
            # print(   datetime_object_access_time                                               )  ; ''' 2020-03-10 08:43:17.392117 '''
            '''   20181009_142757_Burst13.jpg
                  nameTime:   20181009_142757      2018-10-09 14:27:57
                  mod_time:   1539088080.0         2018-10-09 14:28:00
                  cre_time:   1583602087.2259052   2020-03-07 18:28:07.225905
                  acc_time:   1583602087.2259052   2020-03-07 18:28:07.225905
            # photo was   ctrl+C  &  ctrl+V                                   '''

            # GPS Latitude, Longitude
            path_name = file_name
            meta_data = ImageMetaData(path_name)
            LatLong = meta_data.get_lat_lng() # round 6 = 111 mm of accuracy = 11 cm.
            # print( LatLong ) # (50.06741116666667, 19.92924505555556)
            exif_data = meta_data.get_exif_data()
            # print(  str( exif_data ).replace(  r'\x00',  ''  )  )

            Lati,  Long,  Altitude  =  'No',  'GPS',  ''
            if   LatLong   !=   (None, None):
                Lati = round(  LatLong[0],  6  ) # 50.067411
                # print( Lati )                  # 50.067411
                Long = round(  LatLong[1],  6  ) # 19.929245
                # print( Long )                  # 19.929245



            # GPS Altitude

            # print(      f"GPSAltitude={   znak   }"
            #           # f"{     int(   exif_data['GPSInfo']['GPSAltitude'][0]   /   exif_data['GPSInfo']['GPSAltitude'][1]   )   }"
            #             f"{   round(   exif_data['GPSInfo']['GPSAltitude'][0]   /   exif_data['GPSInfo']['GPSAltitude'][1]   )   }"
            #             f"{   jednostki   }"   ) # GPSAltitude=+279mnpm

            Altitude = altitude_str(  exif_data  )      ;''' Alt+279mnpm '''
            # print(   altitude_str(  exif_data  )   )

            CamModel = camera_model(  exif_data  )      ;''' Model_LG·H870_LG·G6 '''   ''' Model_LG-H870(LG-G6) '''
            # print(     camera_model(  exif_data  )   )



            new_file_name = ''
            part_file_name  =  file_name.replace(   f'IMG_{  current_datetime_str  }',   ""          )   \
                                        .replace(            current_datetime_str    ,   ""          )   \
                                        .replace(            "_HDR."                 ,   "__HDR."    )   \
                                        .replace(            "_Burst"                ,   "__Burst"   )
            print(   '\t\t\t\t\t\t\t\t ',   part_file_name   );''' __HDR.jpg '''


            if   LatLong   ==   (None, None):
                new_file_name = f'{   TheOnlyTime( datetime_object_from_name )   }'          \
                                f' ___NoGPS'                                                 \
                                f'__{  CamModel   }'                                         \
                                f'{  part_file_name  }'   # f'{  file_name  }'
            else:
                new_file_name = f'{   TheOnlyTime( datetime_object_from_name )   }'          \
                                f' ___GPS {Lati},{Long} {Altitude}'                          \
                                f'__{  CamModel   }'                                         \
                                f'{  part_file_name  }'   # f'{  file_name  }'
            print(   new_file_name   )                              ;''' 180708nie052739 ___180708nie052739 ___20180708_052739_HDR.jpg '''



            dictionary[ file_name ]  =  new_file_name
            # os.rename(   file_name,   new_file_name   )



    print('\n')
    for elem in dictionary:
        print(   f'\n\t\t\t\t   {  elem  }\n{  dictionary[elem]  }'   )
        # os.rename(   elem,   dictionary[elem]   )
    the_only_time = TheOnlyTime( datetime.now() )

    if   len( dictionary )  >  0  :

        name_for_log_file   =   f'{  the_only_time  } TheOnlyTime+GPS LOG ' \
                                f'NumOfRenamedPictures{  index  }'          \
                                f' dictionary .txt'
        f = open(   name_for_log_file,   "w+"   )
        f.write(   str( dictionary )   )
        f.close();                                    print(   f'\n{  len( dictionary )  }'
                                                               f'\n{  name_for_log_file  }'   )

        name_for_log_file   =   f'{  the_only_time  } TheOnlyTime+GPS LOG ' \
                                f'NumOfRenamedPictures{  index  }'          \
                                f' HumanReadable .txt'
        f = open(   name_for_log_file,   "w+"   )
        for elem in dictionary:
            # f.write(  f'\n\t\t\t\t   {        elem  }\n{  dictionary[elem]  }\n'   )
            f.write(  f'\n                   {  elem  }\n{  dictionary[elem]  }\n'   )
        f.close();                                    print(   f'\n{  len( dictionary )  }'
                                                           f'\n{  name_for_log_file  }'   )


    # name_for_log_file   =   f'{  TheOnlyTime( datetime.now() )  } TheOnlyTime+GPS LOG NumOfRenamedPhotos{  index  } .csv'
    # print(   name_for_log_file   )
    #
    # import csv
    # w  =  csv.writer( open(   name_for_log_file,   "w"   ) )
    # for key, val in dictionary.items():
    #     w.writerow(  [key, val])




if __name__ == "__main__":
    main()
