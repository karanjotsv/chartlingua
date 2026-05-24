import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# --- Argument and File Handling ---
if len(sys.argv) != 2:
    print(f"Usage: python {Path(__file__).name} <json_file_path>")
    sys.exit(1)

json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

output_path = json_path.with_suffix(".png")

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# --- Data Extraction ---
chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']
y_axis_format = config.get('y_axis_format', {})

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]
bar_texts = [item.get('text', '') for item in chart_data]

# --- Chart Creation ---
fig = go.Figure()

# Add Bar Trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=bar_texts,
    textposition='outside',
    marker_color=colors[0],
    textfont=dict(family="Arial", size=12, color='black'),
    cliponaxis=False  # Prevents text labels from being clipped at the top
))

# --- Layout Configuration ---
fig.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12, color='black'),
    showlegend=False,
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        zeroline=False,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=True,
        gridcolor='#e0e0e0',
        zeroline=False,
        range=[0, 7000],
        tickvals=y_axis_format.get('tickvals'),
        ticktext=y_axis_format.get('ticktext'),
        tickfont=dict(size=12)
    ),
    margin=dict(l=90, r=40, t=50, b=100)
)

# --- Add Annotations ---
# Add Source
if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        xref="paper", yref="paper",
        x=0.99, y=-0.18,
        showarrow=False,
        xanchor='right',
        yanchor='top',
        align='right',
        font=dict(family="Arial", size=10, color="#555555")
    )

# --- Output ---
fig.write_image(output_path, scale=2)
print(f"Chart saved to {output_path}")