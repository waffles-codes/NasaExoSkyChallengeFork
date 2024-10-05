import astropy.units as u
from astropy.coordinates import SkyCoord
from astroquery.gaia import Gaia
import json

# Define a region around a chosen RA/Dec (for example, around RA=280, Dec=-60)
coord = SkyCoord(ra=280, dec=-60, unit=(u.degree, u.degree), frame='icrs')
width = u.Quantity(0.1, u.deg)  # width of the region in degrees
height = u.Quantity(0.1, u.deg)  # height of the region in degrees

# Query Gaia DR3 for stars in this region
r = Gaia.query_object_async(coordinate=coord, width=width, height=height)

# Extract relevant columns: RA, Dec, brightness (phot_g_mean_mag), color index (bp_rp)
stars = []
for row in r:
    stars.append({
        "ra": float(row['ra']),  # Right Ascension
        "dec": float(row['dec']),  # Declination
        "brightness": float(row['phot_g_mean_mag']),  # Brightness
        "color_index": float(row['bp_rp']),  # Color index (approximation of color)
    })

# Save the data to a JSON file
with open('stars.json', 'w') as f:
    json.dump(stars, f, indent=2)
    
print(f"{len(stars)} stars saved to 'stars.json'")
