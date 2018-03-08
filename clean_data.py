# Lucy Lee
# March 2018
#
# Code to clean MassGIS OpenSpace shapefile

import sys
from datetime import date
try:
    import arcpy
except ImportError:
    print "Error importing ArcPy."

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



##########
# create_year_field
#
# creates a year field from existing date field
# new field is short integer
##########

def create_year_field(in_table, year_field, date_field):
    
    # Check to see if the new field to create already exists
    try:
        arcpy.AddField_management(in_table, year_field, "SHORT")
    except Exception:
        # If the field exists, ask user if they wish to overwrite
        q = int(raw_input("Field " + year_field + " already exists. Overwrite years?" + \
                      "\nEnter 1 for yes and 0 for no:   "))
        
    # If the user wants to overwrite years, do that    
    if q == 1:
        try:
            # Make a string copy of the date field to enable string slicing
            arcpy.AddField_management(in_table, "STR_DATE", "TEXT")
            with arcpy.da.UpdateCursor(in_table, ["STR_DATE", date_field]) as cursor:
                for row in cursor:
                    if row[1] is not None:
                        row[0] = row[1]
                    else:
                        row[0] = 0    # If unknown set to zero because shp is not nullable
                    cursor.updateRow(row)
        except Exception:
            pass

        # Create the year field using the string 
        fields = [year_field, "STR_DATE"]

        with arcpy.da.UpdateCursor(in_table, fields) as cursor:
            for row in cursor:
                if row[1] != "0":
                    year = row[1][-4:]
                    row[0] = int(year)
                else:
                    row[0] = row[1]    # Set year to 0 if unknown
                cursor.updateRow(row)
        del row
        del cursor
        try:
            arcpy.DeleteField_management(in_table, "STR_DATE")
        except Exception:
            pass
        print 'Done!'
    # Otherwise, exit 
    elif q == 0:
        sys.exit()
    else:
        print "Not a recognized response. Exiting function."
        sys.exit()
    

shp = "OPENSPACE_POLY.shp"
create_year_field(shp, "YEAR", "CAL_DATE_R")

    
## CAL_DATE_R

# Trim the openspace attribute table to retain only most relevant fields
##keep_fields = ["FID", "Shape", "TOWN_ID", "SITE_NAME", "FEE_OWNER", "PUB_ACCESS", \
##               "LEV_PROT", "GIS_ACRES", "CAL_DATE_R"]
##del_fields(shp, keep_fields)
