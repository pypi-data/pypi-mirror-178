
def smooth_and_simplify_polygon_fc(geojson: str, simplify_tolerance_m: float) -> str:
    """
    Reads polygons from GeoJSON FeatureCollection, smoothens and simplifies them.
    The FeatureCollection must container only Polygons (and/or MultiPolygons). 
    Expects the coordinates in the GeoJSON to be in meters.
    
    Returns GeoJSON FeatureCollection as string.
    """
    pass
