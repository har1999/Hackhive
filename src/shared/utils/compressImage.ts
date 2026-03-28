import imageCompression from 'browser-image-compression'

export const compressJobPhoto = async (file: File) => {
  return imageCompression(file, {
    maxSizeMB: 0.1,
    maxWidthOrHeight: 1024,
    useWebWorker: true,
    fileType: 'image/webp',
  })
}
