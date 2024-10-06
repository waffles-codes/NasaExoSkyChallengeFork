import React, { useEffect, useRef, useState } from 'react';
import { Canvas, Circle } from 'fabric';

const ExoSkyCanvas = () => {
    const canvasRef = useRef(null); // Reference to the canvas
    const fabricCanvas = useRef(null); // Keep a reference to the Fabric.js canvas
    const isDrawing = useRef(false);

    // State for drawing color and eraser mode
    const [color, setColor] = useState('red');
    const [isErasing, setIsErasing] = useState(false);
    const [brushSize, setBrushSize] = useState(5); // Default brush size

    // Refs for current color and eraser state
    const colorRef = useRef(color);
    const isErasingRef = useRef(isErasing);
    const brushSizeRef = useRef(brushSize);

    // Update refs when color, eraser state, or brush size changes
    useEffect(() => {
        colorRef.current = color;
        isErasingRef.current = isErasing;
        brushSizeRef.current = brushSize;
    }, [color, isErasing, brushSize]);

    // Initialize the Fabric.js canvas
    useEffect(() => {
        fabricCanvas.current = new Canvas(canvasRef.current, {
            width: window.innerWidth,
            height: window.innerHeight,
            selection: false
        });

        const handleMouseDown = (event) => {
            isDrawing.current = true; // Start drawing
        };

        const handleMouseMove = (event) => {
            if (!isDrawing.current) return; // If not drawing, do nothing

            const pointer = fabricCanvas.current.getPointer(event.e);
            const strokeColor = isErasingRef.current ? null : colorRef.current; // Use null for erasing

            if (isErasingRef.current) {
                // Find the object under the pointer and remove it
                const targetObject = fabricCanvas.current.findTarget(event.e);
                if (targetObject) {
                    fabricCanvas.current.remove(targetObject);
                }
            } else {
                // Draw a circle at the current pointer position with the current brush size
                const circle = new Circle({
                    left: pointer.x,
                    top: pointer.y,
                    radius: brushSizeRef.current, // Use the current brush size
                    fill: strokeColor,
                    selectable: false, // Prevents the circle from being selected
                });

                fabricCanvas.current.add(circle); // Add the circle to the canvas
            }
        };


        const handleMouseUp = () => {
            isDrawing.current = false; // Stop drawing
            fabricCanvas.current.renderAll(); // Refresh the canvas to show the new circle
        };

        // Add event listeners to the canvas
        fabricCanvas.current.on('mouse:down', handleMouseDown);
        fabricCanvas.current.on('mouse:move', handleMouseMove);
        fabricCanvas.current.on('mouse:up', handleMouseUp);

        // Clean up event listeners and dispose of the canvas on unmount
        return () => {
            fabricCanvas.current.off('mouse:down', handleMouseDown);
            fabricCanvas.current.off('mouse:move', handleMouseMove);
            fabricCanvas.current.off('mouse:up', handleMouseUp);
            fabricCanvas.current.dispose(); // Dispose of the canvas instance
        };
    }, []); // Run only once when the component mounts

    // Function to export the canvas as a PNG
    const exportCanvas = () => {
        const dataURL = fabricCanvas.current.toDataURL({
            format: 'png',
            quality: 1.0 // Set quality (1.0 = best quality)
        });

        // Create a link element
        const link = document.createElement('a');
        link.href = dataURL;
        link.download = 'exosky_canvas.png'; // Set a default file name

        // Trigger the download
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    };

    return (
        <div>
            <div>
                {/* Color palette */}
                {['yellow', 'red', 'green', 'blue'].map((color) => (
                    <button
                        key={color}
                        onClick={() => setColor(color)}
                        style={{backgroundColor: color, width: '30px', height: '30px'}}
                    ></button>
                ))}
                <button onClick={() => setIsErasing(!isErasing)} style={{backgroundColor: 'gray'}}>
                    {isErasing ? 'Use Pen' : 'Use Eraser'}
                </button>
                <div>
                    {/* Brush size slider */}
                    <label htmlFor="brushSize">Brush Size: {brushSize}</label>
                    <input
                        id="brushSize"
                        type="range"
                        min="1"
                        max="10" // Adjust the max size as needed
                        value={brushSize}
                        onChange={(e) => setBrushSize(e.target.value)}
                    />
                </div>
                <button onClick={exportCanvas}>Export as PNG</button>
            </div>
            <canvas ref={canvasRef} style={{border: '1px solid black', width: '100%', height: '100%'}}/>
        </div>
    );
};

export default ExoSkyCanvas;


// import React from 'react';
//
// const EmbeddedPaint = () => {
//     return (
//         <iframe
//             title="Embedded Paint Tool"
//             src="https://sketch.io/sketchpad/"
//             style={{ width: '100%', height: '100vh', border: 'none' }}
//         />
//     );
// };
//
// export default EmbeddedPaint;