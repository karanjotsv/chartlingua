import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_file_path}")
    sys.exit(1)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

fig = go.Figure()

# Add main trace
series = chart_data[0]
fig.add_trace(go.Scatter(
    x=series['x'],
    y=series['y'],
    mode='lines+markers',
    line=dict(color=colors[0], width=2.5),
    marker=dict(color=colors[0], size=8),
    hoverinfo='none'
))

# Add data labels as annotations for better positioning control
for x_val, y_val in zip(series['x'], series['y']):
    fig.add_annotation(
        x=x_val,
        y=y_val,
        text=f"<b>{y_val}%</b>",
        showarrow=False,
        font=dict(family="Arial", size=12, color="#000000"),
        yshift=15
    )

fig.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12, color='#333333'),
    showlegend=False,
    margin=dict(l=80, r=40, t=40, b=120),
    yaxis=dict(
        title=dict(text=texts.get('y_axis_title'), standoff=15),
        range=[29, 32],
        ticksuffix='%',
        showgrid=True,
        gridcolor='#EAEAEA',
        showline=False,
        zeroline=False
    ),
    xaxis=dict(
        showgrid=True,
        gridcolor='#FDFDFD', # very light vertical grid
        showline=False,
        zeroline=False
    )
)

# Add source and note annotations
annotations = []
if texts.get('note'):
    annotations.append(
        dict(
            xref='paper', yref='paper',
            x=0, y=-0.25,
            xanchor='left', yanchor='bottom',
            text=texts['note'],
            showarrow=False,
            font=dict(family="Arial", size=12, color='#3B82F6')
        )
    )
if texts.get('source'):
    annotations.append(
        dict(
            xref='paper', yref='paper',
            x=1, y=-0.25,
            xanchor='right', yanchor='bottom',
            text=texts['source'],
            showarrow=False,
            font=dict(family="Arial", size=12, color='#888888')
        )
    )

fig.update_layout(annotations=annotations)

output_filename_base = json_file_path.rsplit('.', 1)[0]
output_filename_png = f"{output_filename_base}.png"
fig.write_image(output_filename_png, scale=2)

print(f"Chart successfully generated and saved to {output_filename_png}")