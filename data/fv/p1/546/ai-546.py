import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data for plotting
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']
series_names = texts['legend_series_names']

# Prepare data for Plotly
categories = [item['category'] for item in chart_data]
values_by_series = []
if chart_data:
    num_series = len(chart_data[0]['values'])
    for i in range(num_series):
        series_values = [item['values'][i] for item in chart_data]
        values_by_series.append(series_values)

# Create the figure
fig = go.Figure()

# Add a bar trace for each data series
for i, series_name in enumerate(series_names):
    fig.add_trace(go.Bar(
        name=series_name,
        x=values_by_series[i],
        y=categories,
        orientation='h',
        marker_color=colors[i]
    ))

# Update layout to match the original chart
fig.update_layout(
    barmode='group',
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="center",
        x=0.5
    ),
    xaxis=dict(
        showgrid=True,
        gridcolor='lightgrey',
        zeroline=True,
        zerolinecolor='black',
        zerolinewidth=1,
        range=[0, 3.5],
        tickmode='linear',
        tick0=0,
        dtick=0.5
    ),
    yaxis=dict(
        showgrid=False,
        autorange='reversed'  # To display categories from top to bottom
    ),
    margin=dict(l=100, r=40, t=60, b=40),
    annotations=[
        dict(
            text=texts['source'],
            align='left',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.58,  # Positioned based on original chart's layout
            y=0.45,
            xanchor='left',
            yanchor='middle'
        )
    ]
)

# Determine output filename and save the image
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")