import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

# Extract categories and values, then reverse for top-to-bottom display in Plotly
categories = [item['category'] for item in data]
values = [item['value'] for item in data]
categories.reverse()
values.reverse()

fig = go.Figure()

fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker_color=colors[0],
    text=values,
    textposition='outside',
    texttemplate='%{text:,}'.replace(',', ' '),
    cliponaxis=False
))

annotations = []
if texts.get('note'):
    annotations.append(
        dict(
            xref='paper', yref='paper',
            x=0, y=-0.1,
            xanchor='left', yanchor='top',
            text=texts['note'],
            showarrow=False,
            font=dict(family="Arial", size=12, color="#666666")
        )
    )
if texts.get('source'):
    annotations.append(
        dict(
            xref='paper', yref='paper',
            x=1, y=-0.1,
            xanchor='right', yanchor='top',
            text=texts['source'],
            showarrow=False,
            font=dict(family="Arial", size=12, color="#666666")
        )
    )

fig.update_layout(
    font=dict(family="Arial"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=100, r=60, t=30, b=80),
    xaxis=dict(
        title=texts['x_axis_title'],
        title_font=dict(size=12),
        showgrid=True,
        gridcolor='#EAEAEA',
        griddash='dot',
        zeroline=False,
        showline=False,
        separatethousands=True,
        range=[0, max(values) * 1.3]
    ),
    yaxis=dict(
        showline=True,
        linewidth=1,
        linecolor='black',
        tickfont=dict(size=12)
    ),
    annotations=annotations
)

base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_image_path = f"{base_filename}.png"

fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")