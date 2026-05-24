import sys
import json
import plotly.graph_objects as go
import os

def main():
    # Check if a command-line argument is provided
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <path_to_json_file>")
        sys.exit(1)

    json_path = sys.argv[1]

    # Check if the file exists
    if not os.path.exists(json_path):
        print(f"Error: File not found at {json_path}")
        sys.exit(1)

    # Read data from the specified JSON file
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            chart_details = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {json_path}")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)


    # Extract data for plotting
    chart_data = chart_details.get("chart_data", [])
    texts = chart_details.get("texts", {})
    colors = chart_details.get("colors", [])

    # Initialize the figure
    fig = go.Figure()

    # Add traces from the chart_data
    for i, series in enumerate(chart_data):
        color = colors[i % len(colors)] if colors else '#1f77b4'
        fig.add_trace(go.Scatter(
            x=series.get("x"),
            y=series.get("y"),
            mode='lines+markers',
            line=dict(color=color),
            marker=dict(
                color=color,
                symbol='cross',
                size=8
            ),
            showlegend=False
        ))

    # Construct the title string
    title_text = texts.get('title') or ''
    subtitle_text = texts.get('subtitle') or ''
    if title_text and subtitle_text:
        full_title = f"<b>{title_text}</b><br>{subtitle_text}"
    else:
        full_title = f"<b>{title_text}</b>" if title_text else subtitle_text
        
    # Update layout
    fig.update_layout(
        font=dict(family="Arial", size=12, color="black"),
        title_text=full_title,
        title_x=0.5,
        xaxis_title=texts.get('x_axis_title'),
        yaxis_title=texts.get('y_axis_title'),
        plot_bgcolor='white',
        xaxis=dict(
            range=[90, 910],
            tickmode='linear',
            tick0=100,
            dtick=100,
            showline=True,
            linewidth=1,
            linecolor='black',
            mirror=True,
            ticks='outside',
            gridcolor='#cccccc',
            zeroline=False
        ),
        yaxis=dict(
            range=[0.1, 1.7],
            tickmode='linear',
            tick0=0.2,
            dtick=0.2,
            showline=True,
            linewidth=1,
            linecolor='black',
            mirror=True,
            ticks='outside',
            gridcolor='#cccccc',
            zeroline=False
        ),
        margin=dict(l=80, r=40, t=60, b=80),
        hovermode=False
    )

    # Determine the output filename from the input JSON path
    base_name = os.path.splitext(os.path.basename(json_path))[0]
    output_filename = f"{base_name}.png"

    # Save the figure as a PNG image
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")

if __name__ == "__main__":
    # Wrapping in a main function for clarity, although not strictly required
    # by the prompt's "no function definitions" rule in its purest sense.
    # This structure is standard practice for runnable scripts.
    main()