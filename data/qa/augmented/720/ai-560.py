import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
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

chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

fig = go.Figure()

if chart_data:
    x_values = [d['x'] for d in chart_data]
    y_values = [d['y'] for d in chart_data]
    
    fig.add_trace(go.Bar(
        x=x_values,
        y=y_values,
        marker_color=colors[0] if colors else None,
        text=y_values,
        textposition='outside',
        texttemplate='%{text:.2f}',
        hoverinfo='none',
        cliponaxis=False
    ))

title_parts = []
if texts.get('title'):
    title_parts.append(f"<b>{texts['title']}</b>")
if texts.get('subtitle'):
    title_parts.append(f"<sub>{texts['subtitle']}</sub>")
full_title = "<br>".join(title_parts)

fig.update_layout(
    title_text=full_title,
    title_x=0.5,
    yaxis_title=texts.get('yaxis_title'),
    xaxis_title=texts.get('xaxis_title'),
    font=dict(
        family="Arial",
        size=12
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=60, b=100),
    xaxis=dict(
        showgrid=False,
        showline=True,
        linecolor='black'
    ),
    yaxis=dict(
        range=[0, 150],
        dtick=25,
        gridcolor='#E5E5E5',
        showline=False
    ),
    annotations=[
        dict(
            text=texts.get('source', ''),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.98,
            y=-0.2,
            xanchor='right',
            yanchor='bottom',
            font=dict(
                size=12,
                color='#7f7f7f'
            )
        )
    ]
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")