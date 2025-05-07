const fileInput = document.querySelector("input[type=file]");
const encodeBtn = document.getElementById("encodeBtn");
const decodeBtn = document.getElementById("decodeBtn");
const canvas = document.createElement("canvas");
const ctx = canvas.getContext("2d");
document.body.appendChild(canvas);

let morseData = "";

// Load image and draw on canvas
fileInput.addEventListener("change", function (event) {
    const file = event.target.files[0];
    if (file) {
        console.log("File selected:", file.name);
        const img = new Image();
        img.src = URL.createObjectURL(file);
        img.onload = () => {
            canvas.width = img.width / 4;  // Reduce size for faster processing
            canvas.height = img.height / 4;
            ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
            console.log("Image loaded successfully");
        };
    } else {
        console.log("No file selected");
    }
});

// Convert image to Morse Code
encodeBtn.addEventListener("click", function () {
    console.log("Encoding started...");
    morseData = "";  // Reset morse data
    const imgData = ctx.getImageData(0, 0, canvas.width, canvas.height).data;

    for (let i = 0; i < imgData.length; i += 4) {
        const brightness = (imgData[i] + imgData[i + 1] + imgData[i + 2]) / 3;
        morseData += brightness < 128 ? "." : "-";  // Dark = dot, Light = dash
    }

    console.log("Encoded Morse:", morseData);
    alert("Encoding complete! Check console.");
});

// Decode Morse Code back to an image
decodeBtn.addEventListener("click", function () {
    console.log("Decoding started...");
    if (!morseData) {
        alert("No encoded data available!");
        return;
    }

    const decodedImage = ctx.createImageData(canvas.width, canvas.height);
    let index = 0;

    for (let i = 0; i < decodedImage.data.length; i += 4) {
        const color = morseData[index++] === "." ? 0 : 255;
        decodedImage.data[i] = color;   // R
        decodedImage.data[i + 1] = color; // G
        decodedImage.data[i + 2] = color; // B
        decodedImage.data[i + 3] = 255; // Alpha
    }

    ctx.putImageData(decodedImage, 0, 0);
    console.log("Decoding complete!");
});
