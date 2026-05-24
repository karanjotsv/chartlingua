import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# --- Argument and File Handling ---
if len(sys.argv) != 2:
    print(f"Usage: python {Path(__file__).name} <json_file_path>")
    sys.exit(1)

json_filepath = Path(sys.argv[1])
if not json_filepath.is_file():
    print(f"Error: JSON file not found at '{json_filepath}'")
    sys.exit(1)

output_filename_base = json_filepath.stem
output_filename = f"{output_filename_base}.png"

# --- Data Loading ---
try:
    with open(json_filepath, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in '{json_filepath}'")
    sys.exit(1)

# --- Data Extraction ---
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# --- Chart Creation ---
fig = go.Figure()

# --- Add Bar Trace ---
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0] if colors else '#2e77d1',
    name=''
))

# --- Add Data Labels (as Annotations for precision) ---
# The original chart has black text with a white outline. This effect is not
# directly supported. We use bold black text as a readable approximation.
for cat, val in zip(categories, values):
    fig.add_annotation(
        x=cat,
        y=val / 2, # Place label in the vertical middle of the bar
        text=f"<b>{val}</b>",
        showarrow=False,
        font=dict(family="Arial", size=12, color="white"),
        xanchor='center',
        yanchor='middle'
    )

# --- Layout and Styling ---
fig.update_layout(
    font=dict(family="Arial"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=80, r=20, t=40, b=100),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 70],
        tickvals=[0, 10, 20, 30, 40, 50, 60, 70],
        showgrid=True,
        gridcolor='#e0e0e0',
        griddash='dash',
        zeroline=False,
        linecolor='black',
        linewidth=1
    ),
    xaxis=dict(
        showgrid=False,
        tickfont=dict(size=12),
        linecolor='black',
        linewidth=1
    ),
    showlegend=False,
    annotations=[
        dict(
            text=f"ⓘ {texts.get('note', '')}" if texts.get('note') else "",
            xref="paper", yref="paper",
            x=0, y=-0.25,
            showarrow=False,
            xanchor='left',
            yanchor='bottom',
            font=dict(size=12, color='#0073e5')
        ),
        dict(
            text=texts.get('source', ''),
            xref="paper", yref="paper",
            x=1, y=-0.25,
            showarrow=False,
            xanchor='right',
            yanchor='bottom',
            font=dict(size=12, color='#666666')
        )
    ]
)

# --- Output ---
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")