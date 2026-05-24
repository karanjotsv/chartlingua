import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_path}'")
    sys.exit(1)

chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

fig = go.Figure()

for i, item in enumerate(chart_data):
    fig.add_trace(go.Bar(
        x=[item['weapon']],
        y=[item['value']],
        name=item['weapon'],
        marker=dict(
            color=colors[i % len(colors)],
            line=dict(color='black', width=1)
        ),
        showlegend=True
    ))

fig.update_layout(
    title=dict(
        text=texts.get('title'),
        x=0.5,
        y=0.95,
        xanchor='center',
        yanchor='top'
    ),
    yaxis_title=texts.get('y_axis_title'),
    font=dict(family="Arial"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    barmode='group',
    legend=dict(
        traceorder='normal'
    ),
    xaxis=dict(
        showticklabels=False,  # Hides x-axis labels to match the original image
        showgrid=False,
        showline=True,
        linecolor='black',
        zeroline=False,
        title_text=texts.get('x_axis_title')
    ),
    yaxis=dict(
        range=[0, 60],
        tick0=0,
        dtick=10,
        showgrid=True,
        gridcolor='#cccccc',
        showline=True,
        linecolor='black',
        zeroline=False
    ),
    margin=dict(l=80, r=40, t=100, b=40)
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_image_path = f"{base_filename}.png"

fig.write_image(output_image_path, scale=2)
print(f"Chart saved to {output_image_path}")