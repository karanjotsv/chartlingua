import sys
import json
import pathlib
import plotly.graph_objects as go

# --- 1. Load data from JSON file ---
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# --- 2. Extract and prepare data ---
chart_data = chart_info.get("chart_data", [])
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", [])

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Reverse data to display in the same top-to-bottom order as the image
categories.reverse()
values.reverse()
colors.reverse()

# --- 3. Create the chart ---
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors),
    text=values,
    textposition='outside',
    textfont=dict(family="Arial", size=12),
    cliponaxis=False  # Prevents text labels from being clipped
))

# --- 4. Configure layout and styling ---
annotations = []

# Add source text at the bottom right
if texts.get("source"):
    annotations.append(dict(
        xref="paper", yref="paper",
        x=0.99, y=-0.15,
        xanchor="right", yanchor="top",
        text=texts["source"],
        showarrow=False,
        font=dict(family="Arial", size=12, color="#666666")
    ))

fig.update_layout(
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title=texts.get("x_axis_title"),
        showgrid=True,
        gridcolor='#E0E0E0',
        gridwidth=1,
        griddash='dot',
        zeroline=False,
        showline=False,
        ticks='',
        tickmode='linear',
        tick0=0,
        dtick=10
    ),
    yaxis=dict(
        title=texts.get("y_axis_title"),
        showgrid=False,
        zeroline=False,
        showline=False,
        ticks=''
    ),
    margin=dict(l=150, r=40, t=30, b=80),
    annotations=annotations,
    xaxis_range=[0, max(values) * 1.08] # Add padding for outside text
)

# --- 5. Output the chart as a PNG file ---
output_path = json_path.with_suffix(".png")
fig.write_image(output_path, scale=2)

print(f"Chart saved to {output_path}")