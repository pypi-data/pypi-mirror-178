use geo::{ChaikinSmoothing, Polygon, Simplify};

pub fn smooth_simplify_polygons(polygons: Vec<Polygon>, epsilon_m: &f64) -> Vec<Polygon> {
    polygons
        .into_iter()
        .map(|p| p.chaikin_smoothing(2).simplify(epsilon_m))
        .collect()
}
