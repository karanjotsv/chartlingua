import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(sys.argv[0])} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]
if not os.path.exists(json_path):
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

data = config['chart_data']
texts = config['texts']
colors = config['colors']

categories = [item['category'] for item in data]
values = [item['value'] for item in data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker=dict(
        color=colors['bar_fill'],
        line=dict(
            color=colors['bar_line'],
            width=1.5
        )
    ),
    showlegend=False
))

annotations = []
for i in range(len(data)):
    annotations.append(
        dict(
            x=categories[i],
            y=values[i] / 2,
            text=str(values[i]),
            showarrow=False,
            font=dict(
                family="Arial",
                size=12,
                color="black"
            ),
            align="center",
            bordercolor=colors['annotation_border'],
            borderwidth=1.2,
            borderpad=4,
            bgcolor=colors['annotation_bg'],
            opacity=1
        )
    )

title_text = f"<b>{texts['title']}</b><br>{texts['subtitle']}"

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        y=0.95,
        xanchor='center',
        yanchor='top'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        tickfont=dict(family="Arial", size=11),
        automargin=True
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        title_font=dict(family="Arial", size=12),
        range=[0, 4500],
        tickvals=[0, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500],
        gridcolor=colors['grid'],
        showgrid=True,
        tickfont=dict(family="Arial", size=12)
    ),
    plot_bgcolor=colors['background'],
    paper_bgcolor='white',
    font=dict(family="Arial", size=12),
    margin=dict(l=70, r=30, t=100, b=120),
    annotations=annotations
)

base_filename, _ = os.path.splitext(json_path)
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")