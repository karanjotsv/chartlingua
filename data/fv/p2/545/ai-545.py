import sys
import json
import plotly.graph_objects as go
from pathlib import Path

def main():
    # Check for command-line argument
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <json_file_path>")
        sys.exit(1)

    # Get file path from command-line argument
    json_path = Path(sys.argv[1])
    if not json_path.is_file():
        print(f"Error: File not found at {json_path}")
        sys.exit(1)

    # Read and parse the JSON file
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)

    # Initialize the figure
    fig = go.Figure()

    # Define the domains for the two pie charts
    domains = [
        {'x': [0, 0.48], 'y': [0, 1]},
        {'x': [0.52, 1], 'y': [0, 1]}
    ]

    # Add pie chart traces from the JSON data
    for i, data in enumerate(chart_data["chart_data"]):
        fig.add_trace(go.Pie(
            labels=data["labels"],
            values=data["values"],
            domain=domains[i],
            marker=dict(colors=data["colors"], line=dict(color='#ffffff', width=2)),
            pull=data["pull"],
            rotation=data.get("rotation", 0),
            direction='clockwise',
            textposition='inside',
            insidetextorientation='radial',
            insidetextfont=dict(color='white'),
            hoverinfo='label+percent',
            sort=False,
            showlegend=False
        ))

    # Update layout properties
    fig.update_layout(
        font=dict(family="Arial"),
        margin=dict(t=120, b=40, l=40, r=40),
        paper_bgcolor='white',
        plot_bgcolor='white'
    )
    
    # Add annotations from the JSON data
    if chart_data["texts"]["annotations"]:
        for ann in chart_data["texts"]["annotations"]:
            fig.add_annotation(
                text=ann["text"],
                xref="paper", yref="paper",
                x=ann["x"], y=ann["y"],
                showarrow=True,
                arrowhead=0,
                arrowcolor="#000000",
                arrowwidth=1,
                ax=ann["ax"],
                ay=ann["ay"],
                font=dict(
                    family="Arial",
                    size=ann["font_size"],
                    color="#000000"
                )
            )

    # Define output filename and save the image
    output_filename = f"{json_path.stem}.png"
    fig.write_image(output_filename, scale=2)
    print(f"Image saved to {output_filename}")


if __name__ == "__main__":
    main()