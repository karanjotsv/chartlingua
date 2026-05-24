import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_file_path = sys.argv[1]

with open(json_file_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

x_values = [d['x'] for d in chart_data]
y_values = [d['y'] for d in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    marker_color=colors[0],
    text=[f'{y:,}'.replace(',', ' ') for y in y_values],
    textposition='outside',
    textfont=dict(family="Arial", size=12, color='black'),
    cliponaxis=False
))

fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    title=dict(
        text=texts.get('title') if texts.get('title') else '',
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        zeroline=False,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 1250000],
        tickvals=[0, 200000, 400000, 600000, 800000, 1000000, 1200000],
        ticktext=['0', '200 000', '400 000', '600 000', '800 000', '1 000 000', '1 200 000'],
        gridcolor='#E0E0E0',
        zeroline=False,
        tickfont=dict(size=12)
    ),
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=80, b=100),
    annotations=[
        dict(
            text=texts.get('source', ''),
            showarrow=False,
            xref='paper', yref='paper',
            x=1, y=-0.18,
            xanchor='right', yanchor='top',
            align='right',
            font=dict(size=10, color='#666666')
        )
    ]
)

base_filename = json_file_path.split('/')[-1].split('\\')[-1].replace('.json', '')
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)