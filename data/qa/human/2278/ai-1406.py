import sys
import json
import plotly.graph_objects as go
import pathlib

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_json = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

# Create a figure
fig = go.Figure()

# Add a bar trace for each data series from the JSON
for i, series in enumerate(chart_json['chart_data']):
    fig.add_trace(go.Bar(
        x=series['x'],
        y=series['y'],
        name=series['name'],
        marker_color=chart_json['colors'][i],
        text=series['y'],
        texttemplate='%{text}%',
        textposition='outside',
        textfont=dict(family='Arial', size=12, color='black'),
        cliponaxis=False  # Prevent text labels from being clipped
    ))

# Update layout for a professional look, based on the JSON texts
fig.update_layout(
    barmode='group',
    plot_bgcolor='white',
    font=dict(family="Arial"),
    xaxis=dict(
        title_text=chart_json['texts']['x_axis_title'],
        showgrid=False,
        showline=True,
        linecolor='black',
        linewidth=1,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=chart_json['texts']['y_axis_title'],
        showgrid=True,
        gridcolor='#e0e0e0',
        tickvals=[0, 20, 40, 60, 80],
        ticktext=['0%', '20%', '40%', '60%', '80%'],
        range=[0, 90],  # Give extra space for labels above bars
        tickfont=dict(size=12)
    ),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=-0.25,
        xanchor='center',
        x=0.5
    ),
    margin=dict(l=80, r=40, t=40, b=150),
    bargap=0.3, # Gap between groups of bars
    bargroupgap=0.1, # Gap between bars within a group
)

# Add source annotation if it exists
source_text = chart_json['texts'].get('source')
if source_text:
    fig.add_annotation(
        text=source_text,
        xref="paper", yref="paper",
        x=1, y=-0.32,
        xanchor='right', yanchor='bottom',
        showarrow=False,
        font=dict(size=12)
    )

# Determine output filename and save the image
base_filename = pathlib.Path(json_path).stem
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")