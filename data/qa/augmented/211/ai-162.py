import sys
import json
import os
import plotly.graph_objects as go

# --- 1. Argument Parsing and File Loading ---
if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# --- 2. Data Extraction ---
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

categories = [d['category'] for d in chart_data]
values = [d['value'] for d in chart_data]

# --- 3. Chart Creation ---
fig = go.Figure()

fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors, line=dict(width=0)),
    text=[f"{v}%" for v in values],
    textposition='outside',
    textfont=dict(family="Arial", size=12, color='#333333'),
    cliponaxis=False
))

# --- 4. Layout Configuration ---
fig.update_layout(
    font=dict(family="Arial", size=12, color='#333333'),
    margin=dict(l=160, r=50, t=30, b=80),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title=texts['x_axis_title'],
        title_standoff=15,
        showgrid=True,
        gridcolor='#EAEAEA',
        griddash='dot',
        zeroline=False,
        showline=False,
        ticksuffix='%',
        range=[0, max(values) * 1.18],
        tickfont=dict(size=11),
        title_font=dict(size=12)
    ),
    yaxis=dict(
        autorange="reversed",
        showline=False,
        ticks='',
        tickfont=dict(size=12)
    ),
    annotations=[
        dict(
            showarrow=False,
            text=texts['source'],
            xref='paper',
            yref='paper',
            x=1,
            y=-0.08,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(size=10, color='#666666')
        )
    ]
)

# --- 5. Output ---
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2, width=750, height=950)
print(f"Chart saved as {output_filename}")