import sys
import json
import plotly.graph_objects as go
import os

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read and parse the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_path}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: The file '{json_path}' contains invalid JSON.")
    sys.exit(1)

# Extract data and texts from the JSON structure
chart_data = config.get('chart_data', [])
categories = config.get('categories', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

# Initialize the Plotly figure
fig = go.Figure()

# Iterate through the data series in the JSON to create a bar trace for each
for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        x=categories,
        y=series.get('y', []),
        name=series.get('name', ''),
        marker_color=colors[i % len(colors)],
        texttemplate='%{y:.0%}',
        textposition='outside',
        textfont=dict(family="Arial", size=12, color='black'),
        cliponaxis=False  # Allows text to be drawn outside the plotting area
    ))

# Combine title and subtitle, handling null values
title_parts = []
if texts.get("title"):
    title_parts.append(texts["title"])
if texts.get("subtitle"):
    title_parts.append(f"<span style='font-size: 14px;'>{texts['subtitle']}</span>")
full_title = "<br>".join(title_parts)

# Configure the figure layout for a clean, professional appearance
fig.update_layout(
    barmode='group',
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=14, color='black'),
    title=dict(
        text=full_title,
        x=0.01,
        xanchor='left'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        tickfont=dict(family="Arial", size=12),
        showline=True,
        linecolor='black',
        linewidth=1
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 0.8],
        tickformat='.0%',
        gridcolor='#e0e0e0',
        zeroline=False,
        tickfont=dict(family="Arial", size=12)
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.3,
        xanchor="center",
        x=0.5,
        font=dict(family="Arial", size=12)
    ),
    margin=dict(l=80, r=40, t=80, b=150),
    annotations=[
        dict(
            text=texts.get('source', ''),
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0.99,
            y=-0.35,
            xanchor='right',
            yanchor='bottom',
            align='right',
            font=dict(family="Arial", size=12)
        )
    ]
)

# Determine the output filename from the input JSON filename
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure to a high-resolution PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved to '{output_filename}'")