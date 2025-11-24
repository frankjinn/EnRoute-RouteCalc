"""
Example workflows for the Point Selection system.

Run these examples to see how to use the statistical oriented bounding box
for filtering delivery route pairs around highways.
"""

from typing import List, Tuple
from point_visualization import visualize_route_with_oriented_bbox
from route_data import (
    base_highway_routes,
    delivery_route_pairs,
    get_delivery_pairs_for_route,
    get_all_delivery_pairs
)


def example_1_basic_workflow(compute_oriented_bbox_with_min_pairs, filter_pairs_in_oriented_bbox):
    """
    Example 1: US-101 Delivery Routes with Oriented Bounding Box
    
    Uses pre-generated city-to-city delivery routes along US-101.
    """
    print("=" * 70)
    print("EXAMPLE 1: US-101 Delivery Routes")
    print("=" * 70)
    
    # Load route and delivery pairs
    route = base_highway_routes["sf_to_sj_us101"]
    delivery_pairs = get_delivery_pairs_for_route("sf_to_sj_us101")
    
    print(f"\n1. Route: US-101 SF to SJ ({len(route)} points)")
    print(f"2. Loaded {len(delivery_pairs)} city-to-city delivery routes")
    
    # Compute oriented box with min pairs guarantee
    min_pairs_required = 10
    print(f"3. Computing oriented box guaranteeing {min_pairs_required} delivery routes...")
    
    bbox_corners, angle = compute_oriented_bbox_with_min_pairs(
        route=route,
        pairs=delivery_pairs,
        min_pairs=min_pairs_required,
        method="percentile"
    )
    
    # Filter pairs
    filtered_pairs = filter_pairs_in_oriented_bbox(
        delivery_pairs,
        bbox_corners,
        require_both=True
    )
    
    print(f"4. Results:")
    print(f"   - Box angle: {angle:.1f}° from east")
    print(f"   - Delivery routes inside: {len(filtered_pairs)}/{len(delivery_pairs)}")
    print(f"   - Guarantee met: {len(filtered_pairs) >= min_pairs_required}")
    
    # Visualize
    visualize_route_with_oriented_bbox(
        route=route,
        all_pairs=delivery_pairs,
        filtered_pairs=filtered_pairs,
        bbox_corners=bbox_corners,
        angle=angle,
        output_file="example1_us101_deliveries.html"
    )
    
    print("\n" + "=" * 70)
    return route, delivery_pairs, filtered_pairs, bbox_corners, angle


def example_2_i280_deliveries(compute_oriented_bbox_with_min_pairs, filter_pairs_in_oriented_bbox):
    """
    Example 2: I-280 Delivery Routes (Scenic Peninsula Route)
    
    Uses pre-generated delivery routes along I-280.
    """
    print("=" * 70)
    print("EXAMPLE 2: I-280 Delivery Routes (Peninsula)")
    print("=" * 70)
    
    route = base_highway_routes["sf_to_sj_i280"]
    delivery_pairs = get_delivery_pairs_for_route("sf_to_sj_i280")
    
    print(f"\nRoute: I-280 SF to SJ ({len(route)} points)")
    print(f"Loaded: {len(delivery_pairs)} delivery routes")
    
    # Compute box for all delivery routes
    min_required = 2
    print(f"\nComputing oriented box guaranteeing {min_required} delivery routes...")
    
    bbox, angle = compute_oriented_bbox_with_min_pairs(
        route, delivery_pairs, min_pairs=min_required, method="percentile"
    )
    filtered = filter_pairs_in_oriented_bbox(delivery_pairs, bbox, require_both=True)
    
    print(f"\nResults:")
    print(f"  Box angle: {angle:.1f}° from east")
    print(f"  Delivery routes inside: {len(filtered)}/{len(delivery_pairs)}")
    
    # Visualize
    visualize_route_with_oriented_bbox(
        route, delivery_pairs, filtered, bbox, angle,
        "example2_i280_deliveries.html"
    )
    
    print("\n" + "=" * 70)


