import sys
import json
import plotly.graph_objects as go
import os

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Initialize the figure
fig = go.Figure()

# Add a bar trace for each data series from the JSON
for i, series in enumerate(chart_data['chart_data']):
    fig.add_trace(go.Bar(
        x=chart_data['x_categories'],
        y=series['y'],
        name=series['name'],
        marker_color=chart_data['colors'][i],
        text=[f"{val}%" for val in series['y']],
        textposition='outside',
        cliponaxis=False,
        textfont=dict(
            family="Arial",
            size=12,
            color='black'
        )
    ))

# Update layout
fig.update_layout(
    barmode='group',
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis=dict(
        title_text=chart_data['texts']['x_axis_title'],
        showline=True,
        linewidth=1,
        linecolor='black',
        tickfont=dict(size=12),
        showgrid=False
    ),
    yaxis=dict(
        title_text=chart_data['texts']['y_axis_title'],
        range=[0, 125],
        tickvals=[0, 20, 40, 60, 80, 100, 120],
        ticksuffix='%',
        showgrid=True,
        gridcolor='#e0e0e0',
        gridwidth=1,
        zeroline=False,
        showline=False
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.3,
        xanchor="center",
        x=0.5
    ),
    margin=dict(l=80, r=40, b=120, t=40),
    annotations=[
        dict(
            showarrow=False,
            text=chart_data['texts']['source'],
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

# Determine output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")