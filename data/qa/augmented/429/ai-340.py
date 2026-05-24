import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# --- 1. Load Data from Command-Line Argument ---
if len(sys.argv) != 2:
    print(f"Usage: python {Path(__file__).name} <json_file_path>")
    sys.exit(1)

json_file_path = Path(sys.argv[1])
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON in {json_file_path}")
    sys.exit(1)

# --- 2. Prepare Data and Texts ---
data = chart_config['chart_data']
texts = chart_config['texts']
colors = chart_config['colors']

x_values = [d['x'] for d in data]
y_values = [d['y'] for d in data]

# --- 3. Create Chart Figure ---
fig = go.Figure()

# Add bar trace
fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    text=y_values,
    textposition='outside',
    texttemplate='%{text}',
    marker_color=colors[0],
    cliponaxis=False  # Prevent text on top of bars from being clipped
))

# --- 4. Configure Layout ---
title_text = texts.get('title') if texts.get('title') else ''
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

fig.update_layout(
    font_family="Arial",
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=50, b=100),
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title_text=texts.get('xaxis_title'),
        showgrid=False,
        tickmode='array',
        tickvals=x_values,
        ticktext=[str(x) for x in x_values] # Ensure x-axis labels are treated as categories
    ),
    yaxis=dict(
        title_text=texts.get('yaxis_title'),
        range=[0, 2000],
        tickvals=[0, 250, 500, 750, 1000, 1250, 1500, 1750, 2000],
        gridcolor='#e5e5e5',
        gridwidth=1,
        griddash='dot'
    ),
    annotations=[
        dict(
            text=texts.get('source', ''),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.2,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(size=12, color='#666666')
        )
    ]
)

# Update text font properties on the bars
fig.update_traces(textfont_size=12, textfont_color='black')


# --- 5. Output Image ---
base_filename = json_file_path.stem
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")