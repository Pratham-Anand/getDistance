# Distance Calculation API

This project provides a Django-based API to calculate the distance between two cities using city names. It uses the **OpenCage Geocoding API** to convert city names into geographical coordinates and the **OpenRouteService API** to compute the distance between these coordinates. The distance is returned in miles.

## APIs Used

- **OpenCage Geocoding API**: Used to convert city names into latitude and longitude coordinates.
- **OpenRouteService API**: Used to calculate the driving distance between two sets of coordinates.

## Endpoints

### `POST /api/distance/`

Calculates the distance between two cities based on the source and destination city names provided in the request body.

#### Request Body

```json
{
  "source_city": "New York",
  "destination_city": "Los Angeles"
}
