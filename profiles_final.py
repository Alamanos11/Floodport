# -*- coding: utf-8 -*-
"""
Created on Mar-Apr 2025

@author: Angelos
"""

############  Profiles for Storm Surge #################

import numpy as np
import matplotlib.pyplot as plt

# ---------------------------
# 1. Define Zoomed Domain
# ---------------------------
# Seaward side: x from 145 to 150, representing the sea side.
x_sea_zoom = np.linspace(145, 150, 50)
z_sea_zoom = np.zeros_like(x_sea_zoom)  # initial sea level = 0 m

# Port side: x from 150 to 160, representing the engineered port floor.
x_port_zoom = np.linspace(150, 160, 50)
z_port_zoom = np.full_like(x_port_zoom, 2.0)  # port floor at 2 m

# ---------------------------
# 2. Define Sea-Level Scenarios
# ---------------------------
# These are the effective water levels for different scenarios.
mild_level = 1.18      # Mild scenario sea level (green)
moderate_level = 1.51  # Moderate scenario sea level (yellow)
extreme_level = 2.15   # Extreme scenario sea level (red)

# ---------------------------
# 3. Plot Setup
# ---------------------------
fig, ax = plt.subplots(figsize=(12, 6))

# Plot the initial sea level on the seaward side as a continuous water surface.
ax.fill_between(x_sea_zoom, z_sea_zoom, -5, color='lightblue', alpha=0.5, label="Initial Sea Level")
ax.plot(x_sea_zoom, np.full_like(x_sea_zoom, 0), 'b-', linewidth=2)

# Plot the port floor (engineered structure) on the port side.
ax.fill_between(x_port_zoom, z_port_zoom, -5, color='grey', alpha=0.9, label="Port")

# Plot sea-level scenarios:
# Mild and Moderate scenarios are below the port floor, so we draw them only on the seaward side.
ax.hlines(mild_level, xmin=145, xmax=150, colors='green', linewidth=2, label="Mild scenario sea level")
ax.hlines(moderate_level, xmin=145, xmax=150, colors='yellow', linewidth=2, label="Moderate scenario sea level")

# Extreme scenario exceeds the port floor, so it is drawn over the port region.
ax.hlines(extreme_level, xmin=145, xmax=160, colors='red', linewidth=2, label="Extreme scenario sea level")
ax.fill_between(x_port_zoom, extreme_level, z_port_zoom, color='red', alpha=0.2)

# ---------------------------
# 4. Labels and Annotations (no arrows)
# ---------------------------
ax.text(153, 1.5, "Port", fontsize=12, color="black")
ax.text(147, 0.2, "Initial Sea Level", fontsize=12, color="blue")
ax.text(146, mild_level + 0.2, "Mild", fontsize=12, color="green")
ax.text(147, moderate_level + 0.2, "Moderate", fontsize=12, color="orange")
ax.text(151, extreme_level + 0.2, "Extreme", fontsize=12, color="red")

# ---------------------------
# 5. Add Human Figures as Comparison Measures
# ---------------------------
# We'll draw a man (1.80 m tall) and a woman (1.60 m tall) on the port region.
# Their feet are at the port floor (z = 2.0 m).

# Man: placed at x = 155.
man_x = 155
man_feet = 2.0
man_height = 1.80
man_head_center = man_feet + man_height
ax.plot([man_x, man_x], [man_feet, man_feet + man_height], color='black', linewidth=2)
man_head = plt.Circle((man_x, man_feet + man_height), 0.1, color='black', fill=True)
ax.add_patch(man_head)

# Woman: placed at x = 157.
woman_x = 157
woman_feet = 2.0
woman_height = 1.60
woman_head_center = woman_feet + woman_height
ax.plot([woman_x, woman_x], [woman_feet, woman_feet + woman_height], color='black', linewidth=2)
woman_head = plt.Circle((woman_x, woman_feet + woman_height), 0.08, color='black', fill=True)
ax.add_patch(woman_head)

# ---------------------------
# 6. Final Adjustments
# ---------------------------
ax.set_xlabel("Distance (x) [m]", fontsize=12)
ax.set_ylabel("Elevation (z) [m]", fontsize=12)
ax.set_title("Profile View of Port Flooding: Storm Surge & Rainfall Scenarios", 
             fontsize=14, fontweight="bold")

# Zoom in on the desired region
ax.set_xlim(145, 160)
ax.set_ylim(-5, 5)
ax.grid(True, linestyle="--", alpha=0.5)
ax.legend(loc="lower right", fontsize=10)

