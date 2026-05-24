import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# --- 1. Load data from JSON file ---
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = Path(sys.argv[1])
if not json_file_path.is_file():
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)

with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info["chart_data"]
texts = chart_info["texts"]
colors = chart_info["colors"]
output_filename_base = json_file_path.stem

# --- 2. Create the Plotly figure ---
fig = go.Figure()

# --- 3. Add traces based on chart_data ---
# Trace for '2016' (line, markers, text)
data_2016 = chart_data[0]
fig.add_trace(go.Scatter(
    x=data_2016['x'],
    y=data_2016['y'],
    name=data_2016['name'],
    mode='lines+markers+text',
    line=dict(color=colors[0], width=3),
    marker=dict(color=colors[0], size=8),
    text=[str(y) for y in data_2016['y']],
    textposition='top center',
    textfont=dict(family='Arial', size=14, color='#000000'),
    legendgroup='group1'
))

# Trace for '2017' (markers, text for the single point)
data_2017 = chart_data[1]
fig.add_trace(go.Scatter(
    x=data_2017['x'],
    y=data_2017['y'],
    name=data_2017['name'],
    mode='markers+text',
    marker=dict(color=colors[1], size=8, symbol='circle'),
    text=[str(y) if y is not None else '' for y in data_2017['y']],
    textposition='top center',
    textfont=dict(family='Arial', size=14, color='#000000'),
    legendgroup='group2'
))

# --- 4. Configure layout ---
fig.update_layout(
    font=dict(family="Arial", size=12, color="#6f6f6f"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis=dict(
        showgrid=True,
        gridcolor='#eeeeee',
        gridwidth=1,
        zeroline=False,
        showline=False,
        ticklen=0,
        title_text=texts['x_axis_title'] if texts['x_axis_title'] else ''
    ),
    yaxis=dict(
        title=texts['y_axis_title'],
        showgrid=True,
        gridcolor='#eeeeee',
        gridwidth=1,
        zeroline=False,
        showline=False,
        range=[140, 205] # Added padding for top labels
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.3,
        xanchor="center",
        x=0.5,
        traceorder='normal',
        font=dict(size=12)
    ),
    margin=dict(l=90, r=40, b=120, t=50),
    showlegend=True
)

# --- 5. Add annotations for source text ---
annotations = []
if texts.get('source'):
    annotations.append(
        dict(
            xref="paper",
            yref="paper",
            x=0.99,
            y=-0.35,
            xanchor='right',
            yanchor='bottom',
            text=texts['source'],
            showarrow=False,
            font=dict(family="Arial", size=12, color="#6f6f6f")
        )
    )
fig.update_layout(annotations=annotations)

# --- 6. Output the chart as a PNG file ---
output_image_path = f"{output_filename_base}.png"
fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")