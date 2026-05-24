import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# --- 1. Argument and File Handling ---
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

output_base_name = Path(json_path).stem

# --- 2. Data Extraction ---
chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

# --- 3. Chart Creation ---
fig = go.Figure()

# Add bar trace
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]
data_labels = [f"{item['value']}%" for item in chart_data]

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0] if colors else None,
    text=data_labels,
    textposition='outside',
    cliponaxis=False,
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    )
))

# --- 4. Layout and Styling ---
fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    title_text=texts.get('title'),
    yaxis_title_text=texts.get('y_axis_title'),
    showlegend=False,
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=60, r=20, t=40, b=80),
    xaxis=dict(
        showline=True,
        linewidth=1,
        linecolor='black',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        range=[0, 25],
        dtick=5,
        ticksuffix='%',
        showgrid=True,
        gridcolor='#e5e5e5',
        zeroline=False,
        title_standoff=15
    )
)

# Add faint vertical lines as in the original image
fig.add_vline(x=0.5, line_width=1, line_color='#f0f0f0', layer='below')
fig.add_vline(x=1.5, line_width=1, line_color='#f0f0f0', layer='below')


# Add source annotation
if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        xref="paper", yref="paper",
        x=1.0, y=-0.2,
        xanchor='right', yanchor='top',
        showarrow=False,
        font=dict(
            family="Arial",
            size=10,
            color="grey"
        )
    )

# --- 5. Output ---
output_filename = f"{output_base_name}.png"
fig.write_image(output_filename, scale=2, width=800, height=600)
print(f"Chart saved to {output_filename}")