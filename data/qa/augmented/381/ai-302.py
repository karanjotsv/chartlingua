import sys
import json
import pathlib
import plotly.graph_objects as go

# --- 1. Argument and File Handling ---
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

output_path = json_path.with_suffix('.png')

# --- 2. Load Data from JSON ---
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# --- 3. Create Chart ---
fig = go.Figure()

# Add bar traces from the data
for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        x=series['x'],
        y=series['y'],
        name=series.get('name', ''),
        marker_color=colors[i % len(colors)],
        text=series['y'],
        textposition='outside',
        cliponaxis=False,
        textfont=dict(family="Arial", size=12, color='black')
    ))

# --- 4. Configure Layout ---
# Combine title and subtitle if they exist
title_text = ""
if texts.get("title"):
    title_text += texts["title"]
if texts.get("subtitle"):
    title_text += f'<br><sup>{texts["subtitle"]}</sup>'

fig.update_layout(
    title_text=title_text,
    font_family="Arial",
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        showline=False,
        zeroline=False,
        tickfont=dict(family="Arial", size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 40],
        dtick=5,
        showgrid=True,
        gridcolor='#e9e9e9',
        zeroline=False,
        tickfont=dict(family="Arial", size=12)
    ),
    margin=dict(l=80, r=40, t=60, b=80)
)

# Add source annotation
if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0.99,
        y=-0.15,
        font=dict(family="Arial", size=12, color="grey")
    )

# --- 5. Output Image ---
fig.write_image(output_path, scale=2)
print(f"Chart saved to {output_path}")