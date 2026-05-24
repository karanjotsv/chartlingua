import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python your_script_name.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data_list = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

fig = go.Figure()

for i, series in enumerate(chart_data_list):
    fig.add_trace(go.Bar(
        x=series.get('x'),
        y=series.get('y'),
        marker_color=colors[i % len(colors)] if colors else None
    ))

title_string = texts.get('title', '')
if texts.get('subtitle'):
    title_string = f"{title_string}<br><sub>{texts.get('subtitle')}</sub>"

fig.update_layout(
    title_text=title_string,
    title_x=0.5,
    xaxis_title_text=texts.get('x_axis_title'),
    yaxis_title_text=texts.get('y_axis_title'),
    font_family="Arial",
    plot_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        type='category',
        showline=True,
        linecolor='black',
        mirror=True,
        showgrid=False,
        ticks='outside',
        tickfont=dict(size=14),
        titlefont=dict(size=16)
    ),
    yaxis=dict(
        range=[0, 50],
        showline=True,
        linecolor='black',
        mirror=True,
        showgrid=True,
        gridcolor='#D3D3D3',
        zeroline=False,
        ticks='outside',
        tickfont=dict(size=14),
        titlefont=dict(size=16)
    ),
    margin=dict(l=90, r=40, t=90, b=80),
    titlefont=dict(size=20)
)

# Derive base filename from the input JSON path
base_filename = json_path.split('/')[-1].split('\\')[-1].split('.')[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")