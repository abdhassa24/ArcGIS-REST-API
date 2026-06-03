from arcgis.gis import GIS
from arcgis.features import FeatureLayer, Table, FeatureLayerCollection

gis = GIS("https://org.maps.arcgis.com", profile= "profile")
fl_url = "https://services8.arcgis.com/orgid/arcgis/rest/services/Poles/FeatureServer/0"
tbl_url = "https://services8.arcgis.com/orgid/arcgis/rest/services/Inspection/FeatureServer/0"
tbl_2_url = "https://services8.arcgis.com/orgid/arcgis/rest/services/Pole_Info/FeatureServer/0"

fl = FeatureLayer(fl_url, gis)
tbl = Table(tbl_url, gis)
tbl_2 = Table(tbl_2_url, gis)

view_service = gis.content.create_service(name="joined_view", is_view=True)
view_flc = FeatureLayerCollection.fromitem(view_service)

sourceFeatureLayerFields = [
                              {
                                "name": "OBJECTID",
                                "alias": "OBJECTID",
                                "source": "OBJECTID"
                            },
                                {
                                "name": "GlobalID",
                                "alias": "GlobalID",
                                "source": "GlobalID"
                            },
                            {
                                "name": "Barcode",
                                "alias": "Barcode",
                                "source": "Barcode"
                            }
                        ]

sourceTableFields = [
    {
        "name": "Notes",
        "alias": "Notes",
        "source": "Notes"
    }
]

sourceTableFields_2 = [
    {
        "name": "Material",
        "alias": "Material",
        "source": "Material"
    }
]

field_to_join_on = "Barcode"
view_lyr_name = "Poles"
definition_to_add = {
  "layers": [
    {
      "name": view_lyr_name,
      "displayField": "",
      "description": "AttributeJoin",
      "adminLayerInfo": {
        "viewLayerDefinition": {
          "table": {
            "name": "Poles",
            "sourceServiceName": fl.properties.name,
            "sourceLayerId": 0,
            "sourceLayerFields": sourceFeatureLayerFields,
            "relatedTables": [
                            {
                                "name": "Inspection",
                                "sourceServiceName": tbl.properties.name,
                                "sourceLayerId": 0,
                                "sourceId": 203,
                                "sourceLayerFields": sourceTableFields,
                                "type": "LEFT",
                                "parentKeyFields": [
                                    field_to_join_on
                                ],
                                "keyFields": [
                                   field_to_join_on
                                ],
                                "operator": "EQUALS"
                            },
                            {
                                "name": "Pole_Info",
                                "sourceServiceName": tbl_2.properties.name,
                                "sourceLayerId": 0,
                                "sourceId": 203,
                                "sourceLayerFields": sourceTableFields_2,
                                "type": "LEFT",
                                "parentKeyFields": [
                                    field_to_join_on
                                ],
                                "keyFields": [
                                    field_to_join_on
                                ],
                                "operator": "EQUALS"
                            }
                        ],
                        "materialized": False
                    }
                },
                "geometryField": {
                   "name": f"{view_lyr_name}.Shape"
                }
            }
        }
    ]
}

view_flc.manager.add_to_definition(definition_to_add)
print ("Added Joined view successfully")
