import sys
import json
import os
import plotly.graph_objects as go

# --- 1. Argument and File Handling ---
if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

if not os.path.exists(json_path):
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# --- 2. Data Loading ---
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_path}")
    sys.exit(1)

data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']
data_unit = texts.get('data_unit', '')

# --- 3. Data Preparation ---
# Reverse data for top-to-bottom display in Plotly
data.reverse()

categories = [item['category'] for item in data]
values = [item['value'] for item in data]
text_labels = [f"{v}{data_unit}" for v in values]

# --- 4. Chart Creation ---
fig = go.Figure()

# Add bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    text=text_labels,
    textposition='outside',
    marker=dict(color=colors[0]),
    cliponaxis=False,
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    )
))

# --- 5. Layout Configuration ---
fig.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(
        family="Arial",
        size=12,
        color='black'
    ),
    margin=dict(l=120, r=60, t=40, b=80),
    xaxis=dict(
        title=texts['x_axis_title'],
        title_font=dict(size=14),
        showgrid=True,
        gridcolor='#e0e0e0',
        gridwidth=1,
        zeroline=False,
        showline=False,
        ticksuffix=data_unit,
        tickformat=".1f",
        range=[0, max(values) * 1.15],
        side='bottom'
    ),
    yaxis=dict(
        showgrid=False,
        showline=False,
        showticklabels=True,
        categoryorder='array',
        categoryarray=categories
    ),
    showlegend=False,
    annotations=[
        dict(
            text=texts.get('source', ''),
            align='left',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=-0.15,
            xanchor='left',
            yanchor='top',
            font=dict(size=12)
        )
    ]
)

# --- 6. Output Generation ---
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)