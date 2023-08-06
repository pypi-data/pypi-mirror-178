use geo::{MultiPolygon, Polygon};
use geojson::{FeatureCollection, GeoJson, Value};

fn collect_polygons_from_fc(fc: &FeatureCollection) -> Vec<Polygon> {
    let mut v: Vec<Polygon<f64>> = Vec::new();
    fc.features.iter().for_each(|f| {
        if let Some(ref geom) = f.geometry {
            match geom.value {
                Value::Polygon(_) => {
                    v.push(Polygon::try_from(geom).expect("Unable to read Polygon"))
                }
                Value::MultiPolygon(_) => v.extend(
                    MultiPolygon::try_from(geom)
                        .expect("Unable to read MultiPolygon")
                        .into_iter(),
                ),
                _ => (),
            }
        }
    });
    v
}

pub fn read_polygons_from_feature_collection(geojson_str: &str) -> Option<Vec<Polygon>> {
    let geojson: GeoJson = geojson_str.parse::<GeoJson>().unwrap();
    if let GeoJson::FeatureCollection(fc) = geojson {
        return Some(collect_polygons_from_fc(&fc));
    }
    None
}

#[cfg(test)]
mod tests {
    use super::*;

    static GEOJSON_STR: &str = r#"
    {
        "type": "FeatureCollection",
        "features": [
          {
              "type": "Feature",
              "properties": {},
              "geometry": {
                  "coordinates": [
                      [
                          [
                              24.92790821679094,
                              60.17593029781693
                              ],
                  [
                    24.92790821679094,
                    60.17405034530347
                  ],
                  [
                    24.930878152539776,
                    60.17405034530347
                    ],
                    [
                        24.930878152539776,
                        60.17593029781693
                  ],
                  [
                    24.92790821679094,
                    60.17593029781693
                    ]
                    ]
                    ],
                    "type": "Polygon"
                }
            }
        ]
      }
    "#;

    #[test]
    fn test_read_polygons_from_feature_collection() {
        let result = read_polygons_from_feature_collection(GEOJSON_STR);
        assert!(result.is_some());
        assert_eq!(result.expect("empty/invalid GeoJSON").len(), 1);
    }
}
