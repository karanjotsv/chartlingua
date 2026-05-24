import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python recreate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data for plotting
chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

# Initialize Figure
fig = go.Figure()

# Add traces for each data series
for i, series in enumerate(chart_data):
    # Format text labels to show integers without decimals
    text_labels = []
    for val in series.get('y', []):
        if val == int(val):
            text_labels.append(f"{int(val)}%")
        else:
            text_labels.append(f"{val:.2f}%")

    fig.add_trace(go.Bar(
        name=series.get('name', ''),
        x=series.get('x', []),
        y=series.get('y', []),
        marker_color=colors[i % len(colors)] if colors else None,
        text=text_labels,
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(family='Arial', size=12, color='white')
    ))

# Combine title and subtitle
title_text = ""
if texts.get("title"):
    title_text += f"<b>{texts['title']}</b>"
if texts.get("subtitle"):
    title_text += f"<br><sub>{texts['subtitle']}</sub>" if title_text else f"<sub>{texts['subtitle']}</sub>"

# Update layout
fig.update_layout(
    barmode='stack',
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        tickmode='array',
        tickvals=chart_data[0].get('x', []) if chart_data else [],
        showgrid=True,
        gridcolor='#f0f0f0',
        zeroline=False
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 100.1],
        tickmode='linear',
        tick0=0,
        dtick=25,
        ticksuffix='%',
        gridcolor='#d3d3d3',
        zeroline=False
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.25,
        xanchor="center",
        x=0.5
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12, color="black"),
    margin=dict(l=80, r=40, t=50, b=120)
)

# Add source annotation
source_text = ""
if texts.get("source"):
    source_text += texts["source"]
if texts.get("note"):
    source_text += f"<br>{texts['note']}" if source_text else texts['note']

if source_text:
    fig.add_annotation(
        showarrow=False,
        text=source_text,
        xref="paper",
        yref="paper",
        x=1,
        y=-0.3,
        xanchor='right',
        yanchor='bottom',
        align='right',
        font=dict(size=10, color='grey')
    )

# Determine output filename and save the image
base_name = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_name}.png"

fig.write_image(output_filename, scale=2, width=900, height=600)

print(f"Chart saved to {output_filename}")