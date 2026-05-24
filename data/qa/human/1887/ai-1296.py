import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# --- 1. Load data from JSON file provided as a command-line argument ---
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_file_path = Path(sys.argv[1])
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# --- 2. Extract data, texts, and colors from the loaded JSON ---
chart_data = chart_info.get("chart_data", [])
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", {})

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# --- 3. Create the Plotly figure ---
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=values,
    textposition='outside',
    cliponaxis=False,
    marker_color=colors.get('bar', '#1f77b4'),
    texttemplate='%{text}',
    hoverinfo='none'
))

# --- 4. Configure the layout to match the original image ---
fig.update_layout(
    font_family="Arial",
    plot_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showline=True,
        linewidth=1,
        linecolor='black',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 5000],
        tickvals=[0, 1000, 2000, 3000, 4000, 5000],
        tickformat=" ", # Use a space as a thousands separator
        showgrid=True,
        gridcolor='#e0e0e0',
        zeroline=False,
        tickfont=dict(size=12)
    ),
    margin=dict(l=80, r=40, b=100, t=50),
    annotations=[
        # Left source/note
        dict(
            showarrow=False,
            xref="paper", yref="paper",
            x=0, y=-0.2,
            xanchor='left', yanchor='bottom',
            text=texts.get('source_left', ''),
            font=dict(
                family="Arial",
                size=12,
                color=colors.get('source_left_text', '#000000')
            )
        ),
        # Right source/note
        dict(
            showarrow=False,
            xref="paper", yref="paper",
            x=1, y=-0.2,
            xanchor='right', yanchor='bottom',
            text=texts.get('source_right', ''),
            font=dict(
                family="Arial",
                size=12,
                color=colors.get('source_right_text', '#808080')
            )
        )
    ]
)

# Update the bar text font
fig.update_traces(textfont_size=12, textfont_color='black')


# --- 5. Generate and save the output image ---
output_filename = f"{json_file_path.stem}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")