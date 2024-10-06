import numpy as np
import plotly.graph_objects as go
from astropy.coordinates import SkyCoord
from astropy import units as u
from astroquery.gaia import Gaia
from scipy.stats import linregress

import requests

from skyfield.api import Star

# Query Gaia data
ra_center = 280
dec_center = -60

coord = SkyCoord(ra_center, dec_center, unit=(u.degree, u.degree))
width = u.Quantity(0.1, u.deg)
height = u.Quantity(0.1, u.deg)
r = Gaia.query_object_async(coordinate=coord, width=width, height=height)

# Extract relevant columns
ra = r['ra']
dec = r['dec']
distance = r['dist']

#ORIGINAL CORDS -> SHITED CORDS
def spherical_to_cartesian(ra, dec, distance):
    ra_rad = np.radians(ra)
    dec_rad = np.radians(dec)
    
    x = distance * np.cos(dec_rad) * np.cos(ra_rad)
    y = distance * np.cos(dec_rad) * np.sin(ra_rad)
    z = distance * np.sin(dec_rad)

    return np.array([x, y, z])

def cartesian_to_spherical(x, y, z):
    distance = np.sqrt(x**2 + y**2 + z**2)
    ra_rad = np.arctan2(y, x)
    dec_rad = np.arcsin(z / distance)
    
    ra = np.degrees(ra_rad)
    dec = np.degrees(dec_rad)
    
    #RA is in the range [0, 360]
    if ra < 0:
        ra += 360
        
    return ra, dec, distance


def rotation_matrix_z(angle_deg):
    angle_rad = np.radians(angle_deg)
    return np.array([
        [np.cos(angle_rad), -np.sin(angle_rad), 0],
        [np.sin(angle_rad), np.cos(angle_rad), 0],
        [0, 0, 1]
    ])


def rotation_matrix_y(angle_deg):
    angle_rad = np.radians(angle_deg)
    return np.array([
        [np.cos(angle_rad), 0, np.sin(angle_rad)],
        [0, 1, 0],
        [-np.sin(angle_rad), 0, np.cos(angle_rad)]
    ])

def transform_coordinates(ra, dec, distance, delta_ra, delta_dec):

    # Convert spherical coordinates to Cartesian
    star_cartesian = spherical_to_cartesian(ra, dec, distance)
    
    # Rotation matrix to align the new frame to the original frame
    Rz = rotation_matrix_z(-delta_ra)  # Negative to reverse the RA shift
    Ry = rotation_matrix_y(-delta_dec)  # Negative to reverse the Dec shift
    
    # Apply the rotation matrices (Y then Z)
    rotation_matrix = Rz @ Ry
    original_cartesian = rotation_matrix @ star_cartesian
    
    # Convert back to spherical coordinates
    return cartesian_to_spherical(*original_cartesian)


def ra_to_hms(ra_deg):
    """
    Convert Right Ascension from degrees to the format hh:mm:ss.s.
    """
    # Convert RA from degrees to hours (1 hour = 15 degrees)
    ra_hours = ra_deg / 15.0

    hours = int(ra_hours)
    minutes = int((ra_hours - hours) * 60)
    seconds = (ra_hours - hours - minutes / 60) * 3600

    return [hours, minutes, seconds]

def dec_to_dms(dec_deg):
    """
    Convert Declination from degrees to the format ±dd°mm'ss.s".
    """
    # Get the sign for declination (positive or negative)
    
    
    # Work with the absolute value for conversion
    dec_deg = abs(dec_deg)

    degrees = int(dec_deg)
    if dec_deg <= 0:
        degrees = degrees*-1
    minutes = int((dec_deg - degrees) * 60)
    
        
    seconds = (dec_deg - degrees - minutes / 60) * 3600

    return [degrees, minutes, seconds]



ra_new = 45.0  # in degrees
dec_new = 30.0  # in degrees
distance_new = 100.0

# Frame shift (how much the new frame is offset in RA and Dec relative to original)
delta_ra = ra_center  # in degrees
delta_dec = dec_center  # in degrees
APIcords = []

# Transform the coordinates back to the original frame

for i in range(len(r['ra'])):
    #right assection, decinlation, and distance
    ra_orig, dec_orig, distance_orig = transform_coordinates(r['ra'][i], r['dec'][i], r['dist'][i], delta_ra, delta_dec)
    ra_orig = ra_to_hms(ra_orig)
    dec_orig = dec_to_dms(dec_orig)
    temp = [ra_orig, dec_orig, distance_orig]
    APIcords.append(temp)


barnard = Star(ra_hours=(APIcords[0][0]), dec_degrees=(APIcords[0][1]))

print(barnard)



