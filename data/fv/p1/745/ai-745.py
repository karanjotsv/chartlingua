import sys
import json
import os
import plotly.graph_objects as go

def create_chart(json_path):
    """
    Reads chart data from a JSON file and generates a Plotly chart image.
    """
    # Ensure the file exists before proceeding
    if not os.path.exists(json_path):
        print(f"Error: JSON file not found at '{json_path}'")
        sys.exit(1)

    # Load the chart data from the specified JSON file
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error reading or parsing JSON file: {e}")
        sys.exit(1)

    # Extract data components from the loaded JSON
    chart_data = config['chart_data']
    texts = config['texts']
    colors = config['colors']

    # Prepare data for Plotly trace
    labels = [item['label'] for item in chart_data]
    values = [item['value'] for item in chart_data]
    display_texts = [item['display_text'] for item in chart_data]
    
    # Define text colors for labels inside slices to ensure readability
    # White for darker backgrounds, black for lighter ones
    text_colors = ['white', 'white', 'white', 'black', 'black']

    # Create the pie chart figure
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        text=display_texts,
        textinfo='text',
        hoverinfo='label+percent',
        marker=dict(
            colors=colors,
            line=dict(color='#ffffff', width=1) # Add a thin white line between slices
        ),
        sort=False,  # Preserve the original data order
        direction='clockwise',
        rotation=75, # Rotate to match the orientation of the original chart
        textposition='inside',
        insidetextfont=dict(family="Arial", color=text_colors, size=12)
    )])

    # Update the layout for a clean and accurate presentation
    fig.update_layout(
        title_text=f"<b>{texts['title']}</b>" if texts.get('title') else None,
        title_x=0.5,  # Center the title
        title_font=dict(family="Arial", size=20, color='black'),
        showlegend=False,
        font=dict(family="Arial"),
        margin=dict(t=100, b=50, l=50, r=50), # Adjust margins to prevent clipping
        paper_bgcolor='white',
        plot_bgcolor='white'
    )

    # Determine the output filename and save the image
    base_filename = os.path.splitext(os.path.basename(json_path))[0]
    output_filename = f"{base_filename}.png"
    
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python <script_name>.py <path_to_json_file>")
        sys.exit(1)
    
    json_file_path = sys.argv[1]
    create_chart(json_file_path)