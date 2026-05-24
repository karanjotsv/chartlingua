import sys
import json
import os
import plotly.graph_objects as go

# --- 1. Load data from JSON file ---
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]
if not os.path.exists(json_file_path):
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)

with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# --- 2. Create the Plotly figure ---
fig = go.Figure()

# --- 3. Add data traces ---
for i, series in enumerate(chart_data):
    color = colors[i % len(colors)]
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        mode='lines+markers+text',
        name=series.get('name', ''),
        line=dict(color=color, width=2.5),
        marker=dict(color=color, size=7),
        text=[f"{val:.2f}" for val in series['y']],
        textposition='top center',
        textfont=dict(
            family="Arial",
            size=12,
            color='black'
        )
    ))

# --- 4. Configure layout and styling ---
# In the original chart, some labels are below the line to avoid overlap.
# Plotly's default `textposition` is static per trace. `top center` is a close approximation.
# For perfect replication, individual annotations would be required.

annotations = []
# Add source text as an annotation
if texts.get('source'):
    annotations.append(
        dict(
            text=texts['source'],
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.18, # Adjusted for visibility
            xanchor='right',
            yanchor='top',
            font=dict(family="Arial", size=12)
        )
    )

fig.update_layout(
    font=dict(family="Arial", size=14),
    title=dict(
        text=texts.get('title') or '',
        font=dict(size=24)
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        tickfont=dict(size=12),
        zeroline=False
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[144, 152.5],  # Added padding at the top for labels
        dtick=1,
        showgrid=True,
        gridcolor='#EAEAEA',
        gridwidth=1,
        tickfont=dict(size=12),
        zeroline=False
    ),
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(l=100, r=40, t=40, b=80),
    annotations=annotations
)

# --- 5. Output the chart as a PNG image ---
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")