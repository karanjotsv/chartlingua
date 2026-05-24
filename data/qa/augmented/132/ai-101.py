import sys
import json
import plotly.graph_objects as go
from pathlib import Path

if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

categories = [item['category'] for item in chart_data]
legend_labels = texts['legend_labels']

fig = go.Figure()

for i, label in enumerate(legend_labels):
    values = [item['values'][i] for item in chart_data]
    text_labels = [f'{int(v)}%' if v == int(v) else f'{v}%' for v in values]
    
    fig.add_trace(go.Bar(
        x=categories,
        y=values,
        name=label,
        marker_color=colors[i],
        text=text_labels,
        textposition='outside',
        cliponaxis=False
    ))

fig.update_layout(
    barmode='group',
    font_family="Arial",
    plot_bgcolor='white',
    paper_bgcolor='white',
    yaxis=dict(
        title_text=texts['y_axis_label'],
        range=[0, 41],
        tickvals=[0, 10, 20, 30, 40],
        ticktext=['0%', '10%', '20%', '30%', '40%'],
        showgrid=True,
        gridcolor='#e6e6e6',
        zeroline=False
    ),
    xaxis=dict(
        title_text=texts['x_axis_label'],
        tickangle=0,
        showline=True,
        linecolor='lightgrey'
    ),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=-0.6,
        xanchor='center',
        x=0.5,
        bgcolor='rgba(0,0,0,0)'
    ),
    margin=dict(l=80, r=40, t=40, b=250),
    annotations=[
        dict(
            text=texts['source'],
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.7,
            xanchor='right',
            yanchor='bottom',
            align='right',
            font=dict(size=12, color='#666666')
        )
    ]
)

fig.update_traces(textfont_size=12, textangle=0)

output_filename = Path(json_path).stem + '.png'
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")