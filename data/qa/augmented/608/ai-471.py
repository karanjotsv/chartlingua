import sys
import json
import pathlib
import plotly.graph_objects as go

# --- 1. Load data from JSON file ---
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_file_path}'")
    sys.exit(1)

# --- 2. Extract data and text from the loaded JSON ---
data_series = chart_data.get('chart_data', [])
texts = chart_data.get('texts', {})
colors = chart_data.get('colors', [])

# --- 3. Create the Plotly figure ---
fig = go.Figure()

# Add traces for each data series
for i, series in enumerate(data_series):
    # Format text labels: show integers without decimal points
    text_labels = [f"{v:.0f}" if v == int(v) else str(v) for v in series.get('values', [])]

    fig.add_trace(go.Bar(
        x=series.get('categories', []),
        y=series.get('values', []),
        name=series.get('name', ''),
        marker_color=colors[i % len(colors)] if colors else None,
        text=text_labels,
        textposition='outside',
        cliponaxis=False
    ))

# --- 4. Configure layout ---
fig.update_layout(
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        showline=True,
        linecolor='lightgray',
        zeroline=False,
        ticks='',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=True,
        gridcolor='lightgray',
        range=[0, 3.5],
        dtick=0.5,
        ticks='',
        tickfont=dict(size=12)
    ),
    margin=dict(l=80, r=40, t=40, b=100),
    # Position annotations for source and additional info
    annotations=[
        dict(
            xref='paper', yref='paper',
            x=0, y=-0.15,
            xanchor='left', yanchor='top',
            text=texts.get('additional_info', ''),
            showarrow=False,
            font=dict(size=12, color='#4472c4') # Making it look like a link
        ),
        dict(
            xref='paper', yref='paper',
            x=1, y=-0.15,
            xanchor='right', yanchor='top',
            text=texts.get('source', ''),
            showarrow=False,
            font=dict(size=12)
        )
    ]
)

# Update text font for the bar labels
fig.update_traces(textfont_size=12, textfont_color='black')


# --- 5. Output the chart as a PNG image ---
base_filename = pathlib.Path(json_file_path).stem
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved as '{output_filename}'")