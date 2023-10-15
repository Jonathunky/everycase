import ImageGallery from "react-image-gallery";

export default function GalleryComponent({ images }) {
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
            thumbnailPosition={"top"}
            stopPropagation={true}
        />
    );
}
