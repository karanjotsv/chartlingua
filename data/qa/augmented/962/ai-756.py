import sys
import json
import pathlib
import plotly.graph_objects as go

# --- 1. Load data from JSON file provided via command-line ---
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# --- 2. Extract data and text from the loaded JSON ---
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Prepare data for Plotly
x_values = [item['x'] for item in chart_data]
y_values = [item['y'] for item in chart_data]
bar_texts = [f"{item['y']:,}".replace(",", " ") for item in chart_data]

# --- 3. Create the Plotly figure ---
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    text=bar_texts,
    textposition='outside',
    marker_color=colors[0],
    cliponaxis=False,  # Allow text to be drawn outside the axis range
    textfont=dict(
        family="Arial",
        size=12
    )
))

# --- 4. Configure layout, axes, and annotations ---
fig.update_layout(
    xaxis=dict(
        title_text=texts['x_axis_title'],
        tickmode='array',
        tickvals=x_values,
        ticktext=[str(x) for x in x_values],
        showgrid=True,
        gridcolor='#f0f0f0', # Faint vertical grid lines
        linecolor='black',
        zeroline=False
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        range=[0, 60000],
        tickmode='array',
        tickvals=[0, 10000, 20000, 30000, 40000, 50000, 60000],
        ticktext=[f"{v:,}".replace(",", " ") for v in [0, 10000, 20000, 30000, 40000, 50000, 60000]],
        showgrid=True,
        gridcolor='#e0e0e0', # Horizontal grid lines
        zeroline=False
    ),
    plot_bgcolor='white',
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    margin=dict(l=80, r=20, t=50, b=80),
    showlegend=False,
    annotations=[
        dict(
            text=texts['source'],
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.15,
            xanchor='right',
            yanchor='top',
            font=dict(
                family="Arial",
                size=12,
                color="#666666"
            )
        )
    ]
)

# --- 5. Output the chart as a PNG file ---
output_filename = json_path.with_suffix('.png')
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")