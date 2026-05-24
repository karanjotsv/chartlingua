import sys
import json
import plotly.graph_objects as go
import pathlib

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

categories = [item['category'] for item in data]
values = [item['value'] for item in data]

text_labels = [f'{v:,}'.replace(',', ' ') for v in values]

fig = go.Figure()

fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker_color=colors[0],
    text=text_labels,
    textposition='outside',
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    ),
    cliponaxis=False 
))

fig.update_layout(
    font=dict(
        family="Arial",
        size=12
    ),
    plot_bgcolor='white',
    xaxis=dict(
        title_text=texts['x_axis_title'],
        showgrid=True,
        gridcolor='#E5E5E5',
        griddash='dot',
        zeroline=False,
        showticklabels=True
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        showgrid=False,
        zeroline=False
    ),
    showlegend=False,
    margin=dict(l=100, r=100, t=40, b=80),
    annotations=[
        dict(
            text=texts['source'],
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.15,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(
                family="Arial",
                size=12,
                color='#6c757d'
            )
        )
    ]
)

max_value = max(values)
fig.update_xaxes(range=[0, max_value * 1.18])

output_filename_base = pathlib.Path(json_path).stem
output_png_path = f"{output_filename_base}.png"

fig.write_image(output_png_path, scale=2)

print(f"Chart saved to {output_png_path}")