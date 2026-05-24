import sys
import json
import plotly.graph_objects as go
import pathlib

# --- 1. Argument and File Handling ---
if len(sys.argv) != 2:
    print(f"Usage: python {pathlib.Path(__file__).name} <json_file_path>")
    sys.exit(1)

json_file_path = pathlib.Path(sys.argv[1])
if not json_file_path.is_file():
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

output_image_path = json_file_path.with_suffix('.png')

# --- 2. Data Loading ---
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON in file '{json_file_path}'")
    sys.exit(1)

# --- 3. Chart Creation ---
fig = go.Figure()

# --- 4. Add Data Traces ---
data_series = chart_info.get('chart_data', [])
colors = chart_info.get('colors', [])
for i, series in enumerate(data_series):
    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        name=series.get('name', f'Series {i+1}'),
        mode='lines+markers',
        line=dict(color=colors[i % len(colors)]),
        marker=dict(
            symbol=series.get('marker_symbol', 'circle'),
            color=colors[i % len(colors)],
            size=8,
            line=dict(
                color='black',
                width=1
            )
        )
    ))

# --- 5. Layout and Styling ---
texts = chart_info.get('texts', {})
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        font=dict(size=18)
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        range=[2003.5, 2018.5],
        tickmode='array',
        tickvals=[2004, 2006, 2008, 2010, 2012, 2014, 2016, 2018],
        showgrid=True,
        gridcolor='darkgray',
        gridwidth=1
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 2500],
        tickmode='linear',
        dtick=500,
        showgrid=True,
        gridcolor='darkgray',
        gridwidth=1
    ),
    plot_bgcolor='#D6EAF8',
    paper_bgcolor='#C5D9E8',
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    legend=dict(
        x=1.02,
        y=0.55,
        xanchor='left',
        yanchor='middle',
        bgcolor='rgba(0,0,0,0)',
        bordercolor='black',
        borderwidth=0
    ),
    margin=dict(l=90, r=220, t=80, b=80),
    autosize=False,
    width=800,
    height=600
)

# --- 6. Image Export ---
try:
    fig.write_image(output_image_path, scale=2)
    print(f"Chart successfully generated at '{output_image_path}'")
except Exception as e:
    print(f"Error exporting image: {e}")
    sys.exit(1)