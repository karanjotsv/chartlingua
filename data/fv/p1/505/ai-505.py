import sys
import json
import pathlib
import plotly.graph_objects as go

# --- 1. Argument and File Handling ---
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <path_to_json_file>")
    sys.exit(1)

json_path_str = sys.argv[1]
json_path = pathlib.Path(json_path_str)

if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

filename_base = json_path.stem
output_filename = f"{filename_base}.png"

with open(json_path, 'r', encoding='utf-8') as f:
    chart_data_json = json.load(f)

# --- 2. Data Extraction from JSON ---
chart_data = chart_data_json.get('chart_data', [])
texts = chart_data_json.get('texts', {})
colors = chart_data_json.get('colors', [])

# --- 3. Chart Creation ---
fig = go.Figure()

# Add data series traces
for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        name=series.get('name', ''),
        mode='lines',
        line=dict(
            color=colors[i % len(colors)] if colors else None,
            width=1.5
        )
    ))

# --- 4. Layout and Styling ---

# Combine title and subtitle
title_text = texts.get('title', '')
if title_text and texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

fig.update_layout(
    font=dict(family="Arial", size=11, color="black"),
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left'
    ),
    paper_bgcolor='#DCDCDC',
    plot_bgcolor='#FAFAFA',
    showlegend=False,
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        range=[3320, 3375],
        tickmode='linear',
        tick0=3320,
        dtick=10,
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        ticks='outside'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[-450, 450],
        tickmode='linear',
        tick0=-400,
        dtick=200,
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        ticks='outside',
        zeroline=False
    ),
    margin=dict(l=40, r=20, t=20, b=40)
)

# --- 5. Output ---
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")