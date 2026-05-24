import sys
import json
import pathlib
import plotly.graph_objects as go

# --- 1. Load data from JSON file provided as a command-line argument ---
if len(sys.argv) < 2:
    print(f"Usage: python {sys.argv[0]} <path_to_json_file>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON in {json_path}")
    sys.exit(1)

# --- 2. Extract data and configuration from the loaded JSON ---
chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])
filename_base = json_path.stem

# --- 3. Create the plot using Plotly ---
fig = go.Figure()

for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        x=series.get('x', []),
        y=series.get('y', []),
        name=series.get('name', ''),
        marker_color=colors[i % len(colors)] if colors else None
    ))

# --- 4. Configure layout and styling ---
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text = f"<b>{title_text}</b><br><sub>{texts['subtitle']}</sub>"

fig.update_layout(
    barmode='group',
    title={
        'text': title_text,
        'x': 0.5,
        'xanchor': 'center'
    },
    xaxis={
        'title_text': texts.get('x_axis_title'),
        'tickangle': -45,
        'showline': True,
        'linewidth': 1,
        'linecolor': 'lightgray',
        'ticks': 'outside'
    },
    yaxis={
        'title_text': texts.get('y_axis_title'),
        'gridcolor': 'lightgray',
        'showline': True,
        'linewidth': 1,
        'linecolor': 'lightgray',
        'ticks': 'outside',
        'range': [0, 3500],
        'dtick': 500
    },
    legend={
        'orientation': 'h',
        'yanchor': 'bottom',
        'y': 1.02,
        'xanchor': 'center',
        'x': 0.5
    },
    plot_bgcolor='white',
    paper_bgcolor='white',
    font={'family': 'Arial'},
    margin={'t': 80, 'b': 150, 'l': 80, 'r': 40}
)

# --- 5. Save the chart as a PNG image ---
output_filename = f"{filename_base}.png"
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")