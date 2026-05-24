import sys
import json
import pathlib
import plotly.graph_objects as go

# --- 1. Load data from JSON file specified by command-line argument ---
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_config = json.load(f)

# --- 2. Extract data and text from the loaded JSON ---
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# --- 3. Create the Plotly figure ---
fig = go.Figure()

# Add the horizontal bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker_color=colors,
    text=[f'{v:,}'.replace(',', ' ') for v in values],
    textposition='outside',
    textfont=dict(family="Arial", size=12, color='black'),
    cliponaxis=False  # Prevents text from being clipped at the chart's edge
))

# --- 4. Configure the layout to match the original image ---
# Build title string
title_text = ""
if texts.get("title"):
    title_text += texts["title"]
if texts.get("subtitle"):
    title_text += f"<br><sup>{texts['subtitle']}</sup>"

fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#e9e9e9',
        gridwidth=1,
        zeroline=False,
        tickformat=" ", # Use space as thousands separator
        separatethousands=True
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        autorange='reversed',  # To display categories from top to bottom
        showgrid=False,
        zeroline=False
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=120, r=80, t=50, b=80),  # Adjust margins for labels and source text
    annotations=[
        dict(
            text=texts.get('source', ''),
            showarrow=False,
            xref='paper', yref='paper',
            x=1.0, y=-0.15,
            xanchor='right', yanchor='top',
            font=dict(size=10)
        )
    ]
)

# --- 5. Save the figure to a PNG file ---
output_filename = json_path.stem + ".png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")