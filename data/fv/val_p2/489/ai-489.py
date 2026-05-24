import sys
import json
import pathlib
import plotly.graph_objects as go

# --- 1. Load data from JSON file ---
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# --- 2. Extract data and texts ---
data = chart_info.get('chart_data', {})
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])
x_categories = data.get('x_categories', [])
series_data = data.get('series', [])

# --- 3. Create the chart ---
fig = go.Figure()

# Add traces for each data series
for i, series in enumerate(series_data):
    color = colors[i % len(colors)] if colors else None
    fig.add_trace(go.Scatter(
        x=x_categories,
        y=series.get('y', []),
        name=series.get('name', ''),
        mode='lines',
        line=dict(color=color, width=2),
    ))

# --- 4. Configure layout and styling ---
# Combine title and subtitle
title_text = texts.get('title', '')
subtitle_text = texts.get('subtitle')
if subtitle_text:
    title_text = f"<b>{title_text}</b><br>{subtitle_text}"

# Define custom Y-axis tick labels to match the original "K" format
y_axis_tickvals = [0, 200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400]
y_axis_ticktext = ['0', '200', '400', '600', '800', '1K', '1.20K', '1.40K', '1.60K', '1.80K', '2K', '2.20K', '2.40K']

fig.update_layout(
    font=dict(family="Arial", size=12),
    title=dict(
        text=title_text,
        x=0.01,
        y=0.98,
        xanchor='left',
        yanchor='top',
        font=dict(size=18)
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showline=True,
        linewidth=1,
        linecolor='black',
        showgrid=True,
        gridcolor='#EAEAEA',
        tickfont=dict(size=11),
        zeroline=False
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 2450],
        showline=True,
        linewidth=1,
        linecolor='black',
        showgrid=True,
        gridcolor='#EAEAEA',
        tickvals=y_axis_tickvals,
        ticktext=y_axis_ticktext,
        tickfont=dict(size=11),
        zeroline=False
    ),
    legend=dict(
        x=1.02,
        y=1,
        xanchor='left',
        yanchor='top',
        bgcolor='rgba(255,255,255,0.5)'
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=60, r=220, t=100, b=120),
    annotations=[
        dict(
            text=texts.get('source', ''),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=-0.2, # Position below x-axis
            xanchor='left',
            yanchor='top',
            align='left',
            font=dict(size=11)
        )
    ]
)

# --- 5. Save the chart as a PNG image ---
output_filename = json_path.stem + ".png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")