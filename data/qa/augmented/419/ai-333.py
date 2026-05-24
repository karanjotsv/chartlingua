import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# --- Argument Handling ---
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = Path(sys.argv[1])
if not json_file_path.is_file():
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

# --- Data Loading ---
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_config = json.load(f)

chart_data = chart_config['chart_data']
texts = chart_config['texts']
colors = chart_config['colors']

# --- Data Processing ---
x_values = [d['x'] for d in chart_data]
y_values = [d['y'] for d in chart_data]

# Format text labels to match the original chart (space as thousands separator)
bar_texts = []
for val in y_values:
    if val == int(val):
        bar_texts.append(f"{int(val):,}".replace(",", " "))
    else:
        bar_texts.append(f"{val:,.1f}".replace(",", " "))

# --- Chart Creation ---
fig = go.Figure()

# --- Add Trace ---
fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    text=bar_texts,
    textposition='outside',
    marker_color=colors[0],
    cliponaxis=False,
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    )
))

# --- Layout Configuration ---
fig.update_layout(
    plot_bgcolor='white',
    showlegend=False,
    font=dict(
        family="Arial",
        size=12,
        color='black'
    ),
    margin=dict(l=80, r=40, t=40, b=100),
    xaxis=dict(
        title_text=texts['x_axis_title'],
        tickmode='array',
        tickvals=x_values,
        tickformat='%Y',
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black'
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        range=[0, 7000],
        tickvals=[i * 1000 for i in range(8)],
        ticktext=[f"{i * 1000}" for i in range(8)],
        gridcolor='#EAEAEA',
        zeroline=False
    ),
    annotations=[
        dict(
            xref='paper', yref='paper',
            x=1.0, y=-0.2,
            xanchor='right', yanchor='top',
            text=texts['source'],
            showarrow=False,
            font=dict(size=12, color='#666666')
        )
    ]
)

# --- Output ---
output_filename = json_file_path.with_suffix('.png')
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")