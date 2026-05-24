import sys
import json
import plotly.graph_objects as go
import pathlib

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_file_path = pathlib.Path(sys.argv[1])

# Read data from the JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

# Extract data for the chart
labels = [d['label'] for d in chart_data['chart_data']]
values = [d['value'] for d in chart_data['chart_data']]
texts = chart_data['texts']
colors = chart_data['colors']

# Create the pie chart
fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#000000', width=1)),
    textinfo='value',
    textposition='outside',
    textfont=dict(family="Arial", size=14, weight='bold'),
    hoverinfo='label+percent+value',
    sort=False,  # Preserve the original order from the JSON
    direction='clockwise'
))

# Update layout
title_text = f"<b>{texts['title']}</b>"
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

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
        x=0.95,
        y=0.7,
        xanchor='left',
        yanchor='middle'
    ),
    margin=dict(t=80, b=170, l=40, r=40), # Increased bottom margin for long source
    annotations=[
        dict(
            text=texts['source'],
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0,
            y=-0.2, # Position annotation below the chart
            xanchor='left',
            yanchor='top',
            align='left',
            font=dict(family="Arial", size=10)
        )
    ]
)

# Define output filename and save the image
output_filename_base = json_file_path.stem
output_png_path = f"{output_filename_base}.png"

fig.write_image(output_png_path, scale=2)

print(f"Chart successfully generated and saved to {output_png_path}")