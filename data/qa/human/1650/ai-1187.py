import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(sys.argv[0])} <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

fig = go.Figure()

for i, series in enumerate(data):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        mode='lines+markers',
        name=series['name'],
        line=dict(color=colors[i], width=2),
        marker=dict(color=colors[i], size=5),
        showlegend=False
    ))

title_text = f"<b style='color:#333333'>{texts['title']}</b><br><span style='font-size:16px; color:#555555'>{texts['subtitle']}</span>"

annotations = [
    dict(
        x=data[0]['x'][-1],
        y=data[0]['y'][-1],
        text=data[0]['name'],
        showarrow=False,
        xanchor='left',
        yanchor='middle',
        xshift=8,
        font=dict(family="Arial", size=14, color=colors[0])
    ),
    dict(
        xref='paper', yref='paper',
        x=0, y=-0.18,
        xanchor='left', yanchor='top',
        text=texts['source'],
        showarrow=False,
        align='left',
        font=dict(family="Arial", size=12, color='#666666')
    ),
    dict(
        xref='paper', yref='paper',
        x=1.0, y=-0.18,
        xanchor='right', yanchor='top',
        text=texts['note'],
        showarrow=False,
        align='right',
        font=dict(family="Arial", size=12, color='#666666')
    )
]

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.01,
        y=0.98,
        xanchor='left',
        yanchor='top',
        font=dict(size=24)
    ),
    xaxis=dict(
        tickvals=[1961, 1965, 1970, 1975, 1981],
        tickformat='d',
        showline=True,
        linewidth=1,
        linecolor='lightgray',
        showgrid=False,
        zeroline=False,
        domain=[0.01, 0.99]
    ),
    yaxis=dict(
        range=[0, 26],
        tickvals=[0, 5, 10, 15, 20],
        ticksuffix=' t',
        showgrid=True,
        gridcolor='lightgray',
        griddash='dash',
        zeroline=False,
        showline=False
    ),
    font=dict(family="Arial", size=14),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=60, r=60, t=120, b=100),
    autosize=False,
    width=800,
    height=600,
    annotations=annotations
)

base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")