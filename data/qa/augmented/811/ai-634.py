import sys
import json
import pathlib
import plotly.graph_objects as go

# --- 1. Argument and File Handling ---
if len(sys.argv) != 2:
    print(f"Usage: python {pathlib.Path(__file__).name} <json_file_path>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

output_path = json_path.with_suffix('.png')

# --- 2. Data Loading ---
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except (json.JSONDecodeError, IOError) as e:
    print(f"Error reading or parsing JSON file: {e}")
    sys.exit(1)

chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# --- 3. Data Preparation ---
categories = [item.get('category') for item in chart_data]
values = [item.get('value') for item in chart_data]

# --- 4. Chart Creation ---
fig = go.Figure()

# Add bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=values,
    textposition='outside',
    texttemplate='%{text:.1f}',
    marker_color=colors[0] if colors else None,
    cliponaxis=False  # Prevents text labels from being clipped at the top
))

# --- 5. Layout and Styling ---
fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(l=90, r=40, t=40, b=120),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        showline=True,
        linecolor='lightgray',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 200],
        dtick=25,
        gridcolor='#E5E5E5',
        griddash='dash',
        zeroline=False,
        showline=False,
        tickfont=dict(size=12)
    ),
    # Add annotations for source and note at the bottom
    annotations=[
        dict(
            showarrow=False,
            xref='paper', yref='paper',
            x=0, y=-0.25,
            xanchor='left', yanchor='top',
            text=texts.get('note'),
            font=dict(size=12)
        ),
        dict(
            showarrow=False,
            xref='paper', yref='paper',
            x=1, y=-0.25,
            xanchor='right', yanchor='top',
            text=texts.get('source'),
            font=dict(size=12)
        )
    ]
)

# --- 6. Output ---
fig.write_image(output_path, scale=2)
print(f"Chart successfully generated and saved to '{output_path}'")