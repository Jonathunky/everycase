import React, { useState, useEffect } from 'react';
import ImageGallery from "react-image-gallery";

export default function GalleryComponent({ images }) {
    const [thumbnailPosition, setThumbnailPosition] = useState("top");

    useEffect(() => {
        const handleResize = () => {
            if (window.innerWidth > 1024) {
                setThumbnailPosition("right");
            } else {
                setThumbnailPosition("top");
            }
        };

        // Initialize thumbnail position on first render
        handleResize();

        // Add event listener to window resize
        window.addEventListener("resize", handleResize);

        // Cleanup event listener on component unmount
        return () => window.removeEventListener("resize", handleResize);
    }, []);

    return (
        <ImageGallery
            items={images}
            showNav={false}
            showFullscreenButton={false}
            lazyLoad={true}
            showPlayButton={false}
            infinite={false}
            thumbnailHeight={256}
            thumbnailWidth={256}
            thumbnailPosition={thumbnailPosition}
            stopPropagation={true}
        />
    );
}
