import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

fig = go.Figure()

annotations = []

for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        name=series['name'],
        mode='lines+markers',
        line=dict(color=colors[i], width=2),
        marker=dict(color=colors[i], size=5),
        showlegend=False
    ))
    
    annotations.append(dict(
        x=series['x'][-1],
        y=series['y'][-1],
        xref="x",
        yref="y",
        text=series['name'],
        showarrow=False,
        xanchor='left',
        yanchor='middle',
        xshift=8,
        font=dict(family="Arial", size=14, color=colors[i])
    ))

title_text = f"<b>{texts['title']}</b>"
if texts.get('subtitle'):
    title_text += f"<br><span style='font-size: 16px;'>{texts['subtitle']}</span>"

annotations.extend([
    dict(
        x=0, y=-0.12, xref='paper', yref='paper',
        text=texts['source'],
        showarrow=False, xanchor='left', yanchor='top',
        align='left', font=dict(family="Arial", size=10, color='#7f7f7f')
    ),
    dict(
        x=1, y=-0.12, xref='paper', yref='paper',
        text=texts['note'],
        showarrow=False, xanchor='right', yanchor='top',
        align='right', font=dict(family="Arial", size=10, color='#7f7f7f')
    )
])

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.01, xanchor='left',
        y=0.98, yanchor='top',
        font=dict(family="Arial", size=24, color='#333333')
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showline=True, linecolor='black', linewidth=1,
        tickvals=[1965, 1970, 1975, 1980, 1984],
        showgrid=False
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showline=False,
        showgrid=True, gridcolor='#e0e0e0', gridwidth=1,
        zeroline=False,
        range=[0, 13],
        tickvals=[0, 2, 4, 6, 8, 10, 12],
        ticksuffix=" MWh"
    ),
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=60, r=120, t=90, b=100),
    annotations=annotations,
    width=900,
    height=600
)

base_name = json_path.split('/')[-1].split('\\')[-1].replace('.json', '')
output_filename = f"{base_name}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")