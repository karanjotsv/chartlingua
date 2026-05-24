import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

if not os.path.exists(json_file_path):
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info['chart_data']
texts = chart_info['texts']

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]
bar_colors = [item['color'] if item['color'] else 'rgba(0,0,0,0)' for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=bar_colors,
    width=0.6
))

for item in chart_data:
    if item.get('value') is not None and item.get('annotation'):
        fig.add_annotation(
            x=item['category'],
            y=item['value'],
            text=item['annotation'],
            showarrow=False,
            yshift=10,
            font=dict(
                family="Arial",
                size=12,
                color="black"
            ),
            bgcolor="rgba(230, 230, 230, 0.9)",
            borderpad=3,
            align="center"
        )

title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

source_parts = []
if texts.get('source'):
    source_parts.append(texts['source'])
if texts.get('note'):
    source_parts.append(texts['note'])
caption_text = "<br>".join(source_parts)

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        y=0.95,
        xanchor='center',
        yanchor='top'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 6.2],
        tickmode='linear',
        tick0=0,
        dtick=1,
        showgrid=True,
        gridcolor='lightgray',
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True
    ),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=50, r=50, t=100, b=120)
)

if caption_text:
    fig.add_annotation(
        showarrow=False,
        text=caption_text,
        xref="paper",
        yref="paper",
        x=0,
        y=-0.3, # Adjusted for potentially tall x-axis labels
        xanchor='left',
        yanchor='top',
        align='left'
    )

base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")