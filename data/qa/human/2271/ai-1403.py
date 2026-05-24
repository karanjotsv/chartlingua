import sys
import json
import os
import plotly.graph_objects as go

# --- 1. Load data from JSON file ---
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = chart_config['chart_data']
texts = chart_config['texts']
colors = chart_config['colors']

# --- 2. Create the chart figure ---
fig = go.Figure()

# --- 3. Add data series (traces) to the figure ---
for i, series in enumerate(chart_data['series']):
    fig.add_trace(go.Bar(
        x=chart_data['categories'],
        y=series['data'],
        name=series['name'],
        marker_color=colors[i],
        text=[f"{val}%" for val in series['data']],
        textposition='outside',
        textfont=dict(family="Arial", size=12, color='black'),
        cliponaxis=False
    ))

# --- 4. Update layout, styling, and annotations ---
fig.update_layout(
    barmode='group',
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12, color='black'),
    title=dict(
        text=texts['title']['text'] if texts.get('title') and texts['title'].get('text') else None
    ),
    xaxis=dict(
        title_text=texts['x_axis_title'],
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        range=[0, 60],
        ticksuffix='%',
        showgrid=True,
        gridcolor='#e0e0e0',
        gridwidth=1,
        zeroline=False
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.3,  # Position legend below x-axis
        xanchor="center",
        x=0.5
    ),
    margin=dict(l=80, r=40, t=40, b=150), # Increased bottom margin for legend and source
    annotations=[
        dict(
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.4,
            xanchor='right',
            yanchor='top',
            text=texts['source'],
            showarrow=False,
            font=dict(family="Arial", size=12)
        )
    ]
)

# Adjust bar text position for better visibility
fig.update_traces(textangle=0, textfont_size=12)

# --- 5. Output the chart as a PNG file ---
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_directory = os.path.dirname(json_path)
output_filename = os.path.join(output_directory, f"{base_filename}.png")

try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart successfully generated and saved to {output_filename}")
except Exception as e:
    print(f"Error writing image file: {e}")
    sys.exit(1)