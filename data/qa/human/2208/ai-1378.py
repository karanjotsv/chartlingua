import sys
import json
import pathlib
import plotly.graph_objects as go

# --- 1. Load Data from Command-Line Argument ---
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_filepath = pathlib.Path(sys.argv[1])
if not json_filepath.is_file():
    print(f"Error: File not found at {json_filepath}")
    sys.exit(1)

with open(json_filepath, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# --- 2. Extract Data and Texts from JSON ---
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])
output_filename_base = json_filepath.stem

# --- 3. Create Chart ---
fig = go.Figure()

# Add traces by iterating through the data from the JSON file
for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        x=series['x'],
        y=series['y'],
        name=series['name'],
        marker_color=colors[i],
        text=series['y'],
        texttemplate='<b>%{text}</b>',
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(
            family="Arial",
            size=14,
            color='white'
        )
    ))

# --- 4. Configure Layout ---
fig.update_layout(
    barmode='stack',
    title_text=texts.get('title'),
    yaxis_title_text=texts.get('y_axis_title'),
    xaxis_title_text=texts.get('x_axis_title'),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    xaxis=dict(
        showgrid=False,
        linecolor='black',
        zeroline=False
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='#e0e0e0',
        range=[0, 3500],
        zeroline=False,
        linecolor='black',
        tickformat=','
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.3,
        xanchor="center",
        x=0.5
    ),
    margin=dict(l=80, r=40, t=50, b=120),
    annotations=[
        dict(
            text=texts.get('source'),
            align='right',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.32,
            xanchor='right',
            yanchor='bottom',
            font=dict(
                family="Arial",
                size=12
            )
        )
    ]
)

# --- 5. Output Chart ---
output_image_path = f"{output_filename_base}.png"
fig.write_image(output_image_path, scale=2)
print(f"Chart saved to {output_image_path}")