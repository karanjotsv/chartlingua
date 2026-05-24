import sys
import json
import plotly.graph_objects as go
import pathlib

# --- 1. Load Data from JSON ---
# The script expects the JSON file path as the sole command-line argument.
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = pathlib.Path(sys.argv[1])
if not json_file_path.is_file():
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data, texts, and colors from the loaded JSON
chart_data = chart_info.get("chart_data", [])
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", [])

# --- 2. Create the Chart Figure ---
fig = go.Figure()

# Add the bar trace from the chart data
if chart_data:
    series = chart_data[0]
    fig.add_trace(go.Bar(
        y=series.get("categories", []),
        x=series.get("values", []),
        orientation='h',
        marker=dict(color=colors[0] if colors else '#2e7dcb'),
        text=series.get("values", []),
        textposition='outside',
        texttemplate='%{text}',
        cliponaxis=False,
        textfont=dict(
            family="Arial",
            size=12,
            color='black'
        )
    ))

# --- 3. Configure Layout ---
fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    title_text=None,
    xaxis=dict(
        title=texts.get("x_axis_title"),
        showgrid=True,
        gridcolor='#e0e0e0',
        gridwidth=1,
        griddash='dot',
        zeroline=False,
        range=[0, 1300], # Set range to give space for outside text labels
        tickvals=[i * 100 for i in range(13)], # Set ticks every 100
        ticktext=[f"{i*100:,}".replace(",", " ") for i in range(13)] # Format ticks with space as separator
    ),
    yaxis=dict(
        showgrid=False,
        autorange="reversed" # Ensures categories are plotted top-to-bottom as per JSON order
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=100, r=80, t=50, b=100),
    annotations=[
        dict(
            text=texts.get("source"),
            align='right',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.99,
            y=-0.15,
            xanchor='right',
            yanchor='top'
        )
    ]
)

# --- 4. Output the Image ---
output_filename = json_file_path.with_suffix('.png').name
fig.write_image(output_filename, scale=2)

print(f"Chart saved as '{output_filename}'")