use geo::{ChaikinSmoothing, Polygon, Simplify};
use rayon::prelude::*;

pub fn smooth_simplify_polygon(
    polygon: &Polygon,
    smoothing_iterations: usize,
    epsilon_m: &f64,
) -> Polygon {
    if smoothing_iterations == 0 {
        return polygon.simplify(epsilon_m);
    }
    polygon
        .chaikin_smoothing(smoothing_iterations)
        .simplify(epsilon_m)
}

pub fn smooth_simplify_polygons(
    polygons: Vec<Polygon>,
    smoothing_iterations: usize,
    epsilon_m: &f64,
) -> Vec<Polygon> {
    polygons
        .par_iter()
        .map(|p| smooth_simplify_polygon(p, smoothing_iterations, epsilon_m))
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::str::FromStr;
    use wkt::Wkt;

    fn read_polygon_from_wkt(wkt_str: &str) -> Polygon {
        Polygon::try_from(Wkt::from_str(wkt_str).expect("Unable to parse Polygon from WKT"))
            .expect("Unable to read Polygon from WKT")
    }

    #[test]
    fn test_smooth_simplify_polygon() {
        let polygon = read_polygon_from_wkt("POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))");
        let result = smooth_simplify_polygon(&polygon, 2, &0.5);
        assert_eq!(result.exterior().coords().count(), 17);
    }
}
