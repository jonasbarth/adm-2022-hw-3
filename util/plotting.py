"""A module for plotting Atlast Obscura data."""

import plotly.express as px

def plot_map(place_data, title, width=1000, height=600, zoom=0.7, lat_centre=40.77, lon_centre=-73.96):
    """Plots a map with the provided place data."""

    fig = px.scatter_mapbox(
        place_data,  # Our DataFrame
        lat = "lat",
        lon = "lon",
        center = {"lat": lat_centre, "lon": lon_centre},  # where map will be centered (New York)
        width = width,  # Width of map
        height = height,  # Height of map
        color="similarity", size="similarity",
        zoom=zoom,
        hover_data = ["name", "address", "num_people_visited", "num_people_want"],
        # what to display when hovering mouse over coordinate
    )
    fig.update_layout(
        title={
            'text': title,
            'y':0.95,
            'x':0.45,
            'xanchor': 'center',
            'yanchor': 'top'})

    fig.update_layout(mapbox_style="stamen-toner")
    fig.show()