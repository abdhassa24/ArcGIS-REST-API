from arcgis.gis import GIS                             
from arcgis.features import FeatureLayerCollection
from arcgis.features import FeatureSet

gis = GIS("Home") 
# Item ID Feature Service
item_id = ""
#Retrieve Feature Service
flc_item = gis.content.get(item_id)    
flc = FeatureLayerCollection.fromitem(flc_item)

# Retrieve Server Generation Number To Extract Changes
server_gen = flc.properties.changeTrackingInfo.layerServerGens[0].serverGen

# Call extract changes and only interested in deleted features
changes = flc.extract_changes(
    layers=[0],
    servergen= server_gen,   
    return_inserts=False,
    return_updates=False,
    return_deletes=True
)

deletes = changes["edits"][0]["features"].get("deletes", [])

feature_list = []

for feat in deletes:
    geom = feat.get("geometry")

    # skip only truly invalid geometry
    if geom is None:
        continue

    feature_list.append({
        "attributes": feat.get("attributes"),
        "geometry": geom
    })

if not feature_list:
    raise Exception("No valid features.")

feature_set = FeatureSet.from_dict({"features": feature_list})

feature_set.spatial_reference = {"wkid": 3857}

feature_layer = flc.layers[0]

# Add Deleted Features back to the Feature Service
for feature in feature_set:
    add_features = feature_layer.edit_features(adds=[feature])
    print ("Successfully added features")