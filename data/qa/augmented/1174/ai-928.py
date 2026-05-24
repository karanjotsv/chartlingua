import sys
import json
import pathlib
import plotly.graph_objects as go

# --- 1. Load data from JSON file provided as a command-line argument ---
if len(sys.argv) != 2:
    print(f"Usage: python {pathlib.Path(__file__).name} <json_file_path>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# --- 2. Extract data and text from the loaded JSON ---
chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

# --- 3. Create the Plotly figure ---
fig = go.Figure()

# Add the bar trace from the first data series
if chart_data:
    series = chart_data[0]
    fig.add_trace(go.Bar(
        x=series['x'],
        y=series['y'],
        text=series['y'],
        textposition='outside',
        cliponaxis=False,  # Prevents text labels from being clipped at the top
        marker_color=colors[0] if colors else None,
        textfont=dict(size=12, family="Arial")
    ))

# --- 4. Configure the layout ---
# Construct title and source text
title_text = texts.get('title')
if texts.get('subtitle'):
    title_text = f"{title_text}<br><sub>{texts.get('subtitle')}</sub>" if title_text else f"<sub>{texts.get('subtitle')}</sub>"

source_text = texts.get('source_text')

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left'
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        range=[0, 175],
        tickvals=[0, 25, 50, 75, 100, 125, 150, 175],
        showgrid=True,
        gridcolor='#EAEAEA',
        gridwidth=1,
        zeroline=False,
        showline=False
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=False,
        zeroline=False,
        showline=False
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=60, b=100),
    annotations=[] # Initialize empty list for annotations
)

# Add source text as an annotation if it exists
if source_text:
    fig.add_annotation(
        text=source_text,
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=1.0,
        y=-0.22,
        xanchor='right',
        yanchor='top'
    )

# --- 5. Write the output image ---
output_filename = json_path.stem + ".png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")