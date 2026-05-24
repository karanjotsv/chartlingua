import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data for the chart
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the pie chart
fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(
        colors=colors,
        line=dict(color='#000000', width=1)
    ),
    sort=False,
    direction='clockwise',
    hoverinfo='label+percent',
    textinfo='none'
))

# Combine title and source annotations
annotations = []
title_text = f"{texts.get('title', '') or ''}"
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

source_text = texts.get('source', '')
if source_text:
    annotations.append(
        dict(
            showarrow=False,
            text=source_text,
            xref="paper",
            yref="paper",
            x=0,
            y=0,
            xanchor='left',
            yanchor='top',
            align='left',
            font=dict(size=10)
        )
    )

# Update layout
fig.update_layout(
    title_text=title_text if title_text.strip() and title_text != "<br><sub></sub>" else None,
    title_x=0.5,
    font=dict(family="Arial"),
    showlegend=True,
    plot_bgcolor='#D3D3D3',
    paper_bgcolor='#D3D3D3',
    margin=dict(l=50, r=400, t=60, b=180),
    legend=dict(
        x=1.02,
        y=0.98,
        xanchor='left',
        yanchor='top',
        bgcolor='white',
        bordercolor='black',
        borderwidth=1
    ),
    annotations=annotations
)

# Generate output filename from JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the chart as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")