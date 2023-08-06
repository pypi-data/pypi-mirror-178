use geo::{GeometryCollection, Polygon};
use geojson::FeatureCollection;
use std::iter::FromIterator;

pub fn make_fc_from_polygons(polygons: Vec<Polygon>) -> FeatureCollection {
    FeatureCollection::from(&GeometryCollection::from_iter(polygons))
}
