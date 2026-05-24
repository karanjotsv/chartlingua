import sys
import json
from pathlib import Path
import plotly.graph_objects as go

# --- 1. Load Data from JSON ---
# The script expects the path to the JSON file as the first command-line argument.
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <path_to_json_file>")
    sys.exit(1)

json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data and text from the loaded JSON
chart_data = chart_info.get("chart_data", [])
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", [])
output_filename_base = json_path.stem

# --- 2. Prepare Data for Plotting ---
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# --- 3. Create the Chart ---
fig = go.Figure()

# Add the horizontal bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0]),
    text=values,
    texttemplate='%{text:.1f}',
    textposition='outside',
    cliponaxis=False  # Prevents text from being clipped at the plot edge
))

# --- 4. Configure Layout and Styling ---
fig.update_layout(
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    # Set generous margins to prevent labels from being cut off
    margin=dict(l=150, r=60, t=40, b=80),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        title_standoff=15,
        showticklabels=False,  # Hide tick labels
        showline=False,        # Hide axis line
        showgrid=False,        # Hide vertical grid lines
        zeroline=False,
        # Set range to give space for text labels outside the bars
        range=[0, max(values) * 1.08]
    ),
    yaxis=dict(
        # 'reversed' ensures the first item in the data appears at the top
        autorange="reversed",
        showgrid=True,
        gridcolor='#e9e9e9',
        gridwidth=1,
        zeroline=False,
        showline=False
    ),
    # Add source text as an annotation at the bottom right
    annotations=[
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.1, # Position below the plot area
            xanchor='right',
            yanchor='top',
            font=dict(size=11, color='#888888')
        )
    ]
)

# --- 5. Output the Chart ---
output_image_path = f"{output_filename_base}.png"
fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")