def example_3_all_routes(compute_oriented_bbox_with_min_pairs, filter_pairs_in_oriented_bbox):
    """
    Example 3: All Routes with Their Delivery Pairs
    
    Shows how the oriented box adapts to different route directions.
    Processes all highways: US-101, I-280, I-880 (North-South) and I-80 (East-West).
    """
    print("=" * 70)
    print("EXAMPLE 3: All Routes with Delivery Pairs")
    print("=" * 70)
    
    routes_to_test = [
        ("sf_to_sj_us101", "US-101 (North-South)", 10),
        ("sf_to_sj_i280", "I-280 (Peninsula)", 6),
        ("oakland_to_sj_i880", "I-880 (East Bay)", 10),
        ("sf_to_sac_i80", "I-80 (East-West to Sac)", 12),
    ]
    
    for route_key, route_name, min_pairs in routes_to_test:
        route = base_highway_routes[route_key]
        delivery_pairs = get_delivery_pairs_for_route(route_key)
        
        # Compute oriented box
        bbox_corners, angle = compute_oriented_bbox_with_min_pairs(
            route, delivery_pairs, min_pairs=min_pairs, method="percentile"
        )
        
        filtered = filter_pairs_in_oriented_bbox(delivery_pairs, bbox_corners, require_both=True)
        
        print(f"\n{route_name}:")
        print(f"  Route points: {len(route)}")
        print(f"  Delivery routes: {len(delivery_pairs)}")
        print(f"  Box angle: {angle:.1f}° from east")
        print(f"  Inside box: {len(filtered)} (min: {min_pairs})")
        
        # Visualize
        visualize_route_with_oriented_bbox(
            route, delivery_pairs, filtered, bbox_corners, angle,
            f"example3_{route_key}.html"
        )
    
    print("\n" + "=" * 70)


def example_4_combined_deliveries(compute_oriented_bbox_with_min_pairs, filter_pairs_in_oriented_bbox):
    """
    Example 4: All Bay Area Deliveries Combined
    
    Combines delivery routes from all highways into one dataset.
    """
    print("=" * 70)
    print("EXAMPLE 4: All Bay Area Deliveries Combined")
    print("=" * 70)
    
    # Get all delivery pairs from all routes
    all_deliveries = get_all_delivery_pairs()
    
    print(f"\nTotal delivery routes across Bay Area: {len(all_deliveries)}")
    
    # Show breakdown by highway
    for route_name in ["sf_to_sj_us101", "sf_to_sj_i280", "oakland_to_sj_i880", "sf_to_sac_i80"]:
        pairs = get_delivery_pairs_for_route(route_name)
        print(f"  - {route_name}: {len(pairs)} delivery routes")
    
    # For this example, let's use US-101 as the primary route
    # and see how many total Bay Area deliveries fall within its corridor
    route = base_highway_routes["sf_to_sj_us101"]
    
    min_required = 30
    print(f"\nFiltering all Bay Area deliveries along US-101 corridor...")
    print(f"Guaranteeing minimum: {min_required} delivery routes")
    
    bbox, angle = compute_oriented_bbox_with_min_pairs(
        route, all_deliveries, min_pairs=min_required, method="percentile"
    )
    
    filtered = filter_pairs_in_oriented_bbox(all_deliveries, bbox, require_both=True)
    
    print(f"\nResults:")
    print(f"  Box angle: {angle:.1f}° from east")
    print(f"  Delivery routes in US-101 corridor: {len(filtered)}/{len(all_deliveries)}")
    
    visualize_route_with_oriented_bbox(
        route, all_deliveries, filtered, bbox, angle,
        "example4_all_bay_area_deliveries.html"
    )
    
    print("\n" + "=" * 70)


def run_all_examples(compute_oriented_bbox_with_min_pairs, filter_pairs_in_oriented_bbox):
    """
    Run all examples in sequence.
    
    Args:
        compute_oriented_bbox_with_min_pairs: Function from points.ipynb
        filter_pairs_in_oriented_bbox: Function from points.ipynb
    """
    print("\n")
    print("█" * 70)
    print(" " * 20 + "RUNNING ALL EXAMPLES")
    print("█" * 70)
    print("\n")
    
    example_1_basic_workflow(
        compute_oriented_bbox_with_min_pairs,
        filter_pairs_in_oriented_bbox
    )
    
    example_2_i280_deliveries(
        compute_oriented_bbox_with_min_pairs,
        filter_pairs_in_oriented_bbox
    )
    
    example_3_all_routes(
        compute_oriented_bbox_with_min_pairs,
        filter_pairs_in_oriented_bbox
    )
    
    example_4_combined_deliveries(
        compute_oriented_bbox_with_min_pairs,
        filter_pairs_in_oriented_bbox
    )
    
    print("\n")
    print("█" * 70)
    print(" " * 25 + "ALL EXAMPLES COMPLETE")
    print("█" * 70)
    print("\n")

