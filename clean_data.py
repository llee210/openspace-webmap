# Lucy Lee
# March 2018
#
# Code to clean MassGIS OpenSpace shapefile

import sys
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
# create_str_date
#
# creates a text field that is a copy of the date field (MM/DD/YYYY).
# this is done in order to slice the string date to create a year field.
# datetime methods for string formatting do not cover years prior to 1900,
# which are present in the MassGIS shapefile, so this method is done instead.
##########

def create_str_date(in_table, date_field):
    new_field = "STR_DATE"
    try:
        arcpy.AddField_management(in_table, new_field, "TEXT")
        with arcpy.da.UpdateCursor(in_table, [new_field, date_field]) as cursor:
            for row in cursor:
                if row[1] is not None:
                    row[0] = row[1]
                else:
                    row[0] = 0   # If unknown set to 0 because field is not nullable
                cursor.updateRow(row)
        del row
        del cursor
    except Exception:
        pass


##########
# create_year_field
#
# creates a year field from existing date field
# call create_str_date and deletes the new string date field
# new field is short integer
##########

def create_year_field(in_table, year_field, date_field):
    
    # Create string copy of date field and new integer year field
    try:
        create_str_date(in_table, date_field)
        arcpy.AddField_management(in_table, year_field, "SHORT")
    except Exception:
        pass

    # Create the year field using the string date field
    str_date_field = "STR_DATE"
    fields = [year_field, str_date_field]

    # Update year field with year or 0 if unknown
    with arcpy.da.UpdateCursor(in_table, fields) as cursor:
        for row in cursor:
            if row[1] != "0":
                row[0] = row[1][-4:]
            else:
                row[0] = row[1]
            cursor.updateRow(row)
    del row
    del cursor

    # Delete the string date field to keep attribute table clean
    arcpy.DeleteField_management(in_table, str_date_field)

    print "Done! Short integer field", year_field, "created in", in_table



# Trim the openspace attribute table to retain only most relevant fields
##keep_fields = ["FID", "Shape", "TOWN_ID", "SITE_NAME", "FEE_OWNER", "PUB_ACCESS", \
##               "LEV_PROT", "GIS_ACRES", "CAL_DATE_R"]
##del_fields(shp, keep_fields)

# Create year field
shp = "OPENSPACE_POLY.shp"
create_year_field(shp, "YEAR", "CAL_DATE_R")
