import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]
text_labels = [item['text'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0]),
    text=text_labels,
    textposition='outside',
    cliponaxis=False,
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    )
))

annotations = []
if texts.get('source'):
    annotations.append(
        dict(
            text=texts['source'],
            align='right',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.99,
            y=-0.15,
            xanchor='right',
            yanchor='top',
            font=dict(family="Arial", size=12)
        )
    )
if texts.get('note'):
     annotations.append(
        dict(
            text=texts['note'],
            align='left',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=-0.15,
            xanchor='left',
            yanchor='top',
            font=dict(family="Arial", size=12)
        )
    )

fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#e0e0e0',
        gridwidth=1,
        griddash='dot',
        zeroline=False,
        showline=False,
        ticks='outside',
        ticklen=5,
        tickcolor='black',
        range=[0, max(values) * 1.15],
        dtick=250
    ),
    yaxis=dict(
        showgrid=False,
        showline=True,
        linecolor='black',
        linewidth=1,
        ticks='',
    ),
    margin=dict(l=120, r=50, t=30, b=80),
    showlegend=False,
    annotations=annotations
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_image_path = f"{base_filename}.png"

fig.write_image(output_image_path, scale=2)
print(f"Chart saved to {output_image_path}")