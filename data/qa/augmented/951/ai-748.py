import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(sys.argv[0])} <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_details = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_file_path}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: The file '{json_file_path}' contains invalid JSON.")
    sys.exit(1)

chart_data = chart_details['chart_data']
texts = chart_details['texts']
colors = chart_details['colors']

fig = go.Figure()

for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        mode='lines+markers',
        line=dict(color=colors[i % len(colors)], width=2.5),
        marker=dict(color=colors[i % len(colors)], size=8),
        name=series.get('series_name', '')
    ))

title_text_parts = []
if texts.get('title'):
    title_text_parts.append(f"<b>{texts['title']}</b>")
if texts.get('subtitle'):
    title_text_parts.append(texts['subtitle'])
full_title = "<br>".join(title_text_parts)

fig.update_layout(
    title_text=full_title if full_title else None,
    title_x=0.05,
    title_xanchor='left',
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    xaxis=dict(
        type='category',
        showgrid=True,
        gridcolor='#f0f0f0',
        gridwidth=1
    ),
    yaxis=dict(
        range=[75, 81.5],
        tickmode='linear',
        tick0=75,
        dtick=1,
        gridcolor='lightgrey',
        griddash='dot'
    ),
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=50, b=80),
)

if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        xref="paper", yref="paper",
        x=1, y=0,
        xanchor='right', yanchor='top',
        yshift=-30,
        showarrow=False,
        align='right',
        font=dict(size=12)
    )

output_base_name = os.path.splitext(os.path.basename(json_file_path))[0]
output_image_path = f"{output_base_name}.png"

fig.write_image(output_image_path, scale=2)

print(f"Chart successfully generated and saved to '{output_image_path}'.")