# Save the Figure at 300 dpi in the specified folder.
plt.savefig(r"...\...\port_flood_surge.png", dpi=300, bbox_inches='tight')
plt.show()




####################################################################
############  Profiles for Sea-level rise, in t=100 #################
######################################################################


import numpy as np
import matplotlib.pyplot as plt

# ---------------------------
# 1. Define Zoomed Domain
# ---------------------------
# Seaward side: x from 145 to 150, representing the sea side.
x_sea_zoom = np.linspace(145, 150, 50)
z_sea_zoom = np.zeros_like(x_sea_zoom)  # initial sea level = 0 m

# Port side: x from 150 to 160, representing the engineered port floor.
x_port_zoom = np.linspace(150, 160, 50)
z_port_zoom = np.full_like(x_port_zoom, 2.0)  # port floor at 2 m

# ---------------------------
# 2. Define Sea-Level Scenarios
# ---------------------------
# These are the effective water levels for different scenarios.
mild_level = 1.5      # Mild scenario sea level (green)
moderate_level = 2  # Moderate scenario sea level (yellow)
extreme_level = 2.30   # Extreme scenario sea level (red)

# ---------------------------
# 3. Plot Setup
# ---------------------------
fig, ax = plt.subplots(figsize=(12, 6))

# Plot the initial sea level on the seaward side as a continuous water surface.
ax.fill_between(x_sea_zoom, z_sea_zoom, -5, color='lightblue', alpha=0.5, label="Initial Sea Level")
ax.plot(x_sea_zoom, np.full_like(x_sea_zoom, 0), 'b-', linewidth=2)

# Plot the port floor (engineered structure) on the port side.
ax.fill_between(x_port_zoom, z_port_zoom, -5, color='grey', alpha=0.9, label="Port")

# Plot sea-level scenarios:
# Mild and Moderate scenarios are below the port floor, so we draw them only on the seaward side.
ax.hlines(mild_level, xmin=145, xmax=150, colors='green', linewidth=2, label="Mild scenario sea level")
ax.hlines(moderate_level, xmin=145, xmax=150, colors='yellow', linewidth=2, label="Moderate scenario sea level")

# Extreme scenario exceeds the port floor, so it is drawn over the port region.
ax.hlines(extreme_level, xmin=145, xmax=160, colors='red', linewidth=2, label="Extreme scenario sea level")
ax.fill_between(x_port_zoom, extreme_level, z_port_zoom, color='red', alpha=0.2)

# ---------------------------
# 4. Labels and Annotations (no arrows)
# ---------------------------
ax.text(153, 1.5, "Port", fontsize=12, color="black")
ax.text(147, 0.2, "Initial Sea Level", fontsize=12, color="blue")
ax.text(146, mild_level + 0.15, "Mild", fontsize=12, color="green")
ax.text(147, moderate_level + 0.5, "Moderate", fontsize=12, color="orange")
ax.text(151, extreme_level + 0.3, "Extreme", fontsize=12, color="red")

# ---------------------------
# 5. Add Human Figures as Comparison Measures
# ---------------------------
# We'll draw a man (1.80 m tall) and a woman (1.60 m tall) on the port region.
# Their feet are at the port floor (z = 2.0 m).

# Man: placed at x = 155.
man_x = 155
man_feet = 2.0
man_height = 1.80
man_head_center = man_feet + man_height
ax.plot([man_x, man_x], [man_feet, man_feet + man_height], color='black', linewidth=2)
man_head = plt.Circle((man_x, man_feet + man_height), 0.1, color='black', fill=True)
ax.add_patch(man_head)

# Woman: placed at x = 157.
woman_x = 157
woman_feet = 2.0
woman_height = 1.60
woman_head_center = woman_feet + woman_height
ax.plot([woman_x, woman_x], [woman_feet, woman_feet + woman_height], color='black', linewidth=2)
woman_head = plt.Circle((woman_x, woman_feet + woman_height), 0.08, color='black', fill=True)
ax.add_patch(woman_head)

# ---------------------------
# 6. Final Adjustments
# ---------------------------
ax.set_xlabel("Distance (x) [m]", fontsize=12)
ax.set_ylabel("Elevation (z) [m]", fontsize=12)
ax.set_title("Profile View of Port Flooding: Sea-level Rise Scenarios", 
             fontsize=14, fontweight="bold")

# Zoom in on the desired region
ax.set_xlim(145, 160)
ax.set_ylim(-5, 5)
ax.grid(True, linestyle="--", alpha=0.5)
ax.legend(loc="lower right", fontsize=10)

