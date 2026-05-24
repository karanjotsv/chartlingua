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
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_file_path}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Failed to decode JSON from '{json_file_path}'.")
    sys.exit(1)

chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#000000', width=1)),
    textinfo='percent',
    texttemplate='%{value:.2f}%',
    hoverinfo='label+percent',
    sort=False,
    direction='clockwise',
    rotation=68
))

fig.update_traces(
    textposition='auto',
    insidetextfont=dict(family="Arial"),
    outsidetextfont=dict(family="Arial", color="white")
)

annotations = []
total_label = texts.get('total_label')
if total_label:
    annotations.append(
        go.layout.Annotation(
            text=total_label,
            align='left',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=0,
            xanchor='left',
            yanchor='bottom',
            font=dict(family="Arial", size=14, color="red")
        )
    )

fig.update_layout(
    showlegend=True,
    paper_bgcolor='#000000',
    plot_bgcolor='#000000',
    font=dict(family="Arial", color="white"),
    legend=dict(
        bgcolor='rgba(0,0,0,0)',
        bordercolor='rgba(0,0,0,0)',
        font=dict(family="Arial", color="white")
    ),
    margin=dict(l=40, r=40, t=40, b=60),
    annotations=annotations
)

base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_image_path = f"{base_filename}.png"

fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")