import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error reading or parsing JSON file: {e}")
    sys.exit(1)

data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

labels = [d['label'] for d in data]
values = [d['value'] for d in data]
display_texts = [d['display_text'] for d in data]

fig = go.Figure(data=[
    go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors, line=dict(color='#FFFFFF', width=1)),
        text=display_texts,
        textinfo='text',
        textposition='outside',
        hoverinfo='label+percent',
        sort=False,
        direction='counterclockwise'
    )
])

fig.update_layout(
    showlegend=False,
    paper_bgcolor='white',
    plot_bgcolor='white',
    font=dict(
        family="Arial",
        size=14,
        color="black"
    ),
    margin=dict(l=80, r=80, t=40, b=80)
)

if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0.98,
        y=0,
        xanchor='right',
        yanchor='top',
        font=dict(size=12, color='grey')
    )
    
output_path = pathlib.Path(json_path).with_suffix('.png')
fig.write_image(str(output_path), scale=2, width=800, height=600)

print(f"Chart saved to {output_path}")