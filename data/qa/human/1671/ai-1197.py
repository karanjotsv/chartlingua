import sys
import json
import pathlib
import plotly.graph_objects as go

# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) < 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]
path = pathlib.Path(json_path)
output_filename = path.with_suffix(".png")

# Read data and configuration from the JSON file
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
chart_data = config.get("chart_data", [])
texts = config.get("texts", {})
colors = config.get("colors", [])
chart_annotations = config.get("annotations", [])

# Initialize the figure
fig = go.Figure()

# Add traces to the figure
for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series.get("x"),
        y=series.get("y"),
        name=series.get("name"),
        mode='lines+markers',
        line=dict(color=colors[i % len(colors)]),
        marker=dict(color=colors[i % len(colors)], size=6)
    ))

# Build title string
title_text = f"<span style='font-size: 24px;'><b>{texts.get('title', '')}</b></span>"
if texts.get('subtitle'):
    title_text += f"<br><span style='font-size: 16px;'>{texts.get('subtitle')}</span>"

# Prepare layout annotations
layout_annotations = []
for ann in chart_annotations:
    layout_annotations.append(
        go.layout.Annotation(
            text=ann.get("text"),
            x=ann.get("x"),
            y=ann.get("y"),
            xref="x",
            yref="y",
            showarrow=ann.get("showarrow", False),
            xanchor=ann.get("xanchor", "left"),
            yanchor=ann.get("yanchor", "auto"),
            xshift=ann.get("xshift", 0),
            yshift=ann.get("yshift", 0),
            align="left",
            font=dict(family="Arial", size=12)
        )
    )

# Add source and note annotations
source_text = texts.get("source")
if source_text:
    layout_annotations.append(
        go.layout.Annotation(
            text=source_text,
            x=0,
            y=-0.15,
            xref="paper",
            yref="paper",
            xanchor="left",
            yanchor="top",
            showarrow=False,
            align="left",
            font=dict(family="Arial", size=12, color="grey")
        )
    )

note_text = texts.get("note")
if note_text:
    layout_annotations.append(
        go.layout.Annotation(
            text=note_text,
            x=1,
            y=-0.15,
            xref="paper",
            yref="paper",
            xanchor="right",
            yanchor="top",
            showarrow=False,
            align="right",
            font=dict(family="Arial", size=12, color="grey")
        )
    )

# Update layout
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.01,
        xanchor='left',
        y=0.95,
        yanchor='top'
    ),
    xaxis=dict(
        tickvals=[1970, 1972, 1974, 1976, 1978, 1980],
        showgrid=False,
        showline=True,
        linecolor='black',
        linewidth=1,
        zeroline=False,
        title_text=texts.get('x_axis_title')
    ),
    yaxis=dict(
        tickvals=[0, 0.2, 0.4, 0.6, 0.8],
        ticktext=[f"{v}%" for v in [0, 0.2, 0.4, 0.6, 0.8]],
        range=[0, 1.0],
        gridcolor='lightgrey',
        griddash='dot',
        zeroline=True,
        zerolinecolor='lightgrey',
        zerolinewidth=1,
        showline=False,
        title_text=texts.get('y_axis_title')
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    showlegend=False,
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=50, r=50, t=100, b=100),
    annotations=layout_annotations
)

# Write the image to a file
fig.write_image(str(output_filename), scale=2)

print(f"Chart saved to {output_filename}")