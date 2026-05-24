import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check if a file path is provided
if len(sys.argv) < 2:
    print(f"Usage: python {sys.argv[0]} <path_to_json_file>")
    sys.exit(1)

json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Load data from the JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_data_json = json.load(f)

# Extract data and texts
chart_data = chart_data_json['chart_data']
texts = chart_data_json['texts']
series_names = chart_data_json['series_names']
colors = chart_data_json['colors']

# Prepare data for plotting
years = [d['year'] for d in chart_data]
totals = [0] * len(years)

fig = go.Figure()

# Add bar traces for each series in the specified order
for i, series_name in enumerate(series_names):
    y_values = [d[series_name] for d in chart_data]
    fig.add_trace(go.Bar(
        x=years,
        y=y_values,
        name=series_name,
        marker_color=colors[i]
    ))
    # Calculate cumulative totals for annotations
    for j, val in enumerate(y_values):
        totals[j] += val

# Add annotations for total values on top of each bar
for i, total in enumerate(totals):
    if total > 0:
        # Heuristic for text color based on bar height to match original
        text_color = "#4169E1" if total > 150 else "#000000"
        fig.add_annotation(
            x=years[i],
            y=total,
            text=str(total),
            showarrow=False,
            font=dict(
                family="Arial",
                size=9,
                color=text_color
            ),
            yshift=5
        )

# Construct the title string
title_text = texts['title'] if texts['title'] else ''
if texts['subtitle']:
    title_text = f"{title_text}<br><sub>{texts['subtitle']}</sub>"

# Update layout
fig.update_layout(
    barmode='stack',
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title_text=texts['x_axis_title'],
        tickmode='linear',
        tick0=1988,
        dtick=1,
        tickangle=0
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        range=[0, 1550],
        dtick=50,
        showgrid=True,
        gridcolor='#e0e0e0',
        gridwidth=1,
        griddash='dot'
    ),
    yaxis2=dict(
        overlaying='y',
        side='right',
        range=[0, 1550],
        dtick=50,
        showgrid=False,
        showticklabels=True
    ),
    legend=dict(
        traceorder='normal',
        yanchor="top",
        y=0.98,
        xanchor="left",
        x=0.01,
        bgcolor='rgba(255, 255, 255, 0.7)'
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    plot_bgcolor='white',
    margin=dict(l=60, r=60, t=80, b=80),
    showlegend=True,
    xaxis_tickfont_size=9
)

# Generate output filename from the input JSON path
filename_base = json_path.stem
output_filename = f"{filename_base}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")