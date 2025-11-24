"""
Route Data: Bay Area Routes and Delivery Pairs

This module contains:
- Hardcoded highway route anchor points
- Densified route polylines
- Pre-generated delivery route pairs between cities
"""

from typing import List, Tuple, Dict

LatLon = Tuple[float, float]


# =============================================================================
# HIGHWAY ANCHOR ROUTES (Sparse control points)
# =============================================================================

# US-101: San Francisco (Civic Center) → San Jose (Downtown)
sf_to_sj_us101_anchors: List[LatLon] = [
    (37.7749, -122.4194),  # San Francisco City Hall
    (37.7577, -122.3953),  # Potrero Hill / 101 on-ramp area
    (37.7300, -122.3920),  # Bayview / 101 south
    (37.7060, -122.4050),  # Brisbane
    (37.6160, -122.3920),  # SFO Airport
    (37.5900, -122.3460),  # Burlingame / Millbrae
    (37.5500, -122.3040),  # San Mateo
    (37.5100, -122.2700),  # Belmont / San Carlos
    (37.4852, -122.2364),  # Redwood City
    (37.4419, -122.1430),  # Palo Alto
    (37.4040, -122.0790),  # Mountain View
    (37.3688, -122.0363),  # Sunnyvale
    (37.3541, -121.9552),  # Santa Clara
    (37.3382, -121.8863),  # Downtown San Jose
]

# I-280: San Francisco (Civic Center) → San Jose (Downtown)
sf_to_sj_i280_anchors: List[LatLon] = [
    (37.7749, -122.4194),  # SF City Hall
    (37.7440, -122.4310),  # Glen Park
    (37.7083, -122.4500),  # Daly City
    (37.6700, -122.4600),  # South of Daly City
    (37.6300, -122.4400),  # San Bruno
    (37.5900, -122.4200),  # Hillsborough
    (37.5400, -122.3500),  # Woodside area
    (37.4600, -122.2500),  # Portola Valley
    (37.4000, -122.2200),  # Los Altos Hills
    (37.3500, -122.0900),  # Cupertino / 85 interchange area
    (37.3200, -122.0500),  # West San Jose
    (37.3050, -121.9200),  # 280–880–17 area
    (37.3382, -121.8863),  # Downtown San Jose
]

# I-80: San Francisco (Bay Bridge) → Sacramento (Downtown)
sf_to_sac_i80_anchors: List[LatLon] = [
    (37.7950, -122.3930),  # SF Embarcadero / Bay Bridge on-ramp
    (37.8200, -122.3700),  # Yerba Buena / TI vicinity
    (37.8100, -122.3000),  # West Oakland
    (37.8300, -122.2900),  # Emeryville
    (37.8700, -122.3000),  # Berkeley
    (37.9200, -122.3300),  # Richmond
    (38.0200, -122.2600),  # Rodeo / Crockett
    (38.1100, -122.2400),  # Vallejo
    (38.2000, -122.1200),  # Fairfield outskirts
    (38.2700, -122.0300),  # Fairfield
    (38.3600, -121.9900),  # Vacaville
    (38.4700, -121.7800),  # Dixon
    (38.5500, -121.7400),  # Davis
    (38.5800, -121.5300),  # West Sacramento
    (38.5816, -121.4944),  # Downtown Sacramento
]

# I-880: Oakland (Downtown) → San Jose (Downtown)
oakland_to_sj_i880_anchors: List[LatLon] = [
    (37.8044, -122.2712),  # Downtown Oakland
    (37.7900, -122.2600),  # Oakland south
    (37.7700, -122.2400),  # Oakland / Alameda area
    (37.7300, -122.2100),  # San Leandro
    (37.7000, -122.1900),  # San Leandro south
    (37.6700, -122.1500),  # Hayward north
    (37.6300, -122.1200),  # Hayward south / 92
    (37.6000, -122.0700),  # Union City
    (37.5500, -122.0400),  # Fremont north
    (37.5200, -122.0000),  # Fremont central
    (37.4700, -121.9600),  # Fremont south / Warm Springs
    (37.4400, -121.9200),  # Milpitas
    (37.4000, -121.9200),  # North San Jose
    (37.3500, -121.9100),  # Central San Jose
    (37.3382, -121.8863),  # Downtown San Jose
]


# =============================================================================
# DENSIFICATION HELPER
# =============================================================================

