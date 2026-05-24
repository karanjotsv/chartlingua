import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for required command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {pathlib.Path(__file__).name} <json_file_path>")
    sys.exit(1)

# Resolve paths
json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

output_path = json_path.with_suffix(".png")

# Load data from the specified JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

# Create figure
fig = go.Figure()

# Add traces to the figure by iterating through the data
for i, series in enumerate(chart_data):
    color = colors[i % len(colors)] if colors else None
    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        name=series.get('name'),
        mode='lines+markers',
        line=dict(color=color),
        marker=dict(
            symbol=series.get('marker', 'circle'),
            color=color,
            size=8
        )
    ))

# Combine title and subtitle using HTML for rich formatting
title_text = f"<b>{texts.get('title', '')}</b><br>{texts.get('subtitle', '')}"

# Configure layout
fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top',
        font=dict(size=18)
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        tickvals=chart_data[0]['x'] if chart_data else None,
        showgrid=True,
        gridcolor='lightgrey'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        type='log',
        range=[-1, 4],  # Corresponds to 0.1 to 10000
        tickvals=[0.1, 1, 10, 100, 1000, 10000],
        showgrid=True,
        gridcolor='lightgrey'
    ),
    legend=dict(
        orientation="v",
        yanchor="top",
        y=0.75,
        xanchor="left",
        x=1.02,
        bgcolor='rgba(0,0,0,0)' # Transparent background
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(
        family="Arial",
        size=12
    ),
    margin=dict(l=60, r=150, t=100, b=60),
    autosize=False,
    width=800,
    height=600
)

# Add axis lines to replicate the original chart's border
fig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
fig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True)

# Write the output image file
fig.write_image(output_path, scale=2)

print(f"Chart successfully generated and saved to '{output_path}'")