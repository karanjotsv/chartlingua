import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]
text_labels = [f"{v}%" for v in values]

fig = go.Figure()

fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0]),
    text=text_labels,
    textposition='outside',
    cliponaxis=False,
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    )
))

fig.update_layout(
    font=dict(family="Arial", size=12, color='black'),
    title_text=texts.get('title'),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title=texts.get('x_axis_title'),
        range=[0, max(values) * 1.12],
        ticksuffix='%',
        showgrid=False,
        zeroline=True,
        zerolinecolor='black',
        zerolinewidth=1,
        showline=True,
        linecolor='black',
        linewidth=1
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='#dddddd',
        griddash='dot',
        categoryorder='total ascending',
        showline=True,
        linecolor='black',
        linewidth=1,
        ticks='outside',
        tickson='boundaries'
    ),
    margin=dict(l=150, r=60, t=40, b=60),
    annotations=[
        dict(
            text=texts.get('source', ''),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.99,
            y=-0.15,
            xanchor='right',
            yanchor='top',
            font=dict(size=12)
        )
    ]
)

base_path = os.path.splitext(json_file_path)[0]
output_filename = f"{base_path}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")