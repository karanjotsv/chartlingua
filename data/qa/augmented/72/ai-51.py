import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

fig = go.Figure()

if chart_data:
    x_values = [d['x'] for d in chart_data]
    y_values = [d['y'] for d in chart_data]
    text_labels = [d.get('label', str(d['y'])) for d in chart_data]

    fig.add_trace(go.Scatter(
        x=x_values,
        y=y_values,
        mode='lines+markers+text',
        line=dict(color=colors[0] if colors else '#4285F4', width=3),
        marker=dict(color=colors[0] if colors else '#4285F4', size=8),
        text=text_labels,
        textposition='top center',
        textfont=dict(family="Arial", size=12, color='#000000'),
        hoverinfo='none'
    ))

title_text = texts.get('title')
subtitle_text = texts.get('subtitle')
full_title = ""
if title_text:
    full_title += f"<b>{title_text}</b>"
if subtitle_text:
    full_title += f"<br><sub>{subtitle_text}</sub>"

source_text = texts.get('source')
note_text = texts.get('note')
caption_text = ""
if source_text:
    caption_text += source_text
if note_text:
    caption_text += f"<br>{note_text}"

fig.update_layout(
    title=dict(
        text=full_title,
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        tickvals=x_values,
        tickformat='%Y'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=True,
        gridcolor='#E5E5E5',
        gridwidth=1,
        griddash='dash',
        range=[360000, 500000],
        dtick=20000,
        separatethousands=True,
        ticksuffix=' '
    ),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, b=100, t=50)
)

if caption_text:
    fig.add_annotation(
        text=caption_text,
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=1.0,
        y=-0.15,
        xanchor='right',
        yanchor='top',
        font=dict(size=10, color="#555555")
    )

output_filename_base = json_path.rsplit('.', 1)[0]
output_filename = f"{output_filename_base}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")