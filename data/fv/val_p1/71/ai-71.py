import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

# Get file path from argument
json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Load data from JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data for plotting
chart_data = chart_info.get("chart_data", [])
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", {})

# Initialize figure
fig = go.Figure()

# Add traces from chart_data
series_colors = colors.get("series_colors", [])
for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        x=series.get("x"),
        y=series.get("y"),
        name=series.get("name"),
        marker=dict(
            color=series_colors[i] if i < len(series_colors) else None,
            line=dict(color='black', width=1)
        ),
        text=series.get("y"),
        textposition='outside',
        textfont=dict(family="Arial", size=14, color='black', weight='bold'),
        cliponaxis=False 
    ))

# Update layout
fig.update_layout(
    title=dict(
        text=texts.get("title"),
        x=0.5,
        xanchor='center',
        font=dict(family="Arial", size=20, weight='bold')
    ),
    xaxis=dict(
        title_text=texts.get("x_axis_title"),
        showline=True,
        linewidth=1,
        linecolor='black',
        ticks='outside'
    ),
    yaxis=dict(
        title_text=texts.get("y_axis_title"),
        range=[0, 20],
        dtick=2,
        showgrid=True,
        gridwidth=1,
        gridcolor='lightgray',
        showline=True,
        linewidth=1,
        linecolor='black',
        ticks='outside'
    ),
    legend=dict(
        x=0.02,
        y=0.98,
        xanchor='left',
        yanchor='top',
        bordercolor='black',
        borderwidth=1
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial"),
    margin=dict(t=80, b=80, l=60, r=40)
)

# Generate output PNG filename from JSON filename
output_filename = json_path.with_suffix('.png')

# Save the figure to a file
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)