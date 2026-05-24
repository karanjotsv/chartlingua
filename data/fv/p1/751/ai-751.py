import sys
import json
import pathlib
import plotly.graph_objects as go

# --- 1. Load data from JSON file ---
if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data and texts
chart_data = chart_info.get('chart_data', {})
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])
categories = chart_data.get('categories', [])
series = chart_data.get('series', [])

# --- 2. Create the Plotly figure ---
fig = go.Figure()

# Add traces for each series
for i, s in enumerate(series):
    fig.add_trace(go.Scatter(
        x=categories,
        y=s.get('y', []),
        name=s.get('name', ''),
        mode='lines',
        line=dict(color=colors[i], width=2)
    ))

# --- 3. Update layout and styling ---
title_parts = [texts.get('title'), texts.get('subtitle')]
full_title = '<br>'.join(filter(None, title_parts))

source_parts = [texts.get('source')]
full_source = '<br>'.join(filter(None, source_parts))

fig.update_layout(
    title=dict(
        text=full_title,
        x=0.5,
        xanchor='center'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        type='category',
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='lightgray'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 100],
        tickformat='.1f',
        ticksuffix='%',
        gridcolor='lightgray',
        showline=True,
        linewidth=1,
        linecolor='lightgray'
    ),
    legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.2,
        xanchor="center",
        x=0.5
    ),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=60, r=40, t=90, b=100),
    annotations=[
        dict(
            text=full_source,
            showarrow=False,
            xref='paper', yref='paper',
            x=0, y=-0.25,
            xanchor='left', yanchor='top',
            align='left'
        )
    ] if full_source else []
)

# --- 4. Output the image ---
output_filename = json_path.with_suffix('.png')
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")