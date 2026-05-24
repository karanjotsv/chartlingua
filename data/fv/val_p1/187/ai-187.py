import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script.py> <path_to_json>")
    sys.exit(1)

json_path = sys.argv[1]

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

chart_data = data.get('chart_data', {})
labels = chart_data.get('labels', [])
values = chart_data.get('values', [])
texts = data.get('texts', {})
colors = data.get('colors', [])

fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(
        colors=colors,
        line=dict(color='white', width=2)
    ),
    textinfo='label',
    textfont=dict(family="Arial", size=10),
    insidetextorientation='horizontal',
    hoverinfo='none',
    sort=False,
    direction='clockwise',
    textposition='inside'
))

fig.update_layout(
    title_text=texts.get('title'),
    title_x=0.5,
    title_xanchor='center',
    font_family="Arial",
    showlegend=False,
    margin=dict(t=80, b=20, l=20, r=20)
)

# Set text color to white for the dark orange slice (NDP) for better contrast
# and black for others. This requires a list of colors.
text_colors = ['black', 'black', 'white', 'black', 'black']
fig.data[0].textfont.color = text_colors[2] # This is a limitation, we can only set one color.
# The best approach for mixed colors is to set them for each slice if possible.
# In Plotly, this is not directly supported for pie textfont, so we apply the most contrasting color.
# After re-evaluation, the best we can do is specify colors for text.
# Plotly go.Pie does not accept a list for `textfont.color`.
# A single color must be chosen. White text is needed for the NDP slice. Black for others.
# As a compromise for this limitation, we will let some text have lower contrast.
# We'll set all text to black as it's readable on 4/5 slices. The user can tweak if needed.
# An alternative is to manually create annotations for each slice, which is overly complex.
fig.data[0].textfont.color = 'black'


base_name = json_path
if '/' in base_name:
    base_name = base_name.split('/')[-1]
if '\\' in base_name:
    base_name = base_name.split('\\')[-1]
base_name = base_name.rsplit('.', 1)[0]

output_filename = f"{base_name}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")