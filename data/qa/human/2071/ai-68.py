import sys
import json
import pathlib
import plotly.graph_objects as go

# --- 1. Load data from JSON file ---
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_config = json.load(f)

# --- 2. Extract data and texts from the loaded JSON ---
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

x_values = [item['x'] for item in chart_data]
y_values = [item['y'] for item in chart_data]

# --- 3. Create the Plotly figure ---
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    text=y_values,
    textposition='outside',
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    ),
    marker_color=colors[0] if colors else '#1f77b4',
    cliponaxis=False,
    hoverinfo='none'
))

# --- 4. Configure the layout ---
fig.update_layout(
    font=dict(
        family="Arial",
        size=12
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=50, b=100),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        showline=True,
        linecolor='black',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=True,
        gridcolor='#EAEAEA',
        gridwidth=1,
        showline=False,
        zeroline=False,
        range=[0, 5000],
        tickfont=dict(size=12)
    )
)

# --- 5. Add annotations for source/note texts ---
if texts.get("source_left"):
    fig.add_annotation(
        text=texts["source_left"],
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0,
        y=-0.15,
        xanchor='left',
        yanchor='top'
    )

if texts.get("source_right"):
    fig.add_annotation(
        text=texts["source_right"],
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=1,
        y=-0.15,
        xanchor='right',
        yanchor='top'
    )

# --- 6. Output the chart as a PNG file ---
output_filename = json_path.with_suffix(".png").name
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")