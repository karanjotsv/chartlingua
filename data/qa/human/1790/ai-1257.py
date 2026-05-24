import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file>")
    sys.exit(1)

json_path = sys.argv[1]
output_filename_base = os.path.splitext(os.path.basename(json_path))[0]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error loading JSON file: {e}")
    sys.exit(1)

data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

categories = [item['category'] for item in data]
values = [item['value'] for item in data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors,
    text=[f'{v:.1f}' for v in values],
    textposition='outside',
    textfont=dict(
        family="Arial",
        size=12,
        color=colors
    ),
    cliponaxis=False
))

title_text = f"<b>{texts['title']}</b>   <span style='color:#595959;'>{texts['subtitle']}</span>"

annotations = []
annotations.append(dict(
    text=texts['source'],
    xref="paper", yref="paper",
    x=0.99, y=0.98,
    xanchor='right', yanchor='bottom',
    showarrow=False,
    font=dict(family="Arial", size=12, color='#595959')
))

for i, category in enumerate(categories):
    annotations.append(dict(
        x=category,
        y=0,
        yref='paper',
        yshift=-35,
        text=f"<i>{category}</i>",
        showarrow=False,
        font=dict(color=colors[i], family="Arial", size=11),
        textangle=-45
    ))

fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95, x=0.01,
        xanchor='left', yanchor='top',
        font=dict(family="Arial", size=22, color='black')
    ),
    font=dict(family="Arial", size=12),
    plot_bgcolor='#EAF2F5',
    paper_bgcolor='white',
    xaxis=dict(
        showgrid=False,
        showline=False,
        zeroline=False,
        showticklabels=False
    ),
    yaxis=dict(
        range=[0, 16],
        dtick=2,
        showline=False,
        zeroline=False,
        gridcolor='white',
        gridwidth=1.5,
        tickfont=dict(size=11, color='#595959')
    ),
    showlegend=False,
    margin=dict(l=40, r=40, t=110, b=80),
    annotations=annotations,
    shapes=[
        dict(
            type="line", xref="paper", yref="paper",
            x0=0, y0=0.88, x1=1, y1=0.88,
            line=dict(color="#005A8D", width=1.5)
        ),
        dict(
            type="line", xref="paper", yref="paper",
            x0=0, y0=-0.22, x1=1, y1=-0.22,
            line=dict(color="#005A8D", width=1.5)
        )
    ]
)

output_image_path = f"{output_filename_base}.png"
fig.write_image(output_image_path, scale=2)
print(f"Chart saved to {output_image_path}")