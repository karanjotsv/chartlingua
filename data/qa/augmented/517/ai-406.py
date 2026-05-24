import sys
import json
import plotly.graph_objects as go
import os

# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Ensure the input file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

# Load data from the specified JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_json = json.load(f)

# Initialize the figure
fig = go.Figure()

# Add a bar trace for each data series from the JSON
for i, series in enumerate(chart_json['chart_data']):
    fig.add_trace(go.Bar(
        x=series['x'],
        y=series['y'],
        name=series['name'],
        marker_color=chart_json['colors'][i],
        text=series['y'],
        textposition='outside',
        textfont=dict(
            family="Arial",
            size=12,
            color='black'
        ),
        cliponaxis=False # Prevent text from being clipped by the plot area
    ))

# Update the layout of the chart
fig.update_layout(
    barmode='group',
    plot_bgcolor='white',
    font=dict(
        family="Arial",
        size=12
    ),
    xaxis=dict(
        title_text=chart_json['texts']['x_axis_title'],
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=chart_json['texts']['y_axis_title'],
        range=[0, 210],
        tickvals=[0, 50, 100, 150, 200],
        showgrid=True,
        gridcolor='#EAEAEA',
        griddash='dash',
        zeroline=False,
        title_standoff=10
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.3,
        xanchor="center",
        x=0.5,
        font=dict(size=12)
    ),
    margin=dict(l=90, r=40, t=50, b=120),
    title=dict(
        text=chart_json['texts']['title'],
        x=0.05,
        xanchor='left'
    ),
    annotations=[
        dict(
            text=chart_json['texts']['source'],
            showarrow=False,
            xref="paper",
            yref="paper",
            x=1,
            y=-0.35,
            xanchor='right',
            yanchor='bottom',
            align='right',
            font=dict(
                size=12,
                color="#888888"
            )
        )
    ]
)

# Determine the output filename from the input JSON path
base_filename = os.path.splitext(json_path)[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")