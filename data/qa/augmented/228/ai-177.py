import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
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

x_values = [item['x'] for item in chart_data]
y_values = [item['y'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    text=y_values,
    textposition='outside',
    marker_color=colors[0] if colors else None,
    textfont=dict(family="Arial", size=12, color='black'),
    cliponaxis=False
))

# Combine source and note for the footer
source_text = texts.get('source')
note_text = texts.get('note')
footer_elements = [text for text in [source_text, note_text] if text]
footer_html = "<br>".join(footer_elements)

fig.update_layout(
    font=dict(family="Arial", size=12, color='black'),
    title_text=texts.get('title'),
    yaxis_title_text=texts.get('y_axis_title'),
    xaxis_title_text=texts.get('x_axis_title'),
    showlegend=False,
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis=dict(
        type='category',
        categoryorder='array',
        categoryarray=x_values,
        showgrid=False,
        showline=True,
        linecolor='black',
        linewidth=1,
        ticks='outside',
        tickfont=dict(family="Arial", size=12)
    ),
    yaxis=dict(
        range=[0, 1800],
        dtick=250,
        showgrid=True,
        gridcolor='#e0e0e0',
        gridwidth=1,
        showline=False,
        ticks='outside',
        tickfont=dict(family="Arial", size=12)
    ),
    margin=dict(l=80, r=40, t=50, b=100),
)

if footer_html:
    fig.add_annotation(
        text=footer_html,
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=1,
        y=-0.15,
        xanchor='right',
        yanchor='top',
        font=dict(family="Arial", size=10, color='grey')
    )

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")