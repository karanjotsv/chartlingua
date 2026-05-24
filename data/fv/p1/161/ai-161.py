import sys
import json
import pathlib
import plotly.graph_objects as go

# --- 1. Load data from JSON file ---
if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <path_to_json_file>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_json = json.load(f)

# Extract data, texts, and colors from the loaded JSON
data = chart_json['chart_data']
texts = chart_json['texts']
colors = chart_json['colors']

# --- 2. Create Plotly Figure ---
fig = go.Figure()

# Add Bar trace for runs
fig.add_trace(go.Bar(
    x=data['x_values'],
    y=data['runs'],
    name='Runs',
    marker_color=colors[0],
    showlegend=False
))

# Add Line trace for average
fig.add_trace(go.Scatter(
    x=data['average']['x'],
    y=data['average']['y'],
    mode='lines',
    name='10-inning Average',
    line=dict(color=colors[1], width=2),
    showlegend=False
))

# Add Scatter trace for 'not out' innings
fig.add_trace(go.Scatter(
    x=data['not_out']['x'],
    y=data['not_out']['y'],
    mode='markers',
    name='Not Out',
    marker=dict(color=colors[1], size=5),
    showlegend=False
))

# --- 3. Configure Layout ---
fig.update_layout(
    title=dict(
        text=texts['title'],
        x=0.5,
        y=0.98,
        xanchor='center',
        yanchor='top',
        font=dict(size=16)
    ),
    xaxis=dict(
        tickvals=data['x_axis_ticks']['tickvals'],
        ticktext=data['x_axis_ticks']['ticktext'],
        showgrid=False,
        showline=True,
        linecolor='black',
        mirror=True
    ),
    yaxis=dict(
        range=[0, 140],
        tickmode='linear',
        tick0=0,
        dtick=20,
        showgrid=True,
        gridcolor='black',
        gridwidth=0.5,
        zeroline=False,
        showline=True,
        linecolor='black',
        mirror=True
    ),
    font_family="Arial",
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=40, r=20, t=60, b=40),
    bargap=0.6,
    height=500,
    width=800
)

# --- 4. Output Image ---
output_filename = json_path.stem + ".png"
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")