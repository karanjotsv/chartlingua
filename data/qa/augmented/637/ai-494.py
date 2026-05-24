import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) < 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_filepath = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_filepath, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_filepath}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_filepath}'")
    sys.exit(1)

# Extract data and settings from the JSON object
chart_data = chart_info.get("chart_data", [])
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", [])

# Initialize the figure
fig = go.Figure()

# Add traces from chart_data
for i, series in enumerate(chart_data):
    color = colors[i % len(colors)]
    fig.add_trace(go.Scatter(
        x=series["x"],
        y=series["y"],
        mode='lines+markers+text',
        line=dict(color=color, width=2.5),
        marker=dict(color=color, size=8),
        text=[f'{val:.2f}' for val in series["y"]],
        textposition='top center',
        textfont=dict(
            family="Arial",
            size=12,
            color='black'
        ),
        hoverinfo='none'
    ))

# Update layout
fig.update_layout(
    font=dict(family="Arial"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title_text=texts.get("x_axis_title"),
        showgrid=False,
        showline=True,
        linecolor='white',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts.get("y_axis_title"),
        title_font=dict(size=14),
        showgrid=True,
        gridcolor='#e0e0e0',
        gridwidth=1,
        zeroline=False,
        showline=False,
        range=[5.7, 7.1],
        tickvals=[5.8, 6.0, 6.2, 6.4, 6.6, 6.8, 7.0],
        tickfont=dict(size=12)
    ),
    margin=dict(l=80, r=40, t=50, b=100)
)

# Add source annotation
fig.add_annotation(
    x=1,
    y=-0.2,
    xref='paper',
    yref='paper',
    text=texts.get("source"),
    showarrow=False,
    xanchor='right',
    yanchor='top',
    align='right',
    font=dict(
        family="Arial",
        size=12,
        color='#666666'
    )
)

# Define output filename and save the image
base_name = os.path.splitext(os.path.basename(json_filepath))[0]
output_filename = f"{base_name}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")