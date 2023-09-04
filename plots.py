#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt

# Constants
OXYGEN_MASS_AMU = 16.0
OXYGEN2_MASS_AMU = 32.0
NITROGEN2_MASS_AMU = 28.0

# Initialize temperature as a function of altitude
def initialize_temperature(altitude_km):
    temperature_kelvin = 200 + 600 * np.tanh((altitude_km - 100) / 100.0)
    return temperature_kelvin

# Update the state
def update_state(old_state, temperature_rate, time_step):
    new_state = {}
    # Update state here
    return new_state
  
# Plotting functions
def plot_spectrum(wavelengths_in_m, intensities, filename):
    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(111)

    ax.scatter(wavelengths_in_m * 1e10, intensities)
    ax.set_xlabel('Wavelength (A)')
    ax.set_ylabel('Intensity (photons/m2/s)')

    fig.savefig(filename)
    plt.close()

def plot_value_vs_altitude(altitudes, values, filename, var_name, is_log=False):
    fig = plt.figure(figsize=(5, 10))
    ax = fig.add_subplot(111)

    ax.plot(values, altitudes)
    ax.set_xlabel(var_name)
    ax.set_ylabel('Altitude (km)')
    if (is_log):
        ax.set_xscale('log')

    fig.savefig(filename)
    plt.close()

# Main Code
if __name__ == '__main__':

    # Set solar activity parameters
    f107 = 100.0
    f107a = 100.0

    # Solar zenith angle and heating efficiency
    solar_zenith_angle_deg = 0.0
    efficiency = 0.3
    
    # Boundary conditions for densities
    density_oxygen_bc = 5.0e17  # /m3
    density_oxygen2_bc = 4.0e18  # /m3
    density_nitrogen2_bc = 1.7e19  # /m3

    # Read EUV data from CSV file
    euv_file = 'euv_37.csv'
    euv_data = read_euv_csv_file(euv_file)

    # Initialize altitudes
    num_altitudes = 41
    altitudes = np.linspace(100, 500, num=num_altitudes)

    # Initialize temperature profile
    temperatures = initialize_temperature(altitudes)

    # Compute scale height
    scale_height_oxygen = calculate_scale_height(OXYGEN_MASS_AMU, altitudes, temperatures)

    # Calculate EUVAC intensity
    intensity_at_infinity = calculate_solar_intensity(euv_data['f74113'], euv_data['afac'], f107, f107a)

    # Calculate mean wavelength
    mean_wavelength = (euv_data['short'] + euv_data['long']) / 2

    # Calculate energies
    energies = convert_wavelength_to_joules(mean_wavelength)

    # Calculate initial oxygen density
    density_oxygen = calculate_hydrostatic(density_oxygen_bc, scale_height_oxygen, temperatures, altitudes)
    # Calculate densities for nitrogen and oxygen2...

    # Plot initial oxygen density
    plot_value_vs_altitude(altitudes, density_oxygen, 'oxygen_density_initial.png', '[O] (/m3)', is_log=True)

    # Calculate Tau for oxygen
    tau_oxygen = calculate_tau(solar_zenith_angle_deg, density_oxygen, scale_height_oxygen, euv_data['ocross'])
    # Calculate Tau for nitrogen and oxygen2, and combine...
    # Repeat for all wavelengths...
    tau = tau_oxygen  # + ...

    # Plot Tau
    plot_value_vs_altitude(altitudes, tau_oxygen[5], 'tau_oxygen.png', 'Tau ()')

    # Calculate EUV heating for oxygen
    heating_oxygen = calculate_Qeuv(density_oxygen, intensity_at_infinity, tau, euv_data['ocross'], energies, efficiency)
    # Calculate heating for nitrogen and oxygen2, and combine...
    # Repeat for all wavelengths...
    heating = heating_oxygen  # + ...

    # Plot oxygen heating
    plot_value_vs_altitude(altitudes, heating_oxygen, 'oxygen_heating.png', 'Qeuv - O (W/m3)')
    
    # Calculate real mass density (include N2 and O2)
    mass_density = calculate_mass_density(density_oxygen, OXYGEN_MASS_AMU)

    # Calculate specific heat capacity
    specific_heat_capacity = calculate_specific_heat_capacity()

    # Calculate temperature rate change
    temperature_rate_change = convert_heating_to_temperature_rate(heating, mass_density, specific_heat_capacity)

    # Plot temperature rate change
    plot_value_vs_altitude(altitudes, temperature_rate_change * 86400, 'temperature_rate_change.png', 'dT/dt (K/day)')