# Save the Figure at 300 dpi in the specified folder.
plt.savefig(r"...\...\port_flood_sea.png", dpi=300, bbox_inches='tight')
plt.show()



########################################################################
###########  Profiles for Storm Surge AND Sea-level rise, in t=30 ######
########################################################################


import numpy as np
import matplotlib.pyplot as plt

# ---------------------------
# 1. Define Zoomed Domain
# ---------------------------
# Seaward side: x from 145 to 150, representing the sea side.
x_sea_zoom = np.linspace(145, 150, 50)
z_sea_zoom = np.zeros_like(x_sea_zoom)  # initial sea level = 0 m

# Port side: x from 150 to 160, representing the engineered port floor.
x_port_zoom = np.linspace(150, 160, 50)
z_port_zoom = np.full_like(x_port_zoom, 2.0)  # port floor at 2 m

# ---------------------------
# 2. Define Sea-Level Scenarios
# ---------------------------
# These are the effective water levels for different scenarios.
mild_level = 1.58      # Mild scenario sea level (green)
moderate_level = 2.06  # Moderate scenario sea level (yellow)
extreme_level = 2.79   # Extreme scenario sea level (red)

# ---------------------------
# 3. Plot Setup
# ---------------------------
fig, ax = plt.subplots(figsize=(12, 6))

# Plot the initial sea level on the seaward side as a continuous water surface.
ax.fill_between(x_sea_zoom, z_sea_zoom, -5, color='lightblue', alpha=0.5, label="Initial Sea Level")
ax.plot(x_sea_zoom, np.full_like(x_sea_zoom, 0), 'b-', linewidth=2)

# Plot the port floor (engineered structure) on the port side.
ax.fill_between(x_port_zoom, z_port_zoom, -5, color='grey', alpha=0.9, label="Port")

# Plot sea-level scenarios:
ax.hlines(mild_level, xmin=145, xmax=150, colors='green', linewidth=2, label="Mild scenario sea level")
ax.hlines(moderate_level, xmin=145, xmax=160, colors='yellow', linewidth=2, label="Moderate scenario sea level")
ax.hlines(extreme_level, xmin=145, xmax=160, colors='red', linewidth=2, label="Extreme scenario sea level")
ax.fill_between(x_port_zoom, extreme_level, z_port_zoom, color='red', alpha=0.2)

# ---------------------------
# 4. Labels and Annotations (no arrows)
# ---------------------------
ax.text(153, 1.5, "Port", fontsize=12, color="black")
ax.text(147, 0.2, "Initial Sea Level", fontsize=12, color="blue")
ax.text(146, mild_level + 0.15, "Mild", fontsize=12, color="green")
ax.text(147, moderate_level + 0.2, "Moderate", fontsize=12, color="orange")
ax.text(151, extreme_level + 0.3, "Extreme", fontsize=12, color="red")

# ---------------------------
# 5. Add Human Figures as Comparison Measures
# ---------------------------
# A man (1.80 m tall) and a woman (1.60 m tall) on the port region, to compare the heights.
# Their feet are at the port floor (z = 2.0 m).

# Man: placed at x = 155.
man_x = 155
man_feet = 2.0
man_height = 1.80
man_head_center = man_feet + man_height
ax.plot([man_x, man_x], [man_feet, man_feet + man_height], color='black', linewidth=2)
man_head = plt.Circle((man_x, man_feet + man_height), 0.1, color='black', fill=True)
ax.add_patch(man_head)

# Woman: placed at x = 157.
woman_x = 157
woman_feet = 2.0
woman_height = 1.60
woman_head_center = woman_feet + woman_height
ax.plot([woman_x, woman_x], [woman_feet, woman_feet + woman_height], color='black', linewidth=2)
woman_head = plt.Circle((woman_x, woman_feet + woman_height), 0.08, color='black', fill=True)
ax.add_patch(woman_head)

# ---------------------------
# 6. Final Adjustments
# ---------------------------
ax.set_xlabel("Distance (x) [m]", fontsize=12)
ax.set_ylabel("Elevation (z) [m]", fontsize=12)
ax.set_title("Profile View of Port Flooding: Sea-level Rise Scenarios", 
             fontsize=14, fontweight="bold")

# Zoom in on the desired region
ax.set_xlim(145, 160)
ax.set_ylim(-5, 5)
ax.grid(True, linestyle="--", alpha=0.5)
ax.legend(loc="lower right", fontsize=10)

# Save the Figure at 300 dpi in the specified folder.
plt.savefig(r"...\...\port_flood_comb.png", dpi=300, bbox_inches='tight')
plt.show()

