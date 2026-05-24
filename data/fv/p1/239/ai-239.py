import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

if not os.path.exists(json_path):
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

fig = go.Figure()

for i, series in enumerate(config['chart_data']):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        name=series['name'],
        mode='lines',
        line=dict(color=config['colors'][i], width=2.5)
    ))

annotations = []
if 'annotations' in config['texts']:
    for ann in config['texts']['annotations']:
        annotation_item = {
            'x': ann['x'],
            'y': ann['y'],
            'text': ann['text'],
            'showarrow': ann['showarrow'],
            'font': dict(
                family="Arial",
                size=16,
                color=ann.get('font_color', '#000000')
            ),
            'xref': 'x',
            'yref': 'y',
            'align': 'center'
        }
        if ann['showarrow']:
            annotation_item.update({
                'ax': ann.get('ax', 0),
                'ay': ann.get('ay', -40),
                'arrowcolor': ann.get('arrow_color', '#000000'),
                'arrowwidth': ann.get('arrow_width', 1.5),
                'arrowhead': 0
            })
        annotations.append(annotation_item)

texts = config['texts']
fig.update_layout(
    plot_bgcolor='white',
    legend_title_text=texts.get('legend_title'),
    legend=dict(
        x=0.98,
        y=0.98,
        xanchor='right',
        yanchor='top',
        bordercolor='black',
        borderwidth=1,
        font=dict(family="Arial", size=12)
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showline=True,
        linewidth=2,
        linecolor='black',
        showgrid=False,
        zeroline=False,
        ticks='outside'
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        showline=True,
        linewidth=2,
        linecolor='black',
        showgrid=False,
        zeroline=False,
        showticklabels=False,
        ticks='outside',
        range=config.get('y_range')
    ),
    font=dict(
        family="Arial",
        size=14
    ),
    margin=dict(l=80, r=40, t=40, b=80),
    annotations=annotations
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")