def densify_polyline(polyline: List[LatLon], points_per_segment: int) -> List[LatLon]:
    """
    Insert interpolated points between each pair of vertices in a polyline.

    Args:
        polyline: list of (lat, lon) points forming the route.
        points_per_segment: how many *subdivisions* per original segment.
            Example: 4 -> each segment gets 4 new points between endpoints.

    Returns:
        New polyline with original points plus interpolated points.
    """
    if len(polyline) < 2 or points_per_segment <= 0:
        return polyline[:]

    dense: List[LatLon] = []

    for i in range(len(polyline) - 1):
        lat1, lon1 = polyline[i]
        lat2, lon2 = polyline[i + 1]

        # Include start of segment (only once at i=0)
        if i == 0:
            dense.append((lat1, lon1))

        # Linear interpolation in lat/lon (OK for test data)
        for k in range(1, points_per_segment + 1):
            t = k / (points_per_segment + 1)  # avoids duplicating end point
            lat = lat1 + t * (lat2 - lat1)
            lon = lon1 + t * (lon2 - lon1)
            dense.append((lat, lon))

        # Add the exact end of the last segment
        if i == len(polyline) - 2:
            dense.append((lat2, lon2))

    return dense


# =============================================================================
# BUILD ROUTE DICTIONARIES
# =============================================================================

anchor_highway_routes: Dict[str, List[LatLon]] = {
    "sf_to_sj_us101_anchor": sf_to_sj_us101_anchors,
    "sf_to_sj_i280_anchor": sf_to_sj_i280_anchors,
    "sf_to_sac_i80_anchor": sf_to_sac_i80_anchors,
    "oakland_to_sj_i880_anchor": oakland_to_sj_i880_anchors,
}

# More base points (good default for algorithms)
BASE_POINTS_PER_SEGMENT = 4

base_highway_routes: Dict[str, List[LatLon]] = {
    name.replace("_anchor", ""): densify_polyline(route, points_per_segment=BASE_POINTS_PER_SEGMENT)
    for name, route in anchor_highway_routes.items()
}

# Very dense for fine-grained sampling
HD_POINTS_PER_SEGMENT = 10

hd_highway_routes: Dict[str, List[LatLon]] = {
    name + "_hd": densify_polyline(route, points_per_segment=HD_POINTS_PER_SEGMENT)
    for name, route in base_highway_routes.items()
}


# =============================================================================
# DELIVERY ROUTE PAIRS (City-to-City)
# =============================================================================

# Delivery routes following US-101 direction (SF → San Jose)
us101_delivery_routes: List[Tuple[LatLon, LatLon]] = [
    # SF → Peninsula
    ((37.7749, -122.4194), (37.6160, -122.3920)),  # SF City Hall → SFO
    ((37.7577, -122.3953), (37.5500, -122.3040)),  # Potrero Hill → San Mateo
    ((37.7300, -122.3920), (37.4852, -122.2364)),  # Bayview → Redwood City
    
    # Peninsula → South Bay
    ((37.6160, -122.3920), (37.4419, -122.1430)),  # SFO → Palo Alto
    ((37.5900, -122.3460), (37.4040, -122.0790)),  # Burlingame → Mountain View
    ((37.5500, -122.3040), (37.3688, -122.0363)),  # San Mateo → Sunnyvale
    ((37.5100, -122.2700), (37.3541, -121.9552)),  # Belmont → Santa Clara
    ((37.4852, -122.2364), (37.3382, -121.8863)),  # Redwood City → San Jose
    
    # Short hops within Peninsula
    ((37.5900, -122.3460), (37.5500, -122.3040)),  # Burlingame → San Mateo
    ((37.5500, -122.3040), (37.5100, -122.2700)),  # San Mateo → Belmont
    ((37.5100, -122.2700), (37.4852, -122.2364)),  # Belmont → Redwood City
    
    # Short hops within South Bay
    ((37.4419, -122.1430), (37.4040, -122.0790)),  # Palo Alto → Mountain View
    ((37.4040, -122.0790), (37.3688, -122.0363)),  # Mountain View → Sunnyvale
    ((37.3688, -122.0363), (37.3541, -121.9552)),  # Sunnyvale → Santa Clara
    ((37.3541, -121.9552), (37.3382, -121.8863)),  # Santa Clara → San Jose
    
    # Long hauls
    ((37.7749, -122.4194), (37.3382, -121.8863)),  # SF → San Jose (full route)
    ((37.6160, -122.3920), (37.3382, -121.8863)),  # SFO → San Jose
]

