import sys
import json
import plotly.graph_objects as go
import os

# --- 1. Load data from JSON file specified by command-line argument ---
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

# --- 2. Extract data and text from the loaded JSON ---
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Prepare data for plotting
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Reverse data for Plotly's horizontal bar chart rendering (plots from bottom up)
categories.reverse()
values.reverse()

# Format bar labels with spaces as thousand separators
bar_texts = [f"{v:,}".replace(",", " ") for v in values]

# --- 3. Create the Plotly figure ---
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0]),
    text=bar_texts,
    textposition='outside',
    cliponaxis=False,
    insidetextanchor='start',
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    )
))

# --- 4. Configure the layout ---
fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    plot_bgcolor='white',
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#e0e0e0',
        gridwidth=1,
        griddash='dot',
        zeroline=False,
        tickformat=" ," # Use space as thousands separator
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        showgrid=False,
        categoryorder='array',
        categoryarray=categories # Explicitly set order
    ),
    showlegend=False,
    margin=dict(l=120, r=60, t=30, b=80),
    annotations=[
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref="paper",
            yref="paper",
            x=1.0,
            y=-0.15,
            xanchor='right',
            yanchor='top',
            align='right'
        )
    ]
)

# --- 5. Output the chart as a PNG image ---
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_image_path = f"{base_filename}.png"

fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")