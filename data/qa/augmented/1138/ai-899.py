import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_filepath = sys.argv[1]

try:
    with open(json_filepath, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_filepath}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_filepath}")
    sys.exit(1)

chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

text_labels = []
for v in values:
    if v == int(v):
        formatted_v = f"{int(v):,}".replace(",", " ")
    else:
        # Format to 2 decimal places, then remove trailing zeros and period
        formatted_v = f"{v:,.2f}".replace(",", " ").rstrip('0').rstrip('.')
    text_labels.append(formatted_v)

fig = go.Figure()

fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0]),
    text=text_labels,
    textposition='outside',
    cliponaxis=False,
    hoverinfo='none'
))

annotations = []
if texts.get('source'):
    annotations.append(
        go.layout.Annotation(
            xref='paper', yref='paper',
            x=1, y=-0.1,
            xanchor='right', yanchor='top',
            text=texts['source'],
            showarrow=False,
            font=dict(family="Arial", size=12, color="#666666")
        )
    )
if texts.get('note'):
    annotations.append(
        go.layout.Annotation(
            xref='paper', yref='paper',
            x=0, y=-0.1,
            xanchor='left', yanchor='top',
            text=texts['note'],
            showarrow=False,
            font=dict(family="Arial", size=12, color="#0000FF") # Simulate hyperlink color
        )
    )

fig.update_layout(
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#E0E0E0',
        griddash='dot',
        zeroline=False,
        tick0=0,
        dtick=25000,
        range=[0, max(values) * 1.2]
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False
    ),
    margin=dict(l=120, r=80, t=30, b=100),
    separators=' .',
    annotations=annotations
)

base_name = pathlib.Path(json_filepath).stem
output_filename = f"{base_name}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")