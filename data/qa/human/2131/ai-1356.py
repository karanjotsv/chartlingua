import sys
import json
import os
import plotly.graph_objects as go

# --- 1. Load Data ---
# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Read and parse the JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

# Extract data and texts from the loaded JSON
chart_data = chart_config.get("chart_data", {})
texts = chart_config.get("texts", {})
colors = chart_config.get("colors", [])
categories = chart_data.get("categories", [])
series_data = chart_data.get("series", [])

# --- 2. Create Figure ---
fig = go.Figure()

# --- 3. Add Traces ---
# Iterate through each data series in the JSON and add it as a bar trace
for i, series in enumerate(series_data):
    fig.add_trace(go.Bar(
        x=categories,
        y=series.get("data", []),
        name=series.get("name", ""),
        marker_color=colors[i % len(colors)],
        text=[f"{val}%" for val in series.get("data", [])],
        textposition='outside',
        textfont=dict(
            family="Arial",
            size=12,
            color='black',
            weight='bold'
        ),
        cliponaxis=False
    ))

# --- 4. Configure Layout ---
# Combine title and subtitle if they exist
title_text = ""
if texts.get("title"):
    title_text += f"<b>{texts['title']}</b>"
if texts.get("subtitle"):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Configure layout properties
fig.update_layout(
    barmode='group',
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title_text=texts.get("x_axis_title"),
        showline=True,
        linecolor='black',
        linewidth=1,
        ticks='',
        tickfont=dict(size=12),
        showgrid=False
    ),
    yaxis=dict(
        title_text=texts.get("y_axis_title"),
        range=[0, 50],
        dtick=10,
        ticksuffix='%',
        showgrid=True,
        gridcolor='#e0e0e0',
        gridwidth=1,
        zeroline=False
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.25,
        xanchor="center",
        x=0.5,
        font=dict(size=12)
    ),
    margin=dict(l=80, r=40, b=120, t=50),
    bargap=0.2,
    bargroupgap=0.1
)

# --- 5. Add Annotations for Source/Note ---
annotations = []
if texts.get("source"):
    annotations.append(
        go.layout.Annotation(
            text=texts["source"],
            align='left',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.99,
            y=-0.35,
            xanchor='right',
            yanchor='bottom',
            font=dict(size=11)
        )
    )

fig.update_layout(annotations=annotations)

# --- 6. Output Image ---
# Derive output filename from the input JSON filename
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_image_path = f"{base_filename}.png"

# Save the figure to a PNG file
fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")