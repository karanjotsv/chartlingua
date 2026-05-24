import sys
import json
import pathlib
import plotly.graph_objects as go

# --- 1. Load Data from JSON ---
# The script requires the path to the JSON file as a command-line argument.
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error reading or parsing JSON file: {e}")
    sys.exit(1)

# Extract data, texts, and colors from the loaded JSON
chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
series_colors = config.get('colors', [])

# Prepare data for plotting
categories = [d['category'] for d in chart_data]
series_1_values = [d['series_1_value'] for d in chart_data]
series_2_values = [d['series_2_value'] for d in chart_data]

# --- 2. Define Chart Styling ---
# These stylistic choices are based on the visual analysis of the source image.
# They are kept separate from the JSON data, which holds the core chart content.
font_family = "Arial"
plot_bg_color = "#F0F8FF"
band_color = "#E6F2FA"
paper_bg_color = "#FFFFFF"
text_color = "#000000"
grid_color = "#DCDCDC"

# --- 3. Create Figure and Traces ---
fig = go.Figure()

# Add Trace 1: Total Testosterone (linked to yaxis1)
fig.add_trace(go.Scatter(
    x=categories,
    y=series_1_values,
    name=texts.get('series_1_label'),
    mode='lines+markers',
    line=dict(color=series_colors[0], width=3),
    marker=dict(color=series_colors[0], size=8),
    yaxis='y1'
))

# Add Trace 2: Free Testosterone (linked to yaxis2)
fig.add_trace(go.Scatter(
    x=categories,
    y=series_2_values,
    name=texts.get('series_2_label'),
    mode='lines+markers',
    line=dict(color=series_colors[1], width=3),
    marker=dict(color=series_colors[1], size=8),
    yaxis='y2'
))

# --- 4. Configure Layout ---
fig.update_layout(
    # Title
    title=dict(
        text=texts.get('title'),
        x=0.5,
        xanchor='center',
        font=dict(size=22, color=text_color)
    ),
    # General styling
    font=dict(family=font_family, color=text_color),
    plot_bgcolor=plot_bg_color,
    paper_bgcolor=paper_bg_color,
    # Axes configuration
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=False,
        zeroline=False,
        ticks='outside',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title=texts.get('y_axis_1_title'),
        side='left',
        range=[250, 750],
        tickvals=[250, 375, 500, 625, 750],
        showgrid=True,
        gridcolor=grid_color,
        zeroline=False,
        tickfont=dict(size=12)
    ),
    yaxis2=dict(
        title=texts.get('y_axis_2_title'),
        overlaying='y',
        side='right',
        range=[4, 14],
        tickvals=[4, 6.5, 9, 11.5, 14],
        showgrid=False,
        zeroline=False,
        tickfont=dict(size=12)
    ),
    # Legend
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="left",
        x=0.01,
        bgcolor='rgba(0,0,0,0)' # Transparent background
    ),
    # Background bands using shapes
    shapes=[
        dict(
            type="rect", xref="paper", yref="y1",
            x0=0, y0=500, x1=1, y1=625,
            fillcolor=band_color, layer="below", line_width=0
        ),
        dict(
            type="rect", xref="paper", yref="y1",
            x0=0, y0=250, x1=1, y1=375,
            fillcolor=band_color, layer="below", line_width=0
        )
    ],
    # Margins to prevent clipping
    margin=dict(l=80, r=80, t=100, b=120),
    # Source text annotation
    annotations=[
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.5,
            y=-0.25,
            xanchor='center',
            yanchor='top',
            font=dict(size=10, color='#666666')
        )
    ]
)
# Move legend from above plot to below x-axis as in the original image
fig.update_layout(
    legend=dict(
        orientation="h", yanchor="top", y=-0.3, xanchor="left", x=0
    )
)

# --- 5. Save Output ---
filename_base = pathlib.Path(json_path).stem
output_filename = f"{filename_base}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")