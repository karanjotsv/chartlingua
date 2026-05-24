import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# This script requires Plotly and Kaleido to be installed.
# You can install them using: pip install plotly kaleido

if len(sys.argv) != 2:
    print(f"Usage: python {Path(__file__).name} <path_to_json_file>")
    sys.exit(1)

json_file_path = Path(sys.argv[1])

if not json_file_path.is_file():
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)

with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

labels = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(
        colors=colors,
        line=dict(color='black', width=1)
    ),
    texttemplate='%{value}%',
    textposition='outside',
    sort=False,
    direction='clockwise'
))

title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

fig.update_layout(
    title_text=title_text,
    title_x=0.5,
    title_font_family="Arial",
    title_font_size=16,
    font_family="Arial",
    font_size=12,
    showlegend=True,
    legend=dict(
        x=0.8,
        y=0.7,
        xanchor='left',
        yanchor='top',
        bgcolor='rgba(255,255,255,0.5)',
        bordercolor='Black',
        borderwidth=1
    ),
    margin=dict(t=100, b=50, l=50, r=50),
    plot_bgcolor='white',
    paper_bgcolor='white'
)

if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        align='left',
        showarrow=False,
        xref='paper', yref='paper',
        x=0, y=-0.1,
        font=dict(family="Arial", size=10, color="grey")
    )

output_filename = json_file_path.stem + ".png"

try:
    fig.write_image(output_filename, scale=2, width=600, height=400)
    print(f"Chart saved as {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    print("Please ensure you have 'kaleido' installed (`pip install kaleido`) for static image export.")
    sys.exit(1)