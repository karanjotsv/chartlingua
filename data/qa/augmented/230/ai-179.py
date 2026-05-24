import sys
import json
import plotly.graph_objects as go
import pathlib

# Check for command-line argument for the JSON file path
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]
output_base_name = pathlib.Path(json_path).stem

# Load all data and texts from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']
legend_series_names = texts['legend_series']

# Reverse data to display in the correct top-to-bottom order in Plotly
chart_data.reverse()

categories = [d['category'] for d in chart_data]
values_series1 = [d['values'][0] for d in chart_data]
values_series2 = [d['values'][1] for d in chart_data]

# Initialize the figure
fig = go.Figure()

# Add the first data series as a bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values_series1,
    name=legend_series_names[0],
    orientation='h',
    marker_color=colors[0],
    text=values_series1,
    textposition='outside',
    textfont=dict(color='black', size=12),
    cliponaxis=False
))

# Add the second data series as a bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values_series2,
    name=legend_series_names[1],
    orientation='h',
    marker_color=colors[1],
    text=values_series2,
    textposition='outside',
    textfont=dict(color='black', size=12),
    cliponaxis=False
))

# Update layout for a professional and accurate appearance
fig.update_layout(
    barmode='group',
    font=dict(family="Arial", size=12, color="black"),
    plot_bgcolor='white',
    xaxis=dict(
        title_text=texts['x_axis_title'],
        showgrid=True,
        gridcolor='rgba(224, 224, 224, 0.7)',
        gridwidth=1,
        zeroline=False,
        range=[0, 475]  # Extend range to prevent data labels from being clipped
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        showgrid=False,
        zeroline=False
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.25,
        xanchor="center",
        x=0.5
    ),
    margin=dict(l=100, r=40, t=30, b=100),
    annotations=[
        dict(
            text=texts['source'],
            showarrow=False,
            xref="paper",
            yref="paper",
            x=1.0,
            y=-0.35,
            xanchor='right',
            yanchor='bottom',
            align='right',
            font=dict(size=12)
        )
    ]
)

# Generate the output image file
output_image_path = f"{output_base_name}.png"
fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")