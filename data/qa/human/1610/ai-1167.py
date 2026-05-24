import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

# Extract data for plotting
chart_data = chart_info.get("chart_data", {})
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", [])
x_values = chart_data.get("x_values", [])

# Initialize figure
fig = go.Figure()

# Add traces for each data series
annotations = []
for i, series in enumerate(chart_data.get("series", [])):
    series_color = colors[i % len(colors)]
    fig.add_trace(go.Scatter(
        x=x_values,
        y=series.get("y_values", []),
        mode='lines+markers',
        name=series.get("name", ""),
        line=dict(color=series_color),
        marker=dict(color=series_color, size=6)
    ))

    # Add annotation for the series name at the end of the line
    annotations.append(dict(
        x=x_values[-1],
        y=series.get("y_values", [])[-1],
        text=series.get("name", ""),
        showarrow=False,
        xanchor='left',
        yanchor='middle',
        xshift=10,
        font=dict(family="Arial", size=14, color=series_color)
    ))

# Combine title and subtitle using HTML for styling
title_text = f"<span style='font-size: 24px;'>{texts.get('title', '')}</span><br><span style='font-size: 16px; color: #555555;'>{texts.get('subtitle', '')}</span>"

# Add source and note annotations
annotations.append(dict(
    xref="paper", yref="paper",
    x=0.0, y=-0.12,
    xanchor='left', yanchor='top',
    text=texts.get('source', ''),
    showarrow=False,
    font=dict(family="Arial", size=12, color="#666666")
))

annotations.append(dict(
    xref="paper", yref="paper",
    x=1.0, y=-0.12,
    xanchor='right', yanchor='top',
    text=texts.get('note', ''),
    showarrow=False,
    font=dict(family="Arial", size=12, color="#666666")
))

# Update layout
fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95,
        x=0.01,
        xanchor='left',
        yanchor='top'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        zeroline=False,
        showline=True,
        linecolor='lightgrey',
        tickmode='array',
        tickvals=[2000, 2002, 2004, 2006, 2008, 2010, 2012, 2014],
        tickfont=dict(size=14, color="#666666")
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=False,
        zeroline=False,
        showline=False,
        tickmode='array',
        tickvals=[0],
        range=[-0.1, 0.5], # Give space so line is not on the edge
        tickfont=dict(size=14, color="#666666")
    ),
    font=dict(
        family="Arial"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=50, r=150, t=120, b=80),
    annotations=annotations
)

# Determine output filename from JSON path
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")