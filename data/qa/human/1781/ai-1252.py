import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_path = sys.argv[1]

# Read data from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_path}'")
    sys.exit(1)

# Extract data and texts from the JSON structure
chart_data = chart_config.get("chart_data", [])
texts = chart_config.get("texts", {})
colors = chart_config.get("colors", [])

# Prepare data for Plotly
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors,
    text=values,
    textposition='outside',
    textfont=dict(
        family="Arial",
        size=12,
        color=colors
    ),
    cliponaxis=False,
    hoverinfo='none'
))

# Update layout
title_text = f"<b>{texts.get('title', '')}</b><br><span style='font-size:14px;color:#555555'>{texts.get('subtitle', '')}</span>"

fig.update_layout(
    title=dict(
        text=title_text,
        y=0.98,
        x=0.01,
        xanchor='left',
        yanchor='top'
    ),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='#e8f4fa',
    paper_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        showticklabels=False,  # We use annotations for colored labels
        showgrid=False,
        zeroline=False,
        showline=False
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='white',
        zeroline=False,
        range=[0, 18],
        tickvals=[0, 2, 4, 6, 8, 10, 12, 14, 16]
    ),
    margin=dict(l=50, r=40, t=100, b=80),
    annotations=[
        dict(
            text=texts.get('source', ''),
            align='right',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.99,
            y=1.05
        )
    ]
)

# Add custom colored x-axis labels using annotations
for i, category in enumerate(categories):
    fig.add_annotation(
        x=category,
        y=0,
        text=category,
        showarrow=False,
        font=dict(color=colors[i]),
        textangle=-45,
        yshift=-35,
        xanchor='center'
    )

# Add separator line below title
fig.add_shape(type="line",
    xref="paper", yref="paper",
    x0=0, y0=0.90, x1=1, y1=0.90,
    line=dict(color="#cccccc", width=1)
)

# Determine output filename from JSON path
p = pathlib.Path(json_path)
output_filename = p.with_suffix(".png")

# Write the image file
fig.write_image(str(output_filename), scale=2)

print(f"Chart saved to {output_filename}")