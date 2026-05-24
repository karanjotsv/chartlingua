import sys
import json
import pathlib
import plotly.graph_objects as go

# --- 1. Load data from JSON file ---
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_config = json.load(f)

chart_data = chart_config['chart_data']
texts = chart_config['texts']
colors = chart_config['colors']
ref_line_y = chart_config['ref_line_y']

# --- 2. Create Figure ---
fig = go.Figure()

# --- 3. Add Line Traces ---
for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        name=series['name'],
        mode='lines+markers',
        line=dict(color=colors[i], width=2),
        marker=dict(color=colors[i], size=5)
    ))

# --- 4. Add Bar Traces for the final values ---
for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        x=[series['x'][-1]],
        y=[series['y'][-1]],
        name=series['name'], # Name is needed for grouping
        marker_color=colors[i],
        text=[str(series['y'][-1])],
        textposition='outside',
        textfont=dict(family="Arial", size=12),
        showlegend=False,
        width=86400000 * 3 # width in milliseconds (approx 3 days)
    ))

# --- 5. Add Reference Line and Annotations ---
fig.add_hline(
    y=ref_line_y,
    line_width=1.5,
    line_dash="dash",
    line_color="grey"
)

# Annotations list
annotations = [
    # Reference line label
    go.layout.Annotation(
        text=texts['ref_line_label'],
        align='left',
        showarrow=False,
        xref='paper',
        yref='y',
        x=0.45,
        y=ref_line_y,
        yanchor='bottom',
        font=dict(family="Arial", size=12),
    ),
    # Credit text
    go.layout.Annotation(
        text=texts['credit'],
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0.01,
        y=0.98,
        xanchor='left',
        yanchor='top',
        font=dict(family="Arial", size=10, color='grey'),
    ),
    # "2026" annotation text on the right
    go.layout.Annotation(
        text=texts['end_annotation_text'],
        align='center',
        showarrow=False,
        xref='x',
        yref='y',
        x='2016-03-24',
        y=500,
        font=dict(family="Arial", size=12),
    )
]
fig.update_layout(annotations=annotations)

# Dashed line shape next to the '2026' annotation
fig.add_shape(
    type="line",
    xref="x", yref="y",
    x0='2016-03-27', y0=550,
    x1='2016-04-01', y1=550,
    line=dict(
        color="grey",
        width=1,
        dash="dash",
    )
)

# --- 6. Configure Layout ---
fig.update_layout(
    font=dict(family="Arial"),
    plot_bgcolor='white',
    xaxis=dict(
        title=texts['x_axis_title'],
        tickformat='%b %d',
        showgrid=False,
        linecolor='black',
        zeroline=False
    ),
    yaxis=dict(
        title=texts['y_axis_title'],
        range=[0, 2300],
        gridcolor='#e0e0e0',
        linecolor='black',
        zeroline=True,
        zerolinewidth=1,
        zerolinecolor='black'
    ),
    legend=dict(
        yanchor="top",
        y=0.98,
        xanchor="right",
        x=0.98,
        bgcolor='rgba(255,255,255,0.5)'
    ),
    margin=dict(l=80, r=40, t=60, b=80),
    barmode='group',
    bargap=0.1,
    bargroupgap=0.0
)

# --- 7. Save Image ---
output_filename = json_path.stem + ".png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")