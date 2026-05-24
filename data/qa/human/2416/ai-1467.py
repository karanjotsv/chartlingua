import sys
import json
import plotly.graph_objects as go
from pathlib import Path

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <path_to_json_file>", file=sys.stderr)
    sys.exit(1)

json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}", file=sys.stderr)
    sys.exit(1)

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except Exception as e:
    print(f"Error reading or parsing JSON file: {e}", file=sys.stderr)
    sys.exit(1)

chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

categories = [d['category'] for d in chart_data]
values = [d['value'] for d in chart_data]

# Format text labels for bars with a space as the thousands separator
text_labels = [f"{v:,}".replace(",", " ") for v in values]

# Reverse the lists to display in the same top-to-bottom order as the image
categories.reverse()
values.reverse()
text_labels.reverse()

fig = go.Figure()

fig.add_trace(go.Bar(
    y=categories,
    x=values,
    text=text_labels,
    orientation='h',
    marker_color=colors[0] if colors else '#2672D1',
    textposition='outside',
    cliponaxis=False,
    textfont=dict(family="Arial", size=12)
))

title_text_parts = []
if texts.get('title'):
    title_text_parts.append(f"<b>{texts['title']}</b>")
if texts.get('subtitle'):
    title_text_parts.append(texts['subtitle'])
final_title = "<br>".join(title_text_parts)

fig.update_layout(
    font=dict(family="Arial", size=12, color='black'),
    title=dict(
        text=final_title if final_title else None,
        x=0.05, xanchor='left', y=0.95, yanchor='top'
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis=dict(
        title=dict(text=texts.get('x_axis_title'), standoff=10),
        showgrid=True,
        gridcolor='#E0E0E0',
        griddash='dot',
        zeroline=False,
        showline=False,
        ticks='outside',
        tickformat=',d',
        range=[0, max(values) * 1.1]
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        showgrid=False,
        zeroline=False,
        showline=True,
        linecolor='black',
        linewidth=1,
        ticks='outside'
    ),
    showlegend=False,
    margin=dict(l=100, r=80, t=40, b=80)
)

if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        xref="paper", yref="paper",
        x=0.99, y=-0.14,
        showarrow=False,
        xanchor='right',
        yanchor='top',
        align='right',
        font=dict(family="Arial", size=12, color='grey')
    )

output_filename_base = json_path.stem
output_png_path = f"{output_filename_base}.png"
fig.write_image(output_png_path, scale=2)

print(f"Chart saved to {output_png_path}")