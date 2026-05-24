import sys
import json
import plotly.graph_objects as go
import os

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data for plotting
chart_data = chart_info.get("chart_data", [])
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", [])

x_values = [d['x'] for d in chart_data]
y_values = [d['y'] for d in chart_data]
text_values = [f"<b>{d['y']:,}</b>" for d in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    text=text_values,
    textposition='outside',
    marker_color=colors,
    cliponaxis=False,
    textfont=dict(
        family='Arial',
        size=16,
        color='black'
    )
))

# Update layout
fig.update_layout(
    title_text=texts.get('title'),
    title_x=0.5,
    title_font=dict(
        family='Arial',
        size=24
    ),
    xaxis=dict(
        categoryorder='array',
        categoryarray=x_values,
        showline=True,
        linecolor='black',
        ticks='',
        tickfont=dict(
            family='Arial',
            size=14
        )
    ),
    yaxis=dict(
        range=[0, 6000],
        dtick=1000,
        showgrid=True,
        gridcolor='lightgray',
        showline=True,
        linecolor='black',
        ticks='outside',
        tickfont=dict(
            family='Arial',
            size=14
        )
    ),
    font=dict(
        family="Arial"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=60, r=40, t=100, b=120),
    annotations=[
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.5,
            y=-0.28,
            xanchor='center',
            yanchor='top',
            font=dict(
                family='Arial',
                size=18
            )
        )
    ]
)

# Determine output filename from input JSON path
filename_base = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{filename_base}.png"

# Write image to file
fig.write_image(output_filename, scale=2, width=650, height=550)

print(f"Chart saved to {output_filename}")