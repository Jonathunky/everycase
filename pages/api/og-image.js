import sharp from "sharp";
import axios from "axios";
import { supabase } from "/components/supabaseClient";

export default async function handler(req, res) {
  const { page } = req.query;

  console.log("Request received. Page:", page); // Log the page parameter

  if (!page) {
    console.error("Error: Page path is required");
    return res.status(400).send("Page path is required");
  }

  try {

    const model = page
      .split("/")
      .slice(1) // Ignore the leading empty string from the slash
      .join(" ") // Join remaining segments with spaces
      .toLowerCase(); // Convert to lowercase
    console.log("Extracted Model:", model);

    // Query the database for SKUs
    const { data: cases, error } = await supabase
      .from("skus")
      .select("SKU")
      .ilike("model", `%${model}%`);

    if (error) {
      console.error("Error fetching SKUs:", error);
      return res.status(500).send("Error fetching SKUs");
    }

    if (!cases || cases.length < 4) {
      return res.status(400).send("Not enough SKUs available for this model");
    }

    // Randomly select four SKUs
    const selectedCases = cases
      .sort(() => 0.5 - Math.random())
      .slice(0, 4)
      .map((item) => `https://cloudfront.everycase.org/everysource/${item.SKU}.webp`);

    console.log("Selected SKUs:", selectedCases);


    const images = await Promise.all(
      selectedCases.map(async (url) => {
        const response = await axios.get(url, { responseType: "arraybuffer" }); // Fetch image
        return sharp(Buffer.from(response.data)).toBuffer(); // Resize and buffer
      })
    );

    console.log("Images successfully fetched and processed"); // Log success in fetching images

    const processedImages = await Promise.all([
      sharp(images[0])
        .resize(800, 800)
        .rotate(-30 - 180, { background: { r: 0, g: 0, b: 0, alpha: 0 } }) // Preserve transparency
        .toBuffer(),
      sharp(images[1])
        .resize(800, 800)
        .rotate(60 - 180, { background: { r: 0, g: 0, b: 0, alpha: 0 } }) // Preserve transparency
        .toBuffer(),
      sharp(images[2])
        .resize(800, 800)
        .rotate(-30 - 270, { background: { r: 0, g: 0, b: 0, alpha: 0 } }) // Preserve transparency
        .toBuffer(),
      sharp(images[3])
        .resize(800, 800)
        .rotate(-30, { background: { r: 0, g: 0, b: 0, alpha: 0 } }) // Preserve transparency
        .toBuffer()
    ]);

    const positions = [
      { input: processedImages[0], left: 360, top: 130 },   // Top left
      { input: processedImages[1], left: 1000, top: 170 }, // Top right
      { input: processedImages[2], left: 80, top: 700 },   // Bottom left
      { input: processedImages[3], left: 720, top: 740 } // Bottom right
    ];

    // Generate the composite image
    const compositeImage = await sharp({
      create: {
        width: 2000, // almost image width
        height: 2000, // almost image height
        channels: 3,
        background: { r: 255, g: 255, b: 240 } // White background
      }
    })
      .composite(positions)
      .png({ quality: 100 })
      .toBuffer();

    const croppedImage = await sharp(compositeImage)
      .extract({
        left: Math.max(0, (2000 - 1200) / 2), // Center the crop horizontally
        top: Math.max(0, (2000 - 630) / 2),   // Center the crop vertically
        width: 1200,
        height: 630
      })
      .toFormat("png")
      .toBuffer();

    console.log("Composite image successfully generated"); // Log success

    // Serve the generated image
    res.setHeader("Content-Type", "image/png");
    res.send(croppedImage);
  } catch (err) {
    console.error("Unhandled error:", err); // Log any unhandled errors
    res.status(500).send("Error generating image");
  }
}