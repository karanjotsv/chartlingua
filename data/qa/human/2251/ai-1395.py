import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python recreate_chart.py <path_to_json_file>")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error reading or parsing JSON file: {e}")
    sys.exit(1)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

fig = go.Figure()

for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        x=series['x'],
        y=series['y'],
        name=series['name'],
        marker_color=colors[i],
        text=[f'{val}%' for val in series['y']],
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(color='white', size=12, family="Arial")
    ))

annotations = []
if texts.get('source'):
    annotations.append(
        go.layout.Annotation(
            text=texts['source'],
            align='right',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.25,
            xanchor='right',
            yanchor='bottom',
            font=dict(family="Arial", size=12, color="#666666")
        )
    )

fig.update_layout(
    barmode='stack',
    title=None,
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        linecolor='black',
        linewidth=1,
        ticks='outside'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 125],
        tickvals=[0, 25, 50, 75, 100, 125],
        ticktext=['0%', '25%', '50%', '75%', '100%', '125%'],
        gridcolor='#EAEAEA',
        zeroline=False
    ),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=-0.2,
        xanchor='center',
        x=0.5
    ),
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=80, r=40, t=40, b=150),
    annotations=annotations
)

base_filename = json_file_path.split('/')[-1].split('\\')[-1].rsplit('.', 1)[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")