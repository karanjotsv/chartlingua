import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# --- 1. Argument and File Handling ---
if len(sys.argv) != 2:
    print(f"Usage: python {Path(__file__).name} <path_to_json_file>")
    sys.exit(1)

json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

output_filename_base = json_path.stem

# --- 2. Data Loading ---
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except (json.JSONDecodeError, IOError) as e:
    print(f"Error reading or parsing JSON file: {e}")
    sys.exit(1)

# Extract data, texts, and colors from the JSON structure
data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', {})

# --- 3. Data Preparation ---
# Plotly's horizontal bars are plotted from bottom to top, so data must be reversed for visual match
categories = [d.get('category', '') for d in data]
values = [d.get('value', 0) for d in data]
categories.reverse()
values.reverse()

# Assign colors to bars, applying a secondary color for the 'MEDIAN' category
bar_colors = [colors.get('secondary') if cat == 'MEDIAN' else colors.get('primary') for cat in categories]

# --- 4. Chart Creation ---
fig = go.Figure()

# Add the main bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker_color=bar_colors,
    text=values,
    textposition='inside',
    texttemplate='%{text}',
    textfont=dict(color='white', size=14, family="Arial"),
    insidetextanchor='end',
    hoverinfo='none'
))

# --- 5. Layout and Styling ---
# Combine title and subtitle using HTML for rich formatting
title_text = f"{texts.get('title', '')}<br><span style='font-size:16px; color:#555555;'>{texts.get('subtitle', '')}</span>"

fig.update_layout(
    # Set main font
    font=dict(family="Arial"),
    # Configure title and subtitle
    title=dict(
        text=title_text,
        x=0.01,
        y=0.98,
        xanchor='left',
        yanchor='top',
        font=dict(size=24, color='black')
    ),
    # Configure axes
    xaxis=dict(
        showticklabels=False,
        showgrid=False,
        zeroline=False,
        showline=False,
        range=[0, max(values) * 1.08]  # Add padding for text inside bars
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=False,
        tickfont=dict(size=14)
    ),
    # Set background colors
    paper_bgcolor='white',
    plot_bgcolor='white',
    showlegend=False,
    # Define margins to prevent text clipping
    margin=dict(l=120, r=20, t=160, b=120),
    # Add source text as a layout annotation for precise positioning
    annotations=[
        dict(
            text=texts.get('source', ''),
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0,
            y=-0.15,
            xanchor='left',
            yanchor='top',
            align='left',
            font=dict(size=12, color='#555555')
        )
    ],
    # Add decorative horizontal lines as shapes
    shapes=[
        go.layout.Shape(
            type="line", xref="paper", yref="paper",
            x0=0, y0=1.04, x1=1, y1=1.04,
            line=dict(color="black", width=2)
        ),
        go.layout.Shape(
            type="line", xref="paper", yref="paper",
            x0=0, y0=-0.08, x1=1, y1=-0.08,
            line=dict(color="black", width=1)
        )
    ]
)

# --- 6. Output ---
output_path = f"{output_filename_base}.png"
fig.write_image(output_path, scale=2)
print(f"Chart saved to {output_path}")