export type Coordinates = {
  lat: number
  lng: number
}

export const getCurrentLocation = (): Promise<Coordinates> => {
  return new Promise((resolve) => {
    if (!navigator.geolocation) {
      resolve({ lat: 28.6139, lng: 77.209 })
      return
    }

    navigator.geolocation.getCurrentPosition(
      (position) => {
        resolve({
          lat: position.coords.latitude,
          lng: position.coords.longitude,
        })
      },
      () => resolve({ lat: 28.6139, lng: 77.209 }),
      { enableHighAccuracy: false, timeout: 6000, maximumAge: 60000 }
    )
  })
}
