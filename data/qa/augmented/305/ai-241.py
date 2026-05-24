import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python script.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

x_values = [d['category'] for d in data]
y_values = [d['value'] for d in data]

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=x_values,
    y=y_values,
    mode='lines+markers',
    line=dict(color=colors[0], width=2),
    marker=dict(color=colors[0], size=6),
    showlegend=False
))

title_text = ""
if texts.get("title"):
    title_text += texts["title"]
if texts.get("subtitle"):
    title_text += f"<br><sup>{texts['subtitle']}</sup>"

fig.update_layout(
    title=dict(text=title_text, x=0.05, xanchor='left'),
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12, color="#555555"),
    margin=dict(l=60, r=40, t=60, b=120),
    xaxis=dict(
        showgrid=False,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='#e5e5e5',
        gridwidth=1,
        range=[10, 45],
        dtick=5,
        ticksuffix='%',
        tickfont=dict(size=12)
    )
)

if texts.get("note"):
    fig.add_annotation(
        text=texts['note'],
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0,
        y=-0.2,
        xanchor='left',
        yanchor='top'
    )

if texts.get("source"):
    fig.add_annotation(
        text=texts['source'],
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=1,
        y=-0.2,
        xanchor='right',
        yanchor='top'
    )

output_filename_base = pathlib.Path(json_file_path).stem
output_filename_png = f"{output_filename_base}.png"

fig.write_image(output_filename_png, scale=2)
print(f"Chart saved to {output_filename_png}")