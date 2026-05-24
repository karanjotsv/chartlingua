import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: File not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker_color=colors,
    text=values,
    textposition='outside',
    hoverinfo='none'
))

title_parts = []
if texts.get('title') and texts['title']:
    title_parts.append(f"<b>{texts['title']}</b>")
if texts.get('subtitle') and texts['subtitle']:
    title_parts.append(f"<span style='font-size:0.8em;color:grey;'>{texts['subtitle']}</span>")
title_text = "<br>".join(title_parts)

fig.update_layout(
    template="plotly_white",
    title_text=title_text,
    title_x=0.5,
    font_family="Arial",
    font_size=12,
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    yaxis=dict(autorange='reversed'),
    xaxis=dict(gridcolor='lightgrey', griddash='dot'),
    showlegend=False,
    margin=dict(l=230, r=40, t=50, b=80),
    annotations=[
        dict(
            text=texts.get('source', ''),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.15,
            xanchor='right',
            yanchor='top',
            align='right',
            font_size=10
        )
    ]
)

fig.update_traces(cliponaxis=False)

output_filename_base = json_path.rsplit('.', 1)[0]
output_filename = f"{output_filename_base}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")