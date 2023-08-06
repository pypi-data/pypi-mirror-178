use geo::Polygon;
use rayon::prelude::*;
use std::str::FromStr;
use wkt::Wkt;

fn read_polygon_from_wkt(wkt_str: &str) -> Polygon {
    Polygon::try_from(Wkt::from_str(wkt_str).expect("Unable to parse Polygon from WKT"))
        .expect("Unable to read Polygon from WKT")
}

pub fn read_polygons_from_wkts(polygon_wkts: &[&str]) -> Vec<Polygon> {
    polygon_wkts
        .par_iter()
        .map(|p| read_polygon_from_wkt(p))
        .collect::<Vec<Polygon>>()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_read_polygon_from_wkt() {
        let result = read_polygon_from_wkt("POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))");
        assert_eq!(result.exterior().coords().count(), 5);
    }

    #[test]
    fn test_read_polygons_from_wkts() {
        let wkts: Vec<&str> = [
            "POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))",
            "POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))",
        ]
        .to_vec();

        let result = read_polygons_from_wkts(&wkts);
        assert_eq!(result.iter().count(), 2);
        assert_eq!(result[0].exterior().coords().count(), 5);
    }
}
