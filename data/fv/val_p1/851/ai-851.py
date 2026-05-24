import sys
import json
import pathlib
import plotly.graph_objects as go

def main():
    # Check for command-line argument
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <json_file_path>")
        sys.exit(1)

    json_path = pathlib.Path(sys.argv[1])
    if not json_path.is_file():
        print(f"Error: JSON file not found at '{json_path}'")
        sys.exit(1)

    # Load data from the specified JSON file
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)

    # Extract data and texts from the JSON structure
    chart_data = chart_info["chart_data"]
    series_names = chart_info["series_names"]
    texts = chart_info["texts"]
    colors = chart_info["colors"]
    
    # Prepare data for Plotly
    categories = [item['category'] for item in chart_data]
    
    # Create figure
    fig = go.Figure()

    # Add bar traces for each series, iterating to preserve order
    for i, series_name in enumerate(series_names):
        values = [item['values'][i] for item in chart_data]
        fig.add_trace(go.Bar(
            x=categories,
            y=values,
            name=series_name,
            marker_color=colors[i]
        ))

    # Update layout for styling, titles, and axes
    fig.update_layout(
        title_text=texts['title'],
        title_x=0.5,
        yaxis_title_text=texts['y_axis_title'],
        xaxis_title_text=texts['x_axis_title'],
        barmode='group',
        plot_bgcolor='white',
        font=dict(
            family="Arial",
            size=12,
            color="black"
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5
        ),
        yaxis=dict(
            range=[0, 35],
            gridcolor='lightgray',
            zeroline=False,
            showline=False,
            tickmode='linear',
            tick0=0,
            dtick=5
        ),
        xaxis=dict(
            showgrid=False,
            showline=False
        ),
        margin=dict(t=100, b=100, l=80, r=40)
    )
    
    # Define output filename based on the input JSON filename
    output_filename = json_path.with_suffix(".png")

    # Save the figure to a file
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")

if __name__ == "__main__":
    main()