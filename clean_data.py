# Lucy Lee
# March 2018
#
# Code to clean MassGIS OpenSpace shapefile


import arcpy

arcpy.env.workspace = "X:/openspace"
arcpy.env.overwriteOutput = True


##########
# del_fields
#
# allows user to delete fields by specifying a list of fields to keep
##########

def del_fields(shp, keep_fields):
    
    # make a copy to preserve original
    arcpy.CopyFeatures_management(shp, shp[:-4] + "_copy.shp")
    
    fields = arcpy.ListFields(shp)
    
    del_fields = [x.name for x in fields if x.name not in keep_fields]

    arcpy.DeleteField_management(shp, del_fields)

    print "Deleted fields", del_fields


# Trim the openspace attribute table to retain only most relevant fields
shp = "OPENSPACE_POLY.shp"
keep_fields = ["FID", "Shape", "TOWN_ID", "SITE_NAME", "FEE_OWNER", "PUB_ACCESS", \
               "LEV_PROT", "GIS_ACRES", "CAL_DATE_R"]
del_fields(shp, keep_fields)



# next: create year field from date field

