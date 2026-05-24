import sys
import json
import pathlib
import plotly.graph_objects as go

# --- 1. Load Data from JSON ---
# The script expects the path to the JSON file as the single command-line argument.
if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <path_to_json_file>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# --- 2. Create Figure ---
fig = go.Figure()

# --- 3. Add Traces (Bars) ---
# Iterate through each series in the JSON data to create a bar trace.
# This ensures the order of series and colors is preserved.
categories = chart_data['chart_data']['categories']
series_data = chart_data['chart_data']['series']
colors = chart_data['colors']

for i, series in enumerate(series_data):
    # Format the text labels to be displayed on top of the bars with a '%' suffix.
    bar_texts = [f'{val:g}%' for val in series['data']]
    
    fig.add_trace(go.Bar(
        x=categories,
        y=series['data'],
        name=series['name'],
        marker_color=colors[i],
        text=bar_texts,
        textposition='outside',
        textfont=dict(family='Arial', size=12, color='black'),
        cliponaxis=False  # Prevents text labels from being clipped at the top of the plot area
    ))

# --- 4. Configure Layout ---
texts = chart_data['texts']

# Combine source and note for the footer annotation
footer_texts = []
if texts['source_text']:
    footer_texts.append(texts['source_text'])
if texts['note_text']:
    footer_texts.append(texts['note_text'])
footer_text = "<br>".join(footer_texts)


fig.update_layout(
    barmode='group',
    plot_bgcolor='white',
    font=dict(family="Arial", size=12, color="black"),
    margin=dict(l=90, r=40, b=120, t=50, pad=4),

    xaxis=dict(
        categoryorder='array',
        categoryarray=categories,
        showline=True,
        linewidth=1.5,
        linecolor='black',
        tickfont=dict(size=12)
    ),

    yaxis=dict(
        title=dict(
            text=texts['y_axis_title'],
            font=dict(size=14)
        ),
        range=[0, 2700],
        tickvals=[0, 500, 1000, 1500, 2000, 2500],
        showgrid=True,
        gridwidth=1,
        gridcolor='#E5E5E5',
        griddash='dot',
        zeroline=False,
        tickfont=dict(size=12)
    ),

    legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.2,
        xanchor="center",
        x=0.5,
        font=dict(size=14),
        traceorder='normal'
    ),
    
    annotations=[
        dict(
            showarrow=False,
            text=footer_text,
            xref="paper",
            yref="paper",
            x=1.0,
            y=-0.28,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(size=12)
        )
    ]
)


# --- 5. Output Image ---
# Derive the output filename from the input JSON filename.
output_filename = json_path.stem + ".png"
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")