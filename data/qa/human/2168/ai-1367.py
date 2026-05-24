import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# --- 1. Argument Parsing and File Loading ---
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

# --- 2. Data Extraction ---
chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']
data_label_suffix = config.get('data_label_suffix', '')

# --- 3. Chart Creation ---
fig = go.Figure()

# Add a trace for each data series
for i, series in enumerate(chart_data['series']):
    fig.add_trace(go.Bar(
        name=series['name'],
        x=chart_data['categories'],
        y=series['values'],
        marker_color=colors[i],
        text=[f"<b>{v}{data_label_suffix}</b>" for v in series['values']],
        textposition='outside'
    ))

# --- 4. Layout Configuration ---
# Combine title and subtitle if they exist
title_text = ""
if texts.get('title'):
    title_text += texts['title']
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Create annotations for source and note
annotations = []
if texts.get('note'):
    annotations.append(
        dict(
            text=texts['note'],
            showarrow=False,
            xref='paper', yref='paper',
            x=0, y=-0.3,
            xanchor='left', yanchor='bottom',
            font=dict(family="Arial", size=12, color='#0066cc')
        )
    )
if texts.get('source'):
    annotations.append(
        dict(
            text=texts['source'],
            showarrow=False,
            xref='paper', yref='paper',
            x=1, y=-0.3,
            xanchor='right', yanchor='bottom',
            font=dict(family="Arial", size=12, color='#666666')
        )
    )

fig.update_layout(
    barmode='group',
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", color='#333333'),
    title=dict(
        text=title_text,
        x=0.05, y=0.95,
        xanchor='left', yanchor='top',
        font=dict(size=24)
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        showline=True,
        linecolor='black',
        linewidth=1,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=True,
        gridcolor='#e0e0e0',
        gridwidth=1,
        range=[0, 80],
        dtick=20,
        ticksuffix="%",
        zeroline=False,
        title_standoff=15,
        tickfont=dict(size=12)
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.2,
        xanchor="center",
        x=0.5,
        font=dict(size=14)
    ),
    margin=dict(l=80, r=40, b=120, t=60),
    annotations=annotations
)

fig.update_traces(
    texttemplate='%{text}',
    cliponaxis=False
)

# --- 5. Output ---
input_path = Path(json_file_path)
output_filename = f"{input_path.stem}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")