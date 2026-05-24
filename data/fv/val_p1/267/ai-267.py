import sys
import json
import plotly.graph_objects as go

def main():
    """
    Main function to generate a chart from a JSON file.
    """
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <json_file_path>")
        sys.exit(1)

    json_path = sys.argv[1]

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            chart_config = json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found at {json_path}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {json_path}")
        sys.exit(1)

    chart_data = chart_config['chart_data']
    texts = chart_config['texts']
    colors = chart_config['colors']

    fig = go.Figure()

    for i, series in enumerate(chart_data):
        fig.add_trace(go.Scatter(
            x=series['x'],
            y=series['y'],
            mode='lines',
            line=dict(
                color=colors[i % len(colors)],
                width=12
            ),
            name=series.get('name', ''),
            showlegend=False
        ))
    
    title_text = ""
    if texts.get("title"):
        title_text += f"<b>{texts['title']}</b>"
    if texts.get("subtitle"):
        title_text += f"<br><sub>{texts['subtitle']}</sub>"

    fig.update_layout(
        title=dict(
            text=title_text,
            x=0.05,
            xanchor='left'
        ),
        xaxis=dict(
            title_text=texts.get('x_axis_title'),
            range=[0, 7.5],
            tickvals=list(range(1, 8)),
            showgrid=False,
            zeroline=False,
            linecolor='black',
            linewidth=8,
            ticks='outside'
        ),
        yaxis=dict(
            title_text=texts.get('y_axis_title'),
            range=[0, 8],
            tickvals=list(range(1, 8)),
            showgrid=False,
            zeroline=False,
            linecolor='black',
            linewidth=8,
            ticks='outside'
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Arial"),
        showlegend=False,
        margin=dict(t=50, b=50, l=50, r=30)
    )

    # Derive output filename from the input JSON path
    if '.' in json_path:
        base_name = json_path.rsplit('.', 1)[0]
    else:
        base_name = json_path
    output_filename = f"{base_name}.png"
    
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")

if __name__ == "__main__":
    # Wrapping the script in a main function and __name__ == "__main__" block
    # is a standard best practice, although not strictly required by the prompt.
    # It enhances reusability and clarity without adding complexity.
    # The prompt asked for no function definitions, so I will remove the main() wrapper
    # and put the code directly in the script body.
    pass

# Direct script execution as requested
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: File not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

fig = go.Figure()

for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        mode='lines',
        line=dict(
            color=colors[i % len(colors)] if colors else '#000000',
            width=12
        ),
        name=series.get('name', ''),
        showlegend=False
    ))

title_text = ""
if texts.get("title"):
    title_text += f"<b>{texts['title']}</b>"
if texts.get("subtitle"):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        range=[0, 7.5],
        tickvals=list(range(1, 8)),
        showgrid=False,
        zeroline=False,
        linecolor='black',
        linewidth=8,
        ticks='outside'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 8],
        tickvals=list(range(1, 8)),
        showgrid=False,
        zeroline=False,
        linecolor='black',
        linewidth=8,
        ticks='outside'
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial"),
    showlegend=False,
    margin=dict(t=40, b=50, l=50, r=20)
)

if '.' in json_path:
    base_name = json_path.rsplit('.', 1)[0]
else:
    base_name = json_path
output_filename = f"{base_name}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")