import sys
import json
import pathlib
import plotly.graph_objects as go

# --- Argument Handling ---
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# --- Data Loading ---
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except (json.JSONDecodeError, IOError) as e:
    print(f"Error reading or parsing JSON file: {e}")
    sys.exit(1)

# --- Data Extraction ---
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# --- Chart Creation ---
fig = go.Figure()

# Add Bar Trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0] if colors else '#1f77b4'),
    text=values,
    textposition='outside',
    texttemplate='%{text}',
    cliponaxis=False,
    outsidetextfont=dict(family="Arial", size=12, color='black')
))

# --- Layout Configuration ---
annotations = []
if texts.get('note'):
    annotations.append(
        dict(
            xref='paper', yref='paper',
            x=0, y=-0.12,
            xanchor='left', yanchor='top',
            text=texts['note'],
            showarrow=False,
            font=dict(family="Arial", size=12, color='#666666')
        )
    )

if texts.get('source'):
    annotations.append(
        dict(
            xref='paper', yref='paper',
            x=1, y=-0.12,
            xanchor='right', yanchor='top',
            text=texts['source'],
            showarrow=False,
            font=dict(family="Arial", size=12, color='#666666')
        )
    )

fig.update_layout(
    font=dict(family="Arial", size=12, color='black'),
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#e9e9e9',
        zeroline=False,
        showline=False,
        ticks='outside',
        tickcolor='#d3d3d3',
        range=[0, max(values) * 1.2] # Dynamic range with padding
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        showgrid=False,
        zeroline=False,
        showline=False,
        ticks='',
    ),
    margin=dict(l=130, r=40, b=80, t=40),
    showlegend=False,
    annotations=annotations
)

# --- Image Export ---
output_path = json_path.with_suffix('.png')
fig.write_image(output_path, scale=2)
print(f"Chart saved to {output_path}")