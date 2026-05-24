import sys
import json
import plotly.graph_objects as go
import pathlib

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Load data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data_json = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and texts
chart_data = chart_data_json.get('chart_data', [])
texts = chart_data_json.get('texts', {})
colors = chart_data_json.get('colors', [])

# Prepare data for Plotly
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]
bar_labels = [str(item['value']) for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=bar_labels,
    textposition='outside',
    marker_color=colors[0] if colors else None,
    cliponaxis=False,
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    )
))

# Update layout
fig.update_layout(
    font=dict(family="Arial", size=12, color='black'),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title=texts.get('x_axis_title'),
        tickmode='linear',
        showgrid=False,
        linecolor='black'
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        range=[0, 20000],
        tickvals=[0, 2500, 5000, 7500, 10000, 12500, 15000, 17500, 20000],
        gridcolor='#EAEAEA',
        zeroline=False,
        linecolor='black'
    ),
    margin=dict(l=80, r=40, t=50, b=100),
)

# Add annotations for source and note
if texts.get('note'):
    fig.add_annotation(
        text=texts['note'],
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0,
        y=-0.20,
        xanchor='left',
        yanchor='bottom'
    )

if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=1,
        y=-0.20,
        xanchor='right',
        yanchor='bottom'
    )

# Define output filename from the input JSON filename
base_filename = pathlib.Path(json_path).stem
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")