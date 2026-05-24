import sys
import json
import plotly.graph_objects as go
from pathlib import Path

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

output_filename_base = json_path.stem

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]
text_labels = [f"{v:g}%" for v in values]

# Reverse data to display top-to-bottom correctly in Plotly's horizontal bar chart
categories.reverse()
values.reverse()
colors.reverse()
text_labels.reverse()

fig = go.Figure()

fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors),
    text=text_labels,
    textposition='outside',
    cliponaxis=False,
    textfont=dict(family="Arial", size=12, color='black')
))

fig.update_layout(
    title=dict(
        text=f"<b>{texts['title']}</b>",
        font=dict(family="Arial", size=24),
        x=0.01,
        y=0.95,
        xanchor='left',
        yanchor='top'
    ),
    xaxis=dict(
        showgrid=True,
        gridcolor='#e0e0e0',
        zeroline=False,
        ticks='outside',
        tickvals=[0, 20, 40, 60, 80],
        ticktext=['0%', '20%', '40%', '60%', '80%'],
        range=[0, 108]
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        ticks='',
        tickfont=dict(size=14)
    ),
    annotations=[
        dict(
            text=texts['source'],
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=-0.18,
            xanchor='left',
            yanchor='top',
            align='left',
            font=dict(family="Arial", size=12)
        )
    ],
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=120, r=60, t=100, b=150),
    showlegend=False,
    font=dict(family="Arial")
)

output_path = f"{output_filename_base}.png"
fig.write_image(output_path, scale=2)
print(f"Chart successfully saved to {output_path}")