# Delivery routes following I-280 direction (SF → San Jose via peninsula)
i280_delivery_routes: List[Tuple[LatLon, LatLon]] = [
    # SF → Peninsula (west side)
    ((37.7749, -122.4194), (37.7083, -122.4500)),  # SF City Hall → Daly City
    ((37.7440, -122.4310), (37.6300, -122.4400)),  # Glen Park → San Bruno
    ((37.7083, -122.4500), (37.5900, -122.4200)),  # Daly City → Hillsborough
    
    # Peninsula → South Bay (scenic route)
    ((37.5900, -122.4200), (37.4600, -122.2500)),  # Hillsborough → Portola Valley
    ((37.5400, -122.3500), (37.4000, -122.2200)),  # Woodside → Los Altos Hills
    ((37.4600, -122.2500), (37.3500, -122.0900)),  # Portola Valley → Cupertino
    ((37.4000, -122.2200), (37.3200, -122.0500)),  # Los Altos Hills → West San Jose
    ((37.3500, -122.0900), (37.3382, -121.8863)),  # Cupertino → San Jose
    
    # Long hauls
    ((37.7749, -122.4194), (37.3382, -121.8863)),  # SF → San Jose (full I-280)
    ((37.5900, -122.4200), (37.3382, -121.8863)),  # Hillsborough → San Jose
]

# Delivery routes following I-80 direction (SF → Sacramento)
i80_delivery_routes: List[Tuple[LatLon, LatLon]] = [
    # SF → East Bay
    ((37.7950, -122.3930), (37.8100, -122.3000)),  # SF → West Oakland
    ((37.7950, -122.3930), (37.8300, -122.2900)),  # SF → Emeryville
    ((37.8100, -122.3000), (37.8700, -122.3000)),  # West Oakland → Berkeley
    ((37.8300, -122.2900), (37.9200, -122.3300)),  # Emeryville → Richmond
    
    # East Bay → North Bay
    ((37.8700, -122.3000), (38.0200, -122.2600)),  # Berkeley → Rodeo
    ((37.9200, -122.3300), (38.1100, -122.2400)),  # Richmond → Vallejo
    ((38.0200, -122.2600), (38.2000, -122.1200)),  # Rodeo → Fairfield outskirts
    
    # North Bay → Inland
    ((38.1100, -122.2400), (38.2700, -122.0300)),  # Vallejo → Fairfield
    ((38.2000, -122.1200), (38.3600, -121.9900)),  # Fairfield outskirts → Vacaville
    ((38.2700, -122.0300), (38.4700, -121.7800)),  # Fairfield → Dixon
    ((38.3600, -121.9900), (38.5500, -121.7400)),  # Vacaville → Davis
    
    # Inland → Sacramento
    ((38.4700, -121.7800), (38.5500, -121.7400)),  # Dixon → Davis
    ((38.5500, -121.7400), (38.5816, -121.4944)),  # Davis → Sacramento
    ((38.5800, -121.5300), (38.5816, -121.4944)),  # West Sacramento → Downtown
    
    # Long hauls
    ((37.7950, -122.3930), (38.5816, -121.4944)),  # SF → Sacramento (full route)
    ((37.8700, -122.3000), (38.5816, -121.4944)),  # Berkeley → Sacramento
    ((38.1100, -122.2400), (38.5816, -121.4944)),  # Vallejo → Sacramento
]

# Delivery routes following I-880 direction (Oakland → San Jose)
i880_delivery_routes: List[Tuple[LatLon, LatLon]] = [
    # Oakland → South
    ((37.8044, -122.2712), (37.7300, -122.2100)),  # Downtown Oakland → San Leandro
    ((37.7900, -122.2600), (37.7000, -122.1900)),  # Oakland south → San Leandro south
    ((37.7700, -122.2400), (37.6700, -122.1500)),  # Oakland/Alameda → Hayward north
    
    # San Leandro → Hayward
    ((37.7300, -122.2100), (37.6300, -122.1200)),  # San Leandro → Hayward south
    ((37.7000, -122.1900), (37.6000, -122.0700)),  # San Leandro south → Union City
    
    # Hayward → Fremont
    ((37.6700, -122.1500), (37.5500, -122.0400)),  # Hayward north → Fremont north
    ((37.6300, -122.1200), (37.5200, -122.0000)),  # Hayward south → Fremont central
    ((37.6000, -122.0700), (37.4700, -121.9600)),  # Union City → Fremont south
    
    # Fremont → South Bay
    ((37.5500, -122.0400), (37.4400, -121.9200)),  # Fremont north → Milpitas
    ((37.5200, -122.0000), (37.4000, -121.9200)),  # Fremont central → North San Jose
    ((37.4700, -121.9600), (37.3500, -121.9100)),  # Fremont south → Central San Jose
    ((37.4400, -121.9200), (37.3382, -121.8863)),  # Milpitas → Downtown San Jose
    
    # Long hauls
    ((37.8044, -122.2712), (37.3382, -121.8863)),  # Oakland → San Jose (full route)
    ((37.7300, -122.2100), (37.3382, -121.8863)),  # San Leandro → San Jose
    ((37.6300, -122.1200), (37.3382, -121.8863)),  # Hayward → San Jose
    ((37.5500, -122.0400), (37.3382, -121.8863)),  # Fremont → San Jose
]


