import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

labels = [d['label'] for d in chart_data]
values = [d['value'] for d in chart_data]
text_on_slices = [d['text'] for d in chart_data]

fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    text=text_on_slices,
    textinfo='text',
    hoverinfo='label+percent',
    marker_colors=colors,
    sort=False,
    insidetextfont=dict(color='white', size=14)
)])

fig.update_layout(
    title=dict(
        text=texts.get('title'),
        y=0.95,
        x=0.05,
        xanchor='left',
        yanchor='top',
        font=dict(size=24, color='#808080')
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    legend=dict(
        orientation="v",
        yanchor="top",
        y=0.9,
        xanchor="right",
        x=1,
        bgcolor='rgba(0,0,0,0)'
    ),
    margin=dict(l=20, r=20, t=100, b=20),
    showlegend=True,
    paper_bgcolor='white',
    plot_bgcolor='white'
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_image_file = f"{base_filename}.png"

fig.write_image(output_image_file, scale=2)

print(f"Chart saved to {output_image_file}")