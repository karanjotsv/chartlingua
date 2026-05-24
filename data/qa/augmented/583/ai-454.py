import sys
import os
import json
import plotly.graph_objects as go

# --- 1. Load data from JSON file provided as a command-line argument ---
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_config = json.load(f)

# --- 2. Extract data and text from the loaded JSON ---
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

x_values = [item['x'] for item in chart_data]
y_values = [item['y'] for item in chart_data]

y_axis_title = texts.get('y_axis_title', None)
source_text = texts.get('source', '')
note_text = texts.get('note', '')

# --- 3. Create the Plotly figure ---
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    text=[f"<b>{y}</b>" for y in y_values],
    textposition='outside',
    marker_color=colors[0] if colors else None,
    cliponaxis=False,
    textfont=dict(
        family="Arial",
        size=12,
        color='#333333'
    )
))

# --- 4. Configure the layout to match the original image ---
fig.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12, color='#333333'),
    showlegend=False,
    margin=dict(l=80, r=40, t=50, b=100),
    xaxis=dict(
        type='category',
        showgrid=True,
        gridcolor='#f0f0f0',
        linecolor='black',
        showline=True,
        tickfont=dict(size=11),
    ),
    yaxis=dict(
        title=y_axis_title,
        title_font=dict(size=12),
        title_standoff=15,
        range=[0, 1250],
        tickvals=[0, 200, 400, 600, 800, 1000, 1200],
        ticktext=['0', '200', '400', '600', '800', '1 000', '1 200'],
        showgrid=True,
        gridcolor='#e0e0e0',
        zeroline=False,
        tickfont=dict(size=11),
    ),
    annotations=[
        # Note text (bottom-left)
        dict(
            text=note_text,
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=-0.22,
            xanchor='left',
            yanchor='bottom',
            font=dict(size=12, color='#0073b0')
        ),
        # Source text (bottom-right)
        dict(
            text=source_text,
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.22,
            xanchor='right',
            yanchor='bottom',
            font=dict(size=11)
        )
    ]
)

# --- 5. Save the generated chart to a PNG file ---
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")