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
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# --- 2. Extract data and texts ---
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Format values for display on bars with space as thousand separator
formatted_text_values = [f'{v:,}'.replace(',', ' ') for v in values]

# --- 3. Create the Plotly figure ---
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0] if colors else None,
    text=formatted_text_values,
    textposition='outside',
    texttemplate='%{text}',
    cliponaxis=False # Prevents text labels from being clipped
))

# --- 4. Configure layout ---
annotations = []
if texts.get('source'):
    annotations.append(dict(
        xref='paper', yref='paper',
        x=1.0, y=-0.15,
        xanchor='right', yanchor='top',
        text=texts['source'],
        showarrow=False,
        align='right',
        font=dict(family="Arial", size=12, color="#666666")
    ))

if texts.get('note'):
     annotations.append(dict(
        xref='paper', yref='paper',
        x=0.0, y=-0.15,
        xanchor='left', yanchor='top',
        text=texts['note'],
        showarrow=False,
        align='left',
        font=dict(family="Arial", size=12, color="#007ACC")
    ))


fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
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
        range=[0, 600000],
        showgrid=True,
        gridcolor='#dddddd',
        zeroline=False,
        tickfont=dict(size=12),
        tickformat=' ' # Use space as thousands separator
    ),
    margin=dict(l=80, r=40, b=120, t=50),
    annotations=annotations
)

# --- 5. Output the image ---
output_filename = json_path.with_suffix('.png').name
fig.write_image(output_filename, scale=2)
print(f"Chart saved as {output_filename}")