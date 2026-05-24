import sys
import json
import pathlib
import plotly.graph_objects as go

# --- 1. Load data from JSON file ---
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_spec = json.load(f)

# --- 2. Extract data and texts ---
chart_data = chart_spec.get('chart_data', [])
texts = chart_spec.get('texts', {})
colors = chart_spec.get('colors', [])

# --- 3. Create the figure ---
fig = go.Figure()

# --- 4. Add traces for each data series ---
for i, series in enumerate(chart_data):
    # Determine text anchor based on bar value (positive or negative)
    text_anchor = 'middle' if series.get('y', [0])[0] >= 0 else 'end'

    fig.add_trace(go.Bar(
        name=series.get('name'),
        # Use the series name as the category to separate the bars
        x=[series.get('name')],
        y=series.get('y'),
        text=[series.get('text')],
        texttemplate='%{text}',
        textposition='inside',
        insidetextanchor=text_anchor,
        textfont=dict(color='black', size=14, family="Arial"),
        marker=dict(color=colors[i]),
        error_y=series.get('error_y'),
        hoverinfo='none',
        width=0.4
    ))

# --- 5. Configure layout ---
# Combine title and subtitle if they exist
title_parts = [texts.get('title'), texts.get('subtitle')]
full_title = '<br>'.join(filter(None, title_parts))

fig.update_layout(
    font=dict(family="Arial", size=12),
    title=dict(
        text=full_title,
        x=0.05,
        xanchor='left'
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showticklabels=False, # Hide category names on the axis
        ticks="", # Hide tick marks
        showline=False,
        zeroline=False
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        range=[-250, 650],
        tickvals=[-200, 0, 200, 400, 600],
        showgrid=True,
        gridcolor='#E5E5E5',
        zeroline=True,
        zerolinecolor='black',
        zerolinewidth=1
    ),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=1.02,
        xanchor='center',
        x=0.5,
        traceorder='normal'
    ),
    margin=dict(l=80, r=40, t=100, b=80),
    bargap=0.5
)

# --- 6. Output the image ---
output_filename = f"{json_path.stem}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")