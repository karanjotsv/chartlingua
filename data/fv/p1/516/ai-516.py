import sys
import json
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def main():
    """
    Main function to generate the chart from a JSON file.
    """
    if len(sys.argv) != 2:
        print("Usage: python <script_name>.py <json_file_path>")
        sys.exit(1)

    json_filepath = sys.argv[1]

    try:
        with open(json_filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at {json_filepath}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {json_filepath}")
        sys.exit(1)

    # Derive the output filename base from the input JSON path
    filename_base = json_filepath.split('/')[-1].split('\\')[-1].split('.')[0]
    output_filename = f"{filename_base}.png"

    fig = make_subplots(
        rows=2, cols=1,
        specs=[[{'type': 'domain'}], [{'type': 'domain'}]],
        vertical_spacing=0.1
    )

    # Define a pull array to explode the 'Other' slice, matching the original chart
    pull_values = [0, 0, 0, 0.1]

    # Add Pie traces
    for i, chart_spec in enumerate(data['chart_data']):
        fig.add_trace(
            go.Pie(
                labels=chart_spec['labels'],
                values=chart_spec['values'],
                name=chart_spec['title'],
                marker_colors=data['colors'],
                hoverinfo='label+percent',
                textinfo='none',
                pull=pull_values,
                sort=False,
                showlegend=(i == 0) # Show legend only for the first pie chart
            ),
            row=i + 1, col=1
        )

    # Add annotations for subplot titles, mimicking the original layout
    fig.add_annotation(
        text=f"<b>{data['chart_data'][0]['title']}</b>",
        xref="paper", yref="paper",
        x=0.85, y=0.8,
        showarrow=False,
        font=dict(size=16, family="Arial")
    )
    fig.add_annotation(
        text=f"<b>{data['chart_data'][1]['title']}</b>",
        xref="paper", yref="paper",
        x=0.85, y=0.2,
        showarrow=False,
        font=dict(size=16, family="Arial")
    )

    # Update layout for styling, titles, and background
    fig.update_layout(
        title_text=data['texts']['title'],
        title_x=0.5,
        title_font=dict(size=18),
        paper_bgcolor='black',
        plot_bgcolor='black',
        font=dict(family="Arial", color="white"),
        height=600,
        width=900,
        margin=dict(t=80, b=40, l=40, r=40),
        legend=dict(
            traceorder='normal',
            x=0.9,
            y=0.5,
            xanchor='right',
            yanchor='middle'
        )
    )

    # Save the figure as a PNG image
    fig.write_image(output_filename, scale=2)
    print(f"Image saved to {output_filename}")

if __name__ == "__main__":
    main()