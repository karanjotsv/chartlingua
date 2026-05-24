import sys
import json
from pathlib import Path
import plotly.graph_objects as go

# --- 1. Argument and File Handling ---
if len(sys.argv) != 2:
    print(f"Usage: python {Path(__file__).name} <json_file_path>")
    sys.exit(1)

json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

output_path = json_path.with_suffix(".png")

# --- 2. Data Loading ---
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except (json.JSONDecodeError, IOError) as e:
    print(f"Error reading or parsing JSON file: {e}")
    sys.exit(1)

chart_data = chart_info.get('chart_data', {})
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])
categories = chart_data.get('categories', [])
series_list = chart_data.get('series', [])

# --- 3. Chart Creation ---
fig = go.Figure()

for i, series in enumerate(series_list):
    fig.add_trace(go.Bar(
        y=categories,
        x=series.get('data', []),
        name=series.get('name', ''),
        orientation='h',
        marker_color=colors[i % len(colors)] if colors else None
    ))

# --- 4. Layout and Styling ---
title_str_parts = []
if texts.get('title'):
    title_str_parts.append(f"<b>{texts['title']}</b>")
if texts.get('subtitle'):
    title_str_parts.append(f"<span style='font-size: 14px;'>{texts['subtitle']}</span>")
full_title = "<br>".join(title_str_parts)

source_str = texts.get('source', '')

fig.update_layout(
    barmode='group',
    font={'family': "Arial", 'size': 12},
    title={
        'text': full_title,
        'y': 0.95,
        'x': 0.05,
        'xanchor': 'left',
        'yanchor': 'top'
    },
    xaxis={
        'title_text': texts.get('x_axis_title'),
        'showgrid': True,
        'gridcolor': 'lightgray',
        'gridwidth': 1,
        'showline': True,
        'linewidth': 1,
        'linecolor': 'black',
        'mirror': True,
        'zeroline': False,
        'range': [0, 90]
    },
    yaxis={
        'title_text': texts.get('y_axis_title'),
        'showgrid': False,
        'showline': True,
        'linewidth': 1,
        'linecolor': 'black',
        'mirror': True,
        'zeroline': False,
        'categoryorder': 'trace'
    },
    legend={
        'orientation': "h",
        'yanchor': "bottom",
        'y': -0.3,
        'xanchor': "center",
        'x': 0.5
    },
    margin={'l': 280, 'r': 30, 't': 50, 'b': 120},
    plot_bgcolor='white',
    paper_bgcolor='white'
)

if source_str:
    fig.add_annotation(
        text=source_str,
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0,
        y=-0.35,
        xanchor='left',
        yanchor='bottom',
        font={'size': 10}
    )

# --- 5. Output ---
fig.write_image(output_path, scale=2)
print(f"Chart saved to {output_path}")