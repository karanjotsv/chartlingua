import sys
import json
import plotly.graph_objects as go

# Check if a file path is provided
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = sys.argv[1]

# Derive the base filename for the output image
filename_base = json_file_path.rsplit('.', 1)[0]

# Load data from the specified JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_file_path}'")
    sys.exit(1)

# Extract data and settings from the JSON structure
chart_data = chart_info.get('chart_data', [])
series_names = chart_info.get('series_names', [])
colors = chart_info.get('colors', [])
texts = chart_info.get('texts', {})

# Prepare data for Plotly
categories = [item['category'] for item in chart_data]
# Transpose values from per-category to per-series
values_by_series = list(zip(*[item['values'] for item in chart_data]))

# Create the figure
fig = go.Figure()

# Add a bar trace for each series, preserving order
for i, series_name in enumerate(series_names):
    fig.add_trace(go.Bar(
        name=series_name,
        x=categories,
        y=values_by_series[i],
        marker_color=colors[i]
    ))

# Build title and source strings safely, handling null values
title_text = texts.get('title', '') or ''
if texts.get('subtitle'):
    title_text += f"<br><sup>{texts['subtitle']}</sup>"

source_text = texts.get('source', '') or ''

# Update layout
fig.update_layout(
    barmode='group',
    title_text=title_text,
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12, color='black'),
    xaxis=dict(
        tickangle=-45,
        automargin=True,
        showgrid=False,
        zeroline=True,
        zerolinecolor='lightgrey',
        zerolinewidth=1
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 40],
        dtick=5,
        gridcolor='lightgrey',
        zeroline=True,
        zerolinecolor='lightgrey',
        zerolinewidth=1
    ),
    legend=dict(
        x=1.02,
        y=0.7,
        xanchor='left',
        yanchor='middle',
        bgcolor='rgba(0,0,0,0)'
    ),
    margin=dict(l=50, r=80, t=50, b=180), # Increased bottom margin for rotated labels
    annotations=[
        dict(
            text=source_text,
            showarrow=False,
            xref='paper', yref='paper',
            x=0, y=-0.35,  # Adjusted y-position for source text
            xanchor='left', yanchor='bottom',
            align='left'
        )
    ] if source_text else []
)

# Generate and save the image
output_filename = f"{filename_base}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")