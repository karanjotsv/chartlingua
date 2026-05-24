import sys
import json
import pathlib
import plotly.graph_objects as go

# --- 1. Load data from JSON file ---
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error reading or parsing JSON file: {e}")
    sys.exit(1)

data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# --- 2. Prepare data for Plotly ---
# The data is already in the desired top-to-bottom visual order in the JSON.
# Plotly's y-axis for horizontal bars starts from the bottom, so we use autorange='reversed'.
y_categories = [d['category'] for d in data]
x_values = [d['value'] for d in data]

# Format text labels for bars
bar_texts = []
for item in data:
    val = item['value']
    if val == int(val):
        bar_texts.append(f"{int(val)}%")
    else:
        bar_texts.append(f"{val}%")

# --- 3. Create the figure ---
fig = go.Figure()

# Add the horizontal bar trace
fig.add_trace(go.Bar(
    y=y_categories,
    x=x_values,
    orientation='h',
    marker=dict(color=colors, line=dict(width=0)),
    text=bar_texts,
    textposition='outside',
    textfont=dict(family="Arial", size=14, color='black'),
    cliponaxis=False # Allows text to be drawn outside the plot area
))

# --- 4. Configure layout ---
fig.update_layout(
    # --- Chart Titles and Source ---
    title=dict(
        text=f"<b>{texts['title']}</b><br><span style='font-size: 15px; color: #555;'>{texts['subtitle']}</span>",
        x=0.01,
        y=0.98,
        xanchor='left',
        yanchor='top',
        font=dict(family="Arial", size=24, color='black')
    ),
    annotations=[
        dict(
            text=texts['source'],
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=-0.15,
            xanchor='left',
            yanchor='top',
            align='left',
            font=dict(family="Arial", size=12, color='#666')
        )
    ],

    # --- Axes ---
    xaxis=dict(
        showgrid=True,
        gridcolor='#e0e0e0',
        griddash='dash',
        zeroline=False,
        showline=False,
        showticklabels=True,
        ticksuffix='%',
        range=[0, max(x_values) * 1.05], # Extend range slightly for text
        tickfont=dict(family="Arial", size=14)
    ),
    yaxis=dict(
        autorange='reversed', # To display categories from top to bottom
        showgrid=False,
        showline=False,
        zeroline=False,
        tickfont=dict(family="Arial", size=14)
    ),

    # --- General Styling ---
    font=dict(family="Arial"),
    paper_bgcolor='white',
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(l=250, r=50, t=110, b=100) # Adjust margins for labels
)

# --- 5. Output the image ---
base_filename = pathlib.Path(json_path).stem
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2, width=800, height=600)

print(f"Chart saved to {output_filename}")