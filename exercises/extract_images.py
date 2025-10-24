#!/usr/bin/env python3
"""
Extract images from PDF file and save them to images directory.
"""

import fitz  # PyMuPDF
import os
from PIL import Image
import io

def extract_images_from_pdf(pdf_path, output_dir):
    """
    Extract all images from a PDF file and save them to the specified directory.
    
    Args:
        pdf_path (str): Path to the PDF file
        output_dir (str): Directory to save extracted images
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    
    image_count = 0
    
    print(f"Processing PDF: {pdf_path}")
    print(f"Total pages: {len(pdf_document)}")
    
    # Iterate through each page
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        print(f"Processing page {page_num + 1}...")
        
        # Get list of images on the page
        image_list = page.get_images()
        
        # Extract each image
        for img_index, img in enumerate(image_list):
            # Get image data
            xref = img[0]
            pix = fitz.Pixmap(pdf_document, xref)
            
            # Skip if image is a mask or has no data
            if pix.n - pix.alpha < 3:  # GRAY or B/W
                if pix.n == pix.alpha:  # if it's just an alpha channel
                    pix = None
                    continue
                    
            image_count += 1
            
            # Generate filename
            if pix.n - pix.alpha == 1:  # Grayscale
                filename = f"image_{image_count:03d}_page_{page_num + 1:02d}.png"
            else:  # RGB
                filename = f"image_{image_count:03d}_page_{page_num + 1:02d}.png"
            
            filepath = os.path.join(output_dir, filename)
            
            # Save the image
            if pix.n - pix.alpha == 1:  # Grayscale
                pix.save(filepath)
            else:  # RGB
                pix.save(filepath)
            
            print(f"  Extracted: {filename} ({pix.width}x{pix.height})")
            
            # Clean up
            pix = None
    
    # Close the PDF
    pdf_document.close()
    
    print(f"\nExtraction completed!")
    print(f"Total images extracted: {image_count}")
    print(f"Images saved to: {output_dir}")
    
    return image_count

if __name__ == "__main__":
    # Define paths
    pdf_file = "TechEd2025_ETDc_Hands-on Script.pdf"
    images_dir = "images"
    
    # Check if PDF file exists
    if not os.path.exists(pdf_file):
        print(f"Error: PDF file '{pdf_file}' not found!")
        exit(1)
    
    # Extract images
    try:
        total_images = extract_images_from_pdf(pdf_file, images_dir)
        
        if total_images == 0:
            print("No images found in the PDF file.")
        else:
            print(f"\nSuccess! Extracted {total_images} images from the PDF.")
            
    except Exception as e:
        print(f"Error extracting images: {str(e)}")
        exit(1)
