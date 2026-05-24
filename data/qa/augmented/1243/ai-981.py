import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
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

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

x_values = [item['category'] for item in chart_data]
y_values = [item['value'] for item in chart_data]

bar_texts = [f"{v:,}".replace(",", " ") for v in y_values]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    text=bar_texts,
    textposition='outside',
    marker_color=colors[0],
    showlegend=False,
    cliponaxis=False
))

annotations = []
if texts.get('source'):
    annotations.append(
        dict(
            xref='paper', yref='paper',
            x=1.0, y=-0.2,
            xanchor='right', yanchor='top',
            text=texts['source'],
            showarrow=False,
            font=dict(family='Arial', size=12, color='grey')
        )
    )

if texts.get('note'):
    annotations.append(
        dict(
            xref='paper', yref='paper',
            x=0.0, y=-0.2,
            xanchor='left', yanchor='top',
            text=texts['note'],
            showarrow=False,
            font=dict(family='Arial', size=12, color='grey')
        )
    )

fig.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12),
    margin=dict(l=80, r=40, t=40, b=120),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        range=[0, 1200000],
        tickvals=[0, 200000, 400000, 600000, 800000, 1000000, 1200000],
        ticktext=['0', '200 000', '400 000', '600 000', '800 000', '1 000 000', '1 200 000'],
        showgrid=True,
        gridcolor='#e0e0e0',
        griddash='dot',
        zeroline=False
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=False,
        zeroline=False
    ),
    annotations=annotations
)

fig.update_traces(textfont_size=12, textfont_family="Arial", textfont_color="black")

base_name = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_name}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")