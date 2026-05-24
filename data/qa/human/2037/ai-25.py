import sys
import json
import plotly.graph_objects as go
import os

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)

chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', {})

x_values = [item['category'] for item in chart_data]
y_values = [item['value'] for item in chart_data]
text_labels = [f"<b>{y}</b>" for y in y_values]

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=x_values,
    y=y_values,
    mode='lines+markers+text',
    line=dict(color=colors.get('series', ['#3579D6'])[0], width=3),
    marker=dict(color=colors.get('series', ['#3579D6'])[0], size=8),
    text=text_labels,
    textposition='top center',
    textfont=dict(
        family="Arial",
        size=12,
        color=colors.get('text', '#333333')
    ),
    hoverinfo='none'
))

annotations = []
if texts.get('note'):
    annotations.append(
        dict(
            xref='paper', yref='paper',
            x=0, y=-0.15,
            xanchor='left', yanchor='top',
            text=texts['note'],
            showarrow=False,
            font=dict(family='Arial', size=12, color=colors.get('note', '#337ab7'))
        )
    )

if texts.get('source'):
    annotations.append(
        dict(
            xref='paper', yref='paper',
            x=1, y=-0.15,
            xanchor='right', yanchor='top',
            text=texts['source'],
            showarrow=False,
            font=dict(family='Arial', size=12, color=colors.get('axes_labels', '#6c757d'))
        )
    )

fig.update_layout(
    title_text=texts.get('title'),
    yaxis_title_text=texts.get('y_axis_title'),
    font=dict(family="Arial"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        showgrid=False,
        zeroline=False,
        tickfont=dict(color=colors.get('axes_labels', '#6c757d'))
    ),
    yaxis=dict(
        range=[200, 700],
        gridcolor='#EAEAEA',
        zeroline=False,
        title_font=dict(color=colors.get('axes_labels', '#6c757d')),
        tickfont=dict(color=colors.get('axes_labels', '#6c757d'))
    ),
    margin=dict(l=60, r=40, t=40, b=100),
    annotations=annotations
)

base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")