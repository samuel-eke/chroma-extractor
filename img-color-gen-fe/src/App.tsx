import React, { useState, useRef } from 'react';
import axios from 'axios';
import './app.css';

interface ColorData {
  rgb: number[];
  hex: string;
  percentage: number;
  name: string;
}

export function ChromaExtractor() {
  // State variables
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewSrc, setPreviewSrc] = useState<string>('');
  const [colors, setColors] = useState<ColorData[]>([]);
  const [showPreview, setShowPreview] = useState<boolean>(false);

  // Reference to file input
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Handle file selection
  function handleFileChange(event: React.ChangeEvent<HTMLInputElement>) {
    const files = event.target.files;

    if (files && files.length > 0) {
      const file = files[0];
      setSelectedFile(file);

      const reader = new FileReader();
      reader.onload = function(e) {
        if (e.target) {
          setPreviewSrc(e.target.result as string);
          setShowPreview(true);
        }
      };
      reader.readAsDataURL(file);
    }
  }

  // Handle upload button click
  async function uploadImage() {
    if (!selectedFile) {
      alert("Please select an image first");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await axios.post("http://127.0.0.1:8000/analyze", formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });

      setColors(response.data.colors);
    } catch (error) {
      console.error("Error connecting to backend:", error);
      alert("Failed to process the image. Try again.");
    }
  }

  // Trigger file input when the button is clicked
  function handleUploadButtonClick() {
    if (fileInputRef.current) {
      fileInputRef.current.click();
    } else {
      uploadImage();
    }
  }

  return (
    <div className="container">
      <div className="sub-container">
        <h1>DevOps Chroma - Image Color Extractor</h1>
        <sub>Bring the image, we give you the colors</sub>
        
        <div className="file-contain">
          <input 
            type="file" 
            name="fileup" 
            id="fileup" 
            className="fileupload"
            ref={fileInputRef}
            onChange={handleFileChange}
            accept="image/*"
          />
        </div>
        
        <div className="">
          {showPreview && (
            <img 
              src={previewSrc} 
              alt="Preview" 
              id="preview" 
              className="preview"
              style={{ display: showPreview ? 'block' : 'none' }}
            />
          )}
          <div id="colors">
            {colors.map((color, index) => (
              <div
                key={index}
                style={{
                  backgroundColor: color.hex,
                  width: '50px',
                  height: '50px',
                  display: 'inline-block',
                  margin: '5px',
                }}
                title={`${color.name} (${color.hex}) - ${color.percentage}%`}
              />
            ))}
          </div>
        </div>
        
        <div className="btn-contain">
          <button 
            id="uploadbtn" 
            className="uploadbtn"
            onClick={uploadImage}
          >
            Upload image
          </button>
        </div>
      </div>
    </div>
  );
}

export default function App(){
  return(
    <>
    <ChromaExtractor />
    </>
  )
}