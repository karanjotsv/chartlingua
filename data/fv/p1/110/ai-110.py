import sys
import json
import plotly.graph_objects as go

# --- Argument Parsing and File Loading ---
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# --- Data Extraction from JSON ---
chart_data = chart_info['chart_data']
colors = chart_info['colors']

# --- Data Preparation for Plotly ---
labels = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]
text_labels = [f"{item['category']}, {item['value']}, {item['percentage']}%" for item in chart_data]

# --- Chart Creation ---
fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    text=text_labels,
    textinfo='none',
    hoverinfo='label+percent',
    marker=dict(
        colors=colors,
        line=dict(color='#000000', width=1)
    ),
    sort=False,
    direction='clockwise'
))

# --- Layout and Styling ---
fig.update_traces(
    textposition='outside',
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    )
)

fig.update_layout(
    showlegend=False,
    font=dict(
        family="Arial",
        size=12,
        color='black'
    ),
    width=750,
    height=750,
    margin=dict(l=80, r=80, t=80, b=80),
    paper_bgcolor='white',
    plot_bgcolor='white',
    shapes=[
        dict(
            type='rect',
            xref='paper',
            yref='paper',
            x0=0,
            y0=0,
            x1=1,
            y1=1,
            line=dict(
                color='black',
                width=1
            )
        )
    ]
)

# --- Output ---
# Derive the output filename from the input JSON path's base name
base_name_with_ext = json_path.split('/')[-1].split('\\')[-1]
base_filename = base_name_with_ext.rsplit('.', 1)[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")