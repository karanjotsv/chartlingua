import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_spec = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_file_path}'")
    sys.exit(1)

data = chart_spec['chart_data']
texts = chart_spec['texts']
colors = chart_spec['colors']

fig = go.Figure()

for i, series in enumerate(data):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        mode='lines+markers',
        name=series.get('name', ''),
        line=dict(color=colors[i % len(colors)]),
        marker=dict(color=colors[i % len(colors)])
    ))

title_text = ""
if texts.get("title"):
    title_text += f'<b>{texts["title"]}</b>'
if texts.get("subtitle"):
    title_text += f'<br><sub>{texts["subtitle"]}</sub>'

annotation_text = ""
if texts.get("source"):
    annotation_text += f'Source: {texts["source"]}'
if texts.get("note"):
    if annotation_text:
        annotation_text += "<br>"
    annotation_text += f'Note: {texts["note"]}'

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        xanchor='center',
        yanchor='top',
        y=0.95
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#d3d3d3',
        zeroline=False,
        range=[1860, 2025],
        tickvals=[1860, 1880, 1900, 1920, 1940, 1960, 1980, 2000, 2020]
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=True,
        gridcolor='#d3d3d3',
        zeroline=False,
        range=[0, 260],
        tickvals=[0, 50, 100, 150, 200, 250]
    ),
    font=dict(
        family="Arial"
    ),
    showlegend=False,
    plot_bgcolor='white',
    margin=dict(l=50, r=30, t=80, b=80),
)

if annotation_text:
    fig.add_annotation(
        text=annotation_text,
        xref="paper", yref="paper",
        x=0, y=-0.15,
        xanchor='left', yanchor='top',
        showarrow=False,
        align='left',
        font=dict(size=10)
    )

base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")