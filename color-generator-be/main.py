from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from PIL import Image
import io
import numpy as np
from sklearn.cluster import KMeans
import colorsys
from typing import List, Dict, Any
import uvicorn

app = FastAPI(
    title="Color Palette Analyzer",
    description="API for extracting dominant colors from images",
    version="1.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Modify for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ColorInfo:
    """Class to represent color information with useful attributes"""
    def __init__(self, rgb, percentage):
        self.rgb = tuple(int(x) for x in rgb)
        self.hex = '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])
        self.percentage = float(percentage)
        
        # Convert RGB to HSV for better color analysis
        r, g, b = [x/255.0 for x in self.rgb]
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        self.hsv = (h, s, v)
        
        # Determine if color is dark or light
        self.is_dark = (r * 0.299 + g * 0.587 + b * 0.114) < 0.5
        
        # Get color name based on hue
        self.name = self._get_color_name(h, s, v)
    
    def _get_color_name(self, h, s, v):
        """Determine approximate color name based on HSV values"""
        if v < 0.2:
            return "Black"
        if v > 0.9 and s < 0.1:
            return "White"
        if s < 0.1:
            return "Gray"
        
        h_degrees = h * 360
        
        if h_degrees < 30 or h_degrees >= 330:
            return "Red"
        elif h_degrees < 90:
            return "Yellow"
        elif h_degrees < 150:
            return "Green"
        elif h_degrees < 210:
            return "Cyan"
        elif h_degrees < 270:
            return "Blue"
        else:
            return "Magenta"
    
    def to_dict(self):
        """Convert to dictionary for JSON response"""
        return {
            "rgb": self.rgb,
            "hex": self.hex,
            "percentage": round(self.percentage, 2),
            "name": self.name,
            "is_dark": self.is_dark
        }

def extract_colors(image: Image.Image, num_colors: int = 7) -> List[ColorInfo]:
    """Extract dominant colors from an image using K-means clustering"""
    # Resize image to speed up processing
    image = image.copy()
    image.thumbnail((200, 200))
    
    # Convert to RGB if in another mode (like RGBA)
    if image.mode != "RGB":
        image = image.convert("RGB")
    
    # Prepare the image data for clustering
    pixels = np.array(image)
    pixels = pixels.reshape(-1, 3)
    
    # Use K-means to find dominant colors
    kmeans = KMeans(n_clusters=num_colors, n_init=10)
    kmeans.fit(pixels)
    
    # Get the colors and their percentages
    colors = kmeans.cluster_centers_.astype(int)
    labels = kmeans.labels_
    
    # Count occurrences of each label
    counts = np.bincount(labels)
    percentages = counts / len(labels)
    
    # Sort colors by their frequency
    color_info = []
    for i in range(len(colors)):
        color_info.append(ColorInfo(tuple(colors[i]), percentages[i] * 100))
    
    # Sort by percentage (descending)
    color_info.sort(key=lambda x: x.percentage, reverse=True)
    
    return color_info

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Chroma Extractor API",
        "version": "1.0.0",
        "endpoints": [
            {"path": "/", "method": "GET", "description": "This information"},
            {"path": "/analyze", "method": "POST", "description": "Upload and analyze an image"},
            {"path": "/analyze/{num_colors}", "method": "POST", "description": "Analyze with custom palette size"}
        ]
    }

@app.post("/analyze")
async def analyze_image(file: UploadFile = File(...), num_colors: int = 5):
    """
    Analyze an uploaded image and extract its color palette
    
    - **file**: The image file to analyze
    - **num_colors**: Number of colors to extract (default: 5)
    """
    # Validate file is an image
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # Validate num_colors
    if num_colors < 1 or num_colors > 20:
        raise HTTPException(status_code=400, detail="Number of colors must be between 1 and 20")
    
    try:
        # Read image data
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data))
        
        # Extract colors
        color_info = extract_colors(image, num_colors)
        
        # Prepare response
        response = {
            "filename": file.filename,
            "image_size": {"width": image.width, "height": image.height},
            "colors": [color.to_dict() for color in color_info],
            "total_colors": len(color_info)
        }
        
        return JSONResponse(content=response)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

@app.post("/analyze/{num_colors}")
async def analyze_image_with_colors(num_colors: int, file: UploadFile = File(...)):
    """Endpoint for analyzing with path parameter for number of colors"""
    return await analyze_image(file, num_colors)

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)