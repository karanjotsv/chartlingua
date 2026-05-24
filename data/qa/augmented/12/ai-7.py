import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for the required command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_path = sys.argv[1]

# Read and parse the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and settings from the loaded JSON
chart_data = chart_config.get('chart_data', {})
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', {})
categories = chart_data.get('categories', [])
series_data = chart_data.get('series', [])
bar_colors = colors.get('bars', [])
text_on_bar_colors = colors.get('text_on_bar', [])

# Initialize the figure
fig = go.Figure()

# Add a bar trace for each data series
for i, series in enumerate(series_data):
    # Prepare text labels, making them bold and hiding zero values
    bar_text = [f"<b>{v}</b>" if v > 0 else '' for v in series['data']]
    
    fig.add_trace(go.Bar(
        x=categories,
        y=series.get('data', []),
        name=series.get('name', ''),
        marker_color=bar_colors[i] if i < len(bar_colors) else None,
        text=bar_text,
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(
            family="Arial",
            size=12,
            color=text_on_bar_colors[i] if i < len(text_on_bar_colors) else '#000000'
        )
    ))

# Combine title and subtitle if they exist
title_text = texts.get('title', '')
if title_text and texts.get('subtitle'):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

# Update layout for a clean, professional look
fig.update_layout(
    barmode='stack',
    title_text=title_text,
    yaxis_title=texts.get('y_axis_title'),
    xaxis_title=texts.get('x_axis_title'),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    xaxis=dict(
        showgrid=False,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='#e0e0e0',
        range=[0, 130],
        tickvals=[0, 25, 50, 75, 100, 125],
        tickfont=dict(size=12)
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.2,
        xanchor="center",
        x=0.5
    ),
    margin=dict(l=60, r=40, t=50, b=150),
    annotations=[
        dict(
            text=texts.get('source', ''),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.98,
            y=-0.28,
            xanchor='right',
            yanchor='bottom',
            align='right',
            font=dict(
                family="Arial",
                size=12
            )
        )
    ]
)

# Derive the output filename from the input JSON filename
output_filename = f"{pathlib.Path(json_path).stem}.png"

# Save the figure to a high-resolution PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved to {output_filename}")