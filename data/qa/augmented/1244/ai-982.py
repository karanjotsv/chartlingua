import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

# Read data from the JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data for plotting
chart_data = chart_info.get("chart_data", {})
categories = chart_data.get("categories", [])
series_data = chart_data.get("series", [])
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", [])

# Initialize the figure
fig = go.Figure()

# Add a trace for each data series
for i, series in enumerate(series_data):
    fig.add_trace(go.Bar(
        x=categories,
        y=series.get("data", []),
        name=series.get("name", ""),
        marker_color=colors[i % len(colors)],
        text=series.get("data", []),
        textposition='outside',
        textfont=dict(family="Arial", size=12),
        cliponaxis=False
    ))

# Update layout for a professional look
fig.update_layout(
    barmode='group',
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    xaxis=dict(
        title_text=texts.get("xaxis_title"),
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black',
        tickfont=dict(family="Arial", size=12)
    ),
    yaxis=dict(
        title_text=texts.get("yaxis_title"),
        range=[0, 260],
        showgrid=True,
        gridcolor='lightgray',
        griddash='dot',
        showline=True,
        linewidth=1,
        linecolor='black',
        tickfont=dict(family="Arial", size=12)
    ),
    legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.2,
        xanchor="center",
        x=0.5
    ),
    margin=dict(l=80, r=40, b=120, t=40),
    annotations=[
        dict(
            text=texts.get("source"),
            showarrow=False,
            xref="paper",
            yref="paper",
            x=1,
            y=-0.3,
            xanchor='right',
            yanchor='bottom',
            font=dict(family="Arial", size=12)
        )
    ]
)

# Derive output filename from the input JSON path
base_name = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_name}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved to {output_filename}")