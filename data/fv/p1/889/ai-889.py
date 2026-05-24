import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

# Get file path from command-line argument
json_path = pathlib.Path(sys.argv[1])

# Read data from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error reading or parsing JSON file: {e}")
    sys.exit(1)

# Extract data and texts
data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']
categories = [item['category'] for item in data]

# Create the figure
fig = go.Figure()

# Add traces for each series
# Assuming a single series for this specific bar chart
if 'series_names' in texts and texts['series_names']:
    series_name = texts['series_names'][0]
    values = [item['values'][0] for item in data]
    color = colors[0] if colors else '#1f77b4'
    
    fig.add_trace(go.Bar(
        x=categories,
        y=values,
        name=series_name,
        marker_color=color
    ))

# Build combined title string if applicable
title_text = ""
if texts.get("title"):
    title_text += texts["title"]
if texts.get("subtitle"):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Update layout
fig.update_layout(
    font_family="Arial",
    title=dict(
        text=title_text if title_text else None,
        x=0.5,
        xanchor='center'
    ),
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    xaxis=dict(
        tickangle=-45,
        gridcolor='LightGray'
    ),
    yaxis=dict(
        range=[0, 2000000000],
        gridcolor='LightGray'
    ),
    plot_bgcolor='#FCFCF5',
    paper_bgcolor='#FFFFFF',
    showlegend=True,
    legend=dict(
        x=0.99,
        y=0.99,
        xanchor='right',
        yanchor='top'
    ),
    margin=dict(l=100, r=40, t=40, b=150)
)

# Add source/note annotation if it exists
if texts.get("source"):
    fig.add_annotation(
        text=texts['source'],
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0,
        y=-0.3, # Adjust based on bottom margin
        xanchor='left',
        yanchor='bottom'
    )


# Define output filename and save the image
output_filename = json_path.stem + ".png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")