# Google Places API Setup Guide

## Overview
This guide explains how to integrate the Google Places API to find real nearby doctors and clinics based on user location.

## Current Implementation
Currently, the application returns **mock data** for demonstration purposes. To use real location data, you need to integrate with Google Places API.

## Steps to Enable Real Location Search

### 1. Get a Google Maps API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the following APIs:
   - **Places API**
   - **Maps JavaScript API** (optional, for map display)
   - **Geocoding API** (optional, for address validation)
4. Go to "Credentials" and create an API key
5. Restrict your API key:
   - Set application restrictions (HTTP referrers for web)
   - Set API restrictions (only enable Places API)

### 2. Install Required Package

Add the `requests` library to your requirements.txt:

```bash
pip install requests
```

Update `requirements.txt`:
```
Flask==2.3.2
scikit-learn==1.3.0
pandas==2.0.3
numpy==1.24.3
Werkzeug==2.3.6
requests==2.31.0
```

### 3. Update the Backend Code

In `main.py`, replace the `/find-doctors` route with this implementation:

```python
import requests
import os

# Add this near the top of your file, after imports
GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY', 'YOUR_API_KEY_HERE')

@app.route('/find-doctors', methods=['POST'])
def find_doctors():
    """
    Endpoint to find nearby doctors/clinics based on user's location
    Uses Google Places API
    """
    try:
        data = request.get_json()
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        
        if not latitude or not longitude:
            return jsonify({'error': 'Location coordinates are required'}), 400
        
        # Google Places API - Nearby Search
        url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
        
        params = {
            'location': f'{latitude},{longitude}',
            'radius': 5000,  # Search within 5km radius
            'type': 'doctor',  # You can also use: hospital, health, pharmacy
            'key': GOOGLE_MAPS_API_KEY
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code != 200:
            return jsonify({'error': 'Failed to fetch data from Google Places API'}), 500
        
        places_data = response.json()
        
        if places_data.get('status') != 'OK':
            return jsonify({'error': f"API Error: {places_data.get('status')}"}), 500
        
        doctors = []
        
        for place in places_data.get('results', [])[:10]:  # Limit to 10 results
            # Get additional details for each place (to get phone number)
            place_id = place.get('place_id')
            details_url = 'https://maps.googleapis.com/maps/api/place/details/json'
            details_params = {
                'place_id': place_id,
                'fields': 'name,formatted_address,formatted_phone_number,rating,opening_hours,types',
                'key': GOOGLE_MAPS_API_KEY
            }
            
            details_response = requests.get(details_url, params=details_params)
            details = details_response.json().get('result', {})
            
            # Calculate distance (approximate)
            lat1, lon1 = latitude, longitude
            lat2 = place['geometry']['location']['lat']
            lon2 = place['geometry']['location']['lng']
            distance_km = calculate_distance(lat1, lon1, lat2, lon2)
            
            doctor_info = {
                'name': place.get('name', 'Unknown'),
                'address': details.get('formatted_address', place.get('vicinity', 'Address not available')),
                'phone': details.get('formatted_phone_number', 'Phone not available'),
                'rating': place.get('rating', 0),
                'distance': f'{distance_km:.1f} km',
                'type': 'Hospital' if 'hospital' in place.get('types', []) else 'Clinic',
                'open_now': place.get('opening_hours', {}).get('open_now', False) if 'opening_hours' in place else None
            }
            
            doctors.append(doctor_info)
        
        return jsonify({
            'success': True,
            'doctors': doctors,
            'location': {
                'latitude': latitude,
                'longitude': longitude
            }
        })
        
    except Exception as e:
        print(f"Error finding doctors: {e}")
        return jsonify({'error': 'An error occurred while searching for doctors'}), 500


def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate distance between two coordinates using Haversine formula
    Returns distance in kilometers
    """
    from math import radians, sin, cos, sqrt, atan2
    
    R = 6371  # Earth's radius in kilometers
    
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    
    return R * c
```

### 4. Set Environment Variable

**For Development:**

Windows (PowerShell):
```powershell
$env:GOOGLE_MAPS_API_KEY="your_actual_api_key_here"
```

Windows (CMD):
```cmd
set GOOGLE_MAPS_API_KEY=your_actual_api_key_here
```

Linux/Mac:
```bash
export GOOGLE_MAPS_API_KEY="your_actual_api_key_here"
```

**For Production:**
- Add the API key to your hosting platform's environment variables
- Never commit your API key to version control
- Use a `.env` file with `python-dotenv` package

### 5. Search Types You Can Use

You can modify the `type` parameter to search for different healthcare facilities:

- `doctor` - Medical doctors and clinics
- `hospital` - Hospitals
- `pharmacy` - Pharmacies
- `dentist` - Dental clinics
- `physiotherapist` - Physical therapy centers
- `health` - General health facilities

### 6. Enhance the Search

You can add filters and sorting:

```python
# Sort by distance
doctors.sort(key=lambda x: float(x['distance'].replace(' km', '')))

# Filter only open now
params['opennow'] = True  # Add to API params

# Search multiple types
for type_name in ['doctor', 'hospital']:
    params['type'] = type_name
    response = requests.get(url, params=params)
    # Process results...
```

## Cost Considerations

Google Places API pricing (as of 2024):
- Nearby Search: $32 per 1000 requests
- Place Details: $17 per 1000 requests
- You get $200 free credit monthly

**Optimization tips:**
- Cache results for same locations
- Limit the number of detail requests
- Use radius wisely
- Consider alternative APIs (Bing Maps, MapQuest) for cost savings

## Alternative: OpenStreetMap (Free)

For a free alternative, use Nominatim API with OpenStreetMap:

```python
import requests

def find_doctors_osm(latitude, longitude):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        'format': 'json',
        'q': 'hospital,clinic,doctor',
        'lat': latitude,
        'lon': longitude,
        'radius': 5000,
        'limit': 10
    }
    headers = {
        'User-Agent': 'MediRecommend/1.0'  # Required by OSM
    }
    response = requests.get(url, params=params, headers=headers)
    return response.json()
```

## Security Best Practices

1. **Never expose your API key in frontend code**
2. **Use environment variables**
3. **Implement rate limiting** to prevent abuse
4. **Restrict API key** to specific domains/IPs
5. **Monitor usage** in Google Cloud Console

## Testing

To test the implementation:

1. Enable HTTPS (required for geolocation in production)
2. Allow location access in browser
3. Check browser console for any errors
4. Verify API calls in Network tab
5. Check Google Cloud Console for API usage

## Troubleshooting

**Location not working:**
- Enable location services in browser
- Use HTTPS (required for geolocation API)
- Check browser permissions

**API errors:**
- Verify API key is correct
- Check if APIs are enabled in Google Cloud
- Ensure billing is set up (even for free tier)
- Check API key restrictions

**No results:**
- Increase search radius
- Try different search types
- Check if location is valid

## Support

For issues with:
- Google Places API: [Google Maps Platform Support](https://developers.google.com/maps/support)
- Geolocation API: [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/API/Geolocation_API)
