"""
Point Selection Visualization Functions

This module contains all Folium-based visualization functions for
displaying routes, point pairs, and oriented bounding boxes.
"""

import folium
import numpy as np
from typing import List, Tuple, Dict


# Type alias
LatLon = Tuple[float, float]


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance between two points on Earth.
    
    Args:
        lat1, lon1: First point coordinates
        lat2, lon2: Second point coordinates
        
    Returns:
        Distance in kilometers
    """
    R = 6371.0  # Earth radius in km
    
    lat1_rad, lon1_rad = np.radians(lat1), np.radians(lon1)
    lat2_rad, lon2_rad = np.radians(lat2), np.radians(lon2)
    
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    a = np.sin(dlat/2)**2 + np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(dlon/2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    
    return R * c


def visualize_route_with_oriented_bbox(
    route: List[LatLon],
    all_pairs: List[Tuple[LatLon, LatLon]],
    filtered_pairs: List[Tuple[LatLon, LatLon]],
    bbox_corners: List[LatLon],
    angle: float,
    output_file: str = "route_oriented_bbox.html"
):
    """
    Visualize route with oriented bounding box and point pairs.
    
    Shows:
    - The route
    - Oriented bounding box aligned with route direction
    - Point pairs (green = kept, red = filtered out)
    
    Args:
        route: Route points
        all_pairs: All generated pairs
        filtered_pairs: Pairs inside the oriented box
        bbox_corners: Oriented bounding box corners
        angle: Rotation angle of the box
        output_file: Output HTML filename
    """
    
    # Create map
    center_lat = np.mean([p[0] for p in route])
    center_lon = np.mean([p[1] for p in route])
    m = folium.Map(location=[center_lat, center_lon], zoom_start=10)
    
    # Draw oriented bounding box
    oriented_bbox_coords = [
        [bbox_corners[i][0], bbox_corners[i][1]]
        for i in range(4)
    ]
    oriented_bbox_coords.append(oriented_bbox_coords[0])  # Close the polygon
    folium.Polygon(
        locations=oriented_bbox_coords,
        color='darkblue',
        fill=True,
        fillColor='darkblue',
        fillOpacity=0.05,
        weight=3,
        popup=f'Oriented Bounding Box (angle: {angle:.1f}°)',
        tooltip=f'Oriented Box ({angle:.1f}° from east)'
    ).add_to(m)
    
    # Draw route
    folium.PolyLine(
        locations=[(lat, lon) for lat, lon in route],
        color='blue',
        weight=4,
        opacity=0.8,
        popup='Route'
    ).add_to(m)
    
    # Convert filtered_pairs to set for quick lookup
    filtered_set = set(filtered_pairs)
    
    # Draw all pairs
    for pair in all_pairs:
        origin, dest = pair
        is_kept = pair in filtered_set
        
        # Choose color: green for kept, red for filtered
        color = 'green' if is_kept else 'red'
        opacity = 0.7 if is_kept else 0.3
        weight = 2 if is_kept else 1
        
        # Draw line
        folium.PolyLine(
            locations=[[origin[0], origin[1]], [dest[0], dest[1]]],
            color=color,
            weight=weight,
            opacity=opacity,
            popup=f'{"✓ KEPT" if is_kept else "✗ FILTERED"}'
        ).add_to(m)
        
        # Draw origin marker
        folium.CircleMarker(
            location=[origin[0], origin[1]],
            radius=4 if is_kept else 3,
            color=color,
            fill=True,
            fillOpacity=opacity,
            weight=1
        ).add_to(m)
        
        # Draw destination marker
        folium.CircleMarker(
            location=[dest[0], dest[1]],
            radius=5 if is_kept else 3,
            color=color,
            fill=True,
            fillOpacity=opacity,
            weight=2 if is_kept else 1
        ).add_to(m)
    
    # Add legend
    legend_html = f'''
    <div style="position: fixed; 
                bottom: 50px; right: 50px; 
                border:2px solid grey; z-index:9999; 
                background-color:white;
                padding: 10px;
                font-size: 14px;">
    <p style="margin: 5px;"><b>Oriented Bounding Box</b></p>
    <p style="margin: 5px;"><span style="color: darkblue;">▭</span> Oriented Box ({angle:.1f}° from east)</p>
    <p style="margin: 5px;"><span style="color: blue;">━━</span> Route</p>
    <hr style="margin: 10px 0;">
    <p style="margin: 5px; font-size: 12px;"><b>Pairs:</b></p>
    <p style="margin: 5px;"><span style="color: green;">●</span> Kept: {len(filtered_pairs)} ({100*len(filtered_pairs)/len(all_pairs):.1f}%)</p>
    <p style="margin: 5px;"><span style="color: red;">●</span> Filtered: {len(all_pairs) - len(filtered_pairs)} ({100*(len(all_pairs)-len(filtered_pairs))/len(all_pairs):.1f}%)</p>
    </div>
    '''
    
    m.get_root().html.add_child(folium.Element(legend_html))
    
    # Save map
    m.save(output_file)
    print(f"\nVisualization saved to {output_file}")
    print(f"  - Route with {len(route)} points")
    print(f"  - Oriented box angle: {angle:.1f}° from east")
    print(f"  - Total pairs: {len(all_pairs)}")
    print(f"  - Pairs kept: {len(filtered_pairs)} ({100*len(filtered_pairs)/len(all_pairs):.1f}%)")
    print(f"  - Pairs filtered: {len(all_pairs) - len(filtered_pairs)} ({100*(len(all_pairs)-len(filtered_pairs))/len(all_pairs):.1f}%)")


def make_folium_map(polylines: Dict[str, List[LatLon]], out_html: str = "routes_map.html"):
    """
    Create an interactive Folium map with the given polylines.

    Args:
        polylines: dict[str, list[(lat, lon)]]
        out_html: output HTML filename for the map
    """
    # 1) Compute a crude center: average all lats and lons
    all_lats = []
    all_lons = []
    for coords in polylines.values():
        for lat, lon in coords:
            all_lats.append(lat)
            all_lons.append(lon)

    if not all_lats:
        raise ValueError("No coordinates found in polylines")

    center_lat = sum(all_lats) / len(all_lats)
    center_lon = sum(all_lons) / len(all_lons)

    # 2) Initialize the map
    m = folium.Map(location=[center_lat, center_lon], zoom_start=11)

    # 3) Add each polyline
    for name, coords in polylines.items():
        folium.PolyLine(
            locations=[(lat, lon) for lat, lon in coords],
            weight=3,
            opacity=0.8,
            tooltip=name,
        ).add_to(m)

    # 4) Optionally, add markers at start/end of each route
    for name, coords in polylines.items():
        if not coords:
            continue
        start_lat, start_lon = coords[0]
        end_lat, end_lon = coords[-1]
        folium.Marker(
            location=[start_lat, start_lon],
            popup=f"{name} start",
            icon=folium.Icon(color="green", icon="play")
        ).add_to(m)
        folium.Marker(
            location=[end_lat, end_lon],
            popup=f"{name} end",
            icon=folium.Icon(color="red", icon="stop")
        ).add_to(m)

    # 5) Save to HTML
    m.save(out_html)
    print(f"Map saved to {out_html}. Open it in your browser.")

