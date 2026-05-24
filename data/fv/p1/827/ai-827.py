import sys
import json
import plotly.graph_objects as go
import os

# Check for correct command-line arguments
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from command-line arguments
json_file_path = sys.argv[1]

# Check if the file exists
if not os.path.exists(json_file_path):
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)
    
# Derive the output filename from the input JSON filename
base_name = os.path.splitext(os.path.basename(json_file_path))[0]
output_image_path = f"{base_name}.png"

# Read and parse the JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON file at {json_file_path}")
    sys.exit(1)


# Extract data for Plotly
labels = [item['category'] for item in chart_data['chart_data']]
values = [item['value'] for item in chart_data['chart_data']]
colors = chart_data['colors']
texts = chart_data['texts']

# Create the pie chart
fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(
        colors=colors,
        line=dict(color='#ffffff', width=1)
    ),
    textinfo='percent',
    texttemplate='%{value:.1f}%',
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    ),
    hoverinfo='label+percent',
    sort=False,
    direction='clockwise'
))

# Update layout
title_text = f"<b>{texts['title']}</b>" if texts.get('title') else ""

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        xanchor='center'
    ),
    font=dict(
        family="Arial"
    ),
    showlegend=True,
    legend=dict(
        orientation="v",
        yanchor="top",
        y=1,
        xanchor="left",
        x=1.02
    ),
    margin=dict(l=50, r=250, t=80, b=50),
    paper_bgcolor='white',
    plot_bgcolor='white'
)

fig.update_traces(
    textposition='inside'
)

# Save the figure as a PNG image
try:
    fig.write_image(output_image_path, scale=2)
    print(f"Chart saved to {output_image_path}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)