# =============================================================================
# DENSIFIED ROUTES
# =============================================================================

# Build base routes from anchors
base_highway_routes: Dict[str, List[LatLon]] = {
    "sf_to_sj_us101": densify_polyline(sf_to_sj_us101_anchors, points_per_segment=4),
    "sf_to_sj_i280": densify_polyline(sf_to_sj_i280_anchors, points_per_segment=4),
    "sf_to_sac_i80": densify_polyline(sf_to_sac_i80_anchors, points_per_segment=4),
    "oakland_to_sj_i880": densify_polyline(oakland_to_sj_i880_anchors, points_per_segment=4),
}

# High-definition routes
hd_highway_routes: Dict[str, List[LatLon]] = {
    "sf_to_sj_us101_hd": densify_polyline(sf_to_sj_us101_anchors, points_per_segment=10),
    "sf_to_sj_i280_hd": densify_polyline(sf_to_sj_i280_anchors, points_per_segment=10),
    "sf_to_sac_i80_hd": densify_polyline(sf_to_sac_i80_anchors, points_per_segment=10),
    "oakland_to_sj_i880_hd": densify_polyline(oakland_to_sj_i880_anchors, points_per_segment=10),
}


# =============================================================================
# DELIVERY ROUTE PAIRS (Combined)
# =============================================================================

delivery_route_pairs: Dict[str, List[Tuple[LatLon, LatLon]]] = {
    "us101_deliveries": us101_delivery_routes,
    "i280_deliveries": i280_delivery_routes,
    "i80_deliveries": i80_delivery_routes,
    "i880_deliveries": i880_delivery_routes,
}


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def get_all_delivery_pairs() -> List[Tuple[LatLon, LatLon]]:
    """Get all delivery pairs from all routes combined."""
    all_pairs = []
    for pairs in delivery_route_pairs.values():
        all_pairs.extend(pairs)
    return all_pairs


def get_delivery_pairs_for_route(route_name: str) -> List[Tuple[LatLon, LatLon]]:
    """
    Get delivery pairs for a specific route.
    
    Args:
        route_name: One of "sf_to_sj_us101", "sf_to_sj_i280", "sf_to_sac_i80", "oakland_to_sj_i880"
        
    Returns:
        List of delivery route pairs
    """
    mapping = {
        "sf_to_sj_us101": us101_delivery_routes,
        "sf_to_sj_i280": i280_delivery_routes,
        "sf_to_sac_i80": i80_delivery_routes,
        "oakland_to_sj_i880": i880_delivery_routes,
    }
    
    if route_name not in mapping:
        raise ValueError(f"Unknown route: {route_name}. Choose from {list(mapping.keys())}")
    
    return mapping[route_name]


def print_route_summary():
    """Print summary of available routes and delivery pairs."""
    print("=" * 70)
    print("ROUTE DATA SUMMARY")
    print("=" * 70)
    
    print("\nBase Highway Routes:")
    for name, route in base_highway_routes.items():
        print(f"  - {name}: {len(route)} points")
    
    print("\nDelivery Route Pairs:")
    for name, pairs in delivery_route_pairs.items():
        print(f"  - {name}: {len(pairs)} delivery routes")
    
    total_deliveries = sum(len(pairs) for pairs in delivery_route_pairs.values())
    print(f"\nTotal delivery routes: {total_deliveries}")
    print("=" * 70)


# Print summary when module is imported
if __name__ == "__main__":
    print_route_summary()

