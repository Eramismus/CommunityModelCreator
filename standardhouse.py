import math

from teaser.logic.buildingobjects.buildingphysics.rooftop import Rooftop
from teaser.logic.buildingobjects.buildingphysics.layer import Layer
from teaser.logic.buildingobjects.buildingphysics.material import Material
from teaser.logic.buildingobjects.buildingphysics.outerwall import OuterWall
from teaser.logic.buildingobjects.buildingphysics.innerwall import InnerWall
from teaser.logic.buildingobjects.buildingphysics.groundfloor import GroundFloor
from teaser.logic.buildingobjects.buildingphysics.floor import Floor
from teaser.logic.buildingobjects.buildingphysics.window import Window
from teaser.logic.buildingobjects.thermalzone import ThermalZone
from teaser.logic.buildingobjects.boundaryconditions.boundaryconditions \
			import BoundaryConditions

from teaser.logic.buildingobjects.building import Building

# Dictionary for materials, data from Allen and Pinney, check values for air

# materials 
#{name: [density, heat capacity, thermal conductance, emissivity, absorptivity]}
			
Mat_dict = {"Plaster": [800, 0.840, 0.26, 0.91, 0.50], 
	"Plasterboard": [950, 0.840, 0.16, 0.91, 0.50], 
	"Brick_in": [1700, 0.800, 0.62, 0.93, 0.70],
	"Brick_out": [1700, 0.8, 0.84, 0.90, 0.93],
	"Cavity": [1.276, 1.006, 0.065/0.18, 0, 0], # R is 0.18 for airspaces acc. CIBSE Guide A
	"Glass_fibre": [250, 0.840, 0.04, 0.90, 0.30],
	"Insulation": [12, 0.840, 0.040, 0.90,0.30],
	"Timber": [650, 1.2, 0.14, 0.91, 0.65],
	"Carpet": [160, 1, 0.06, 0.90, 0.65],
	"Roof_tile": [1900, 0.8, 0.84, 0.90, 0.60],
	"Earth": [1900, 1.7, 1.4, 0.90, 0.85],
	"Concrete": [2100, 0.840, 1.40, 0.90, 0.65],
	"Softwood": [230, 2.760, 0.12, 0.90, 0.65],
	"GlasWindow": [2500, 0.750, 1.05, 0.90, 0.20],
	"ConcreteBlock": [1400, 1.0, 0.510, 0.90, 0.65],
	"ConcreteWallPanel": [1200, 1.0, 0.380, 0.90, 0.65],
	"ConcreteFloorPanel": [2000, 1.0, 1.13, 0.90, 0.65],
	"Screed": [1200, 0.840, 0.410, 0.91, 0.65],
	"ConcreteWaffle": [2000, 1.0, 1.13, 0.90, 0.65],
	"AluminiumSheet": [2700, 0.880, 210, 0.22, 0.20],
	"TimberPanel": [650, 1.2, 0.14, 0.91, 0.65],
	"CeramicTiles": [1900, 0.8, 0.84, 0.90, 0.60],
	"PortlandStone": [2200, 0.712, 1.83, 0.90, 0.60]
	}

def create_stand_dwelling(prj, build_id, type, scaler):
	
	# Data and values based on Allen and Pinney 1990, BEPAC, A Set of Standard Dwelling

	bldg = Building(parent=prj)
	bldg.name = build_id
	bldg.street_name = "StandardClose"
	bldg.city = "StandardTown"
	
	if type == "detached":
		print("Creating a detached house")
	
		bldg.year_of_construction = 1950
		bldg.number_of_floors = 2
		bldg.height_of_floors = 2.5

		# Instantiate a ThermalZone class and set the Building as a parent of it.
		# Set some parameters of the thermal zone. Be careful: Dymola does not
		# like whitespaces in  names and filenames, thus we will delete them
		# anyway in TEASER.

		tz = ThermalZone(parent=bldg)
		tz.name = "House"
		tz.area = scaler[1]*(19.05+13.14+7.71+10.05)
		tz.volume = tz.area * bldg.number_of_floors * bldg.height_of_floors
		tz.infiltration_rate = 0.7

		# Instantiate BoundaryConditions and load conditions for `Living`.
		tz.use_conditions = BoundaryConditions(parent=tz)
		tz.use_conditions.load_use_conditions("Living", prj.data)

		# Define two building elements reflecting a pitched roof (south = 180 and
		# north = 0). Setting the the ThermalZone as a parent will automatically
		# assign this element to the thermal zone. We also set names, tilt and
		# coefficients for heat transfer on the inner and outer side of the
		# roofs. If the building has a flat roof, please use -1 as
		# orientation. Please read the docs to get more information on these
		# parameters.

		
		# To define the wall constructions we need to instantiate Layer and
		# Material objects and set attributes. id indicates the order of wall
		# construction from inside to outside (so 0 is on the inner surface). You
		# need to set this value!
		
		
		

		
		# outer walls
		# {'name_of_wall': [area, tilt, orientation]}
		# interior walls
		# {'name_of_wall': [area, tilt, orientation]}
		# interior floors
		# {'name_of_wall': [area]}
		
		w_n = scaler[2]*(6.5*5.1-(1.58*0.83+1.63*0.58+1.8*2.1+1.58*0.83))
		w_e = scaler[2]*(7.20*5.1-(0.80*2.05-0.74-0.89))
		w_s = scaler[2]*(6.5*5.1-(1.02*0.87+2.16*0.81+0.8*2.05+2.12*1.07))
		w_w = scaler[2]*(7.20*5.1-(0.80*2.05-0.74-0.89))
		
		out_wall_dict = {"OuterWall_north": [w_n, 90.0, 0.0],
						 "OuterWall_east": [w_e, 90.0, 90.0],
						 "OuterWall_south": [w_s, 90.0, 180.0],
						 "OuterWall_west": [w_w, 90.0, 270.0]
						 }
		 
		# Lump all inner walls into one 
		in_wall_dict = {"InnerWall_south": [scaler[3]*((4.3+3.83+2.93+4.43-(4.43+3.83-4.43-2.63-0.016*2-0.105))*2.5+(2.03+1.63+2.63+2.28+3.83-2.63+3.23+2.93+3.23-1.9)*2.35), 90.0, 0.0],
						 }
		
		# Only areas given
		in_floor_dict = {"InnerFloor1": [scaler[4]*(19.05+13.14+7.71+10.05)],
						}
		
		roof_dict = {"Roof_South": [0,  55, 180],
						"Roof_North": [0, 55, 0],
						"Roof_West": [0, 55, 270],
						"Roof_East": [0, 55, 90]
						}
		
		# Calculate the areas, assumed tilt 55 degrees
		roof_dict["Roof_South"][0] = scaler[5]*0.5*2.85*6.50/math.cos(math.radians(roof_dict["Roof_South"][1]))
		
		roof_dict["Roof_North"][0] = scaler[5]*0.5*2.85*6.50/math.cos(math.radians(roof_dict["Roof_North"][1]))
		
		roof_dict["Roof_East"][0] = scaler[5]*(0.5*2.85*(7.20-0.7)/math.cos(math.radians(roof_dict["Roof_East"][1]))+0.7*2.85/math.cos(math.radians(roof_dict["Roof_East"][1]))+2.85*1.2/math.cos(math.radians(roof_dict["Roof_East"][1])))
		
		roof_dict["Roof_West"][0] = scaler[5]*(0.5*2.85*(7.20-0.7)/math.cos(math.radians(roof_dict["Roof_West"][1]))+0.7*2.85/math.cos(math.radians(roof_dict["Roof_West"][1]))+2.85*1.2/math.cos(math.radians(roof_dict["Roof_West"][1])))				

		# For ground floors the orientation is always -2

		ground_floor_dict = {"GroundFloor": [scaler[4]*(19.05+13.14+7.71+10.05), 0.0, -2]}
						
		win_dict = {"Window_south1": [scaler[6]*2.12*1.07, 90.0, 180.0],
					"Window_south2": [scaler[6]*2.16*0.81, 90.0, 180.0],
					"Window_south3": [scaler[6]*0.87*1.02, 90.0, 180.0],
					"Window_north1": [scaler[6]*1.58*0.83, 90.0, 0],
					"Window_north2": [scaler[6]*1.63*0.58, 90.0, 0],
					"Window_north3": [scaler[6]*1.58*0.83, 90.0, 0],
					"Door_back": [1.8*2.10, 90.0, 0],
					"Window_east": [scaler[6]*0.74*0.89, 90.0, 90],
					"Window_east": [scaler[6]*0.74*0.89, 90.0, 270]
					}
		
		door_dict = {"Door_front": [0.8*2.05, 90.0, 180.0],
					"Door_side1": [0.8*2.05, 90.0, 90.0],
					"Door_side2": [0.8*2.05, 90.0, 270]
					}
					
		# Start with the roof
		for key, value in roof_dict.items():
			roof = Rooftop(parent=tz)
			roof.name = key
			roof.tilt = value[1]
			roof.area = value[0]
			roof.orientation = value[2]
			roof.inner_convection = 4.3
			roof.outer_convection = 18.1
			roof.inner_radiation = 5.7
			roof.outer_radiation = 5.7
			
			# Plasterboard
			layer_s1 = Layer(parent=roof, id=0)
			layer_s1.thickness = 0.010

			material_s1 = Material(layer_s1)
			material_s1.name = "Plasterboard"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]
			
			# Insulation
			layer_s2 = Layer(parent=roof, id=1)
			layer_s2.thickness = scaler[7]*0.10

			material_s1 = Material(layer_s2)
			material_s1.name = "Glass_fibre"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]
			
			
			#Loft space
			layer_s3 = Layer(parent=roof, id=2)
			layer_s3.thickness = 0.5*2.15 # Average of the smallest height (conservative)

			material_s1 = Material(layer_s3)
			material_s1.name = "Cavity"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]
			
			# Roof tiles
			layer_s4 = Layer(parent=roof, id=3)
			layer_s4.thickness = 0.010

			material_s1 = Material(layer_s4)
			material_s1.name = "Roof_tile"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]
		
			
		
		# External Walls
		for key, value in out_wall_dict.items():
			# Instantiate class, key is the name
			out_wall = OuterWall(parent=tz)
			out_wall.name = key
			out_wall.inner_convection = 3.0
			out_wall.outer_convection = 14
			out_wall.inner_radiation = 5.7
			out_wall.outer_radiation = 5.7
		
			# area, tilt and orientation need to be set individually.

			out_wall.area = value[0]
			out_wall.tilt = value[1]
			out_wall.orientation = value[2]
			
			# External walls
			# Plaster
			layer_s1 = Layer(parent=out_wall, id=0)
			layer_s1.thickness = 0.016

			material_s1 = Material(layer_s1)
			material_s1.name = "Plaster"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]
			
			# Brick, inner 
			layer_s2 = Layer(parent=out_wall, id=1)
			layer_s2.thickness = 0.105

			material_s1 = Material(layer_s2)
			material_s1.name = "Brick_in"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]
			
			# Cavity
			layer_s3 = Layer(parent=out_wall, id=2)
			layer_s3.thickness = 0.065

			material_s1 = Material(layer_s3)
			material_s1.name = "Cavity"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]
			
			# Insulation
			layer_s4 = Layer(parent=out_wall, id=3)
			layer_s4.thickness = scaler[8]*0.065

			material_s1 = Material(layer_s4)
			material_s1.name = "Insulation"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]
			
			# Brick, outer
			layer_s5 = Layer(parent=out_wall, id=4)
			layer_s5.thickness = 0.105

			material_s1 = Material(layer_s5)
			material_s1.name = "Brick_out"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]

			

		# Inner walls

		for key, value in in_wall_dict.items():

			in_wall = InnerWall(parent=tz)
			in_wall.name = key
			in_wall.area = value[0]
			in_wall.tilt = value[1]
			in_wall.orientation = value[2]
			in_wall.inner_convection = 3.0
			in_wall.outer_convection = 3.0
			in_wall.inner_radiation = 5.7
			in_wall.outer_radiation = 5.7
			
			# Plaster
			layer_s1 = Layer(parent=in_wall, id=0)
			layer_s1.thickness = 0.016

			material_s1 = Material(layer_s1)
			material_s1.name = "Plaster"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]
			
			# Brick
			layer_s2 = Layer(parent=in_wall, id=1)
			layer_s2.thickness = 0.105 # Average of the smallest height (conservative)

			material_s1 = Material(layer_s2)
			material_s1.name = "Brick_in"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]
			
			# Plaster 
			layer_s3 = Layer(parent=in_wall, id=2)
			layer_s3.thickness = 0.016 # Average of the smallest height (conservative)

			material_s1 = Material(layer_s3)
			material_s1.name = "Plaster"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]
			
		# Inner floors
		
		for key, value in in_floor_dict.items():

			in_floor = Floor(parent=tz)
			in_floor.name = key
			in_floor.area = value[0]
			in_floor.inner_convection = 3.0
			in_floor.outer_convection = 3.0
			in_floor.inner_radiation = 5.7
			in_floor.outer_radiation = 5.7

			# Plaster
			layer_s1 = Layer(parent=in_floor, id=0)
			layer_s1.thickness = 0.005

			material_s1 = Material(layer_s1)
			material_s1.name = "Carpet"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]
			
			# timber 
			layer_s2 = Layer(parent=in_floor, id=1)
			layer_s2.thickness = 0.020

			material_s1 = Material(layer_s2)
			material_s1.name = "Timber"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]
			
			# Cavity
			layer_s3 = Layer(parent=in_floor, id=2)
			layer_s3.thickness = 0.200

			material_s1 = Material(layer_s3)
			material_s1.name = "Cavity"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]
			
			# Plasterboard
			layer_s4 = Layer(parent=in_floor, id=3)
			layer_s4.thickness = 0.010

			material_s1 = Material(layer_s4)
			material_s1.name = "Plasterboard"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]

		for key, value in ground_floor_dict.items():

			ground = GroundFloor(parent=tz)
			ground.name = key
			ground.area = value[0]
			ground.tilt = value[1]
			ground.orientation = value[2]
			ground.inner_convection = 3.0
			ground.outer_convection = 100000000000000
			ground.inner_radiation = 5.7
			ground.outer_radiation = 100000000000000
			
			# Carpet
			layer_s1 = Layer(parent=ground, id=0)
			layer_s1.thickness = 0.005
			
			material_s1 = Material(layer_s1)
			material_s1.name = "Carpet"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]
			
			# timber 
			layer_s2 = Layer(parent=ground, id=1)
			layer_s2.thickness = 0.1

			material_s1 = Material(layer_s2)
			material_s1.name = "Concrete"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]
			
			#Earth
			layer_s3 = Layer(parent=ground, id=2)
			layer_s3.thickness = 0.160

			material_s1 = Material(layer_s3)
			material_s1.name = "Earth"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]
		
		# Doors
		
		for key, value in door_dict.items():
			# Instantiate class, key is the name
			out_wall = OuterWall(parent=tz)
			out_wall.name = key
			out_wall.area = value[0]
			out_wall.tilt = value[1]
			out_wall.orientation = value[2]
			out_wall.inner_convection = 3.0
			out_wall.outer_convection = 14
			out_wall.inner_radiation = 5.7
			out_wall.outer_radiation = 5.7
			
			layer_s1 = Layer(parent=out_wall, id=0)
			layer_s1.thickness = 0.030

			material_s1 = Material(layer_s1)
			material_s1.name = "Softwood"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]
		
		
		# Windows
		for key, value in win_dict.items():

			win = Window(parent = tz)
			win.name = key
			win.area = value[0]
			win.tilt = value[1]
			win.orientation = value[2]

			# Additional to the already known attributes the window has
			# additional attributes. Window.g_value describes the solar gain
			# through windows, a_conv the convective heat transmission due to
			# absorption of the window on the inner side. shading_g_total and
			# shading_max_irr refers to the shading (solar gain reduction of the
			# shading and shading_max_irr the threshold of irradiance to
			# automatically apply shading).

			win.inner_convection = 3
			win.inner_radiation = 14
			win.outer_convection = 5.7
			win.outer_radiation = 5.7
			win.g_value = 0.84
			win.a_conv = 0.03
			win.shading_g_total = 0.0
			win.shading_max_irr = 180.0

			# Double-glazed windows:

			win_layer1 = Layer(parent=win)
			win_layer1.id = 0
			win_layer1.thickness = 0.006
			
			# Material for Glas
			win_material = Material(win_layer1)
			win_material.name = "GlasWindow"
			win_material.density = Mat_dict[material_s1.name][0]
			win_material.heat_capac = Mat_dict[material_s1.name][1]
			win_material.thermal_conduc = Mat_dict[material_s1.name][2]
			win_material.ir_emissivity = Mat_dict[material_s1.name][3]
			win_material.solar_absorp = Mat_dict[material_s1.name][4]
			win_material.transmittance = 0.8
			
			# Gap of 12 mm
			win_layer2 = Layer(parent=win)
			win_layer2.id = 1
			win_layer2.thickness = 0.012
			
			win_material = Material(win_layer2)
			win_material.name = "Cavity"
			win_material.density = Mat_dict[material_s1.name][0]
			win_material.heat_capac = Mat_dict[material_s1.name][1]
			win_material.thermal_conduc = Mat_dict[material_s1.name][2]
			win_material.ir_emissivity = Mat_dict[material_s1.name][3]
			win_material.solar_absorp = Mat_dict[material_s1.name][4]
			win_material.transmittance = 0.8
			
			
			#Glass
			win_layer3 = Layer(parent=win)
			win_layer3.id = 2
			win_layer3.thickness = 0.006
			
			# Material for Glas
			win_material = Material(win_layer3)
			win_material.name = "GlasWindow"
			win_material.density = Mat_dict[material_s1.name][0]
			win_material.heat_capac = Mat_dict[material_s1.name][1]
			win_material.thermal_conduc = Mat_dict[material_s1.name][2]
			win_material.ir_emissivity = Mat_dict[material_s1.name][3]
			win_material.solar_absorp = Mat_dict[material_s1.name][4]
			win_material.transmittance = 0.8
	

		#  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
		# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
		# %%%%% ---- Semi detached House --- %%%%%%%%%%%%% 
	
	if type == "semi-detached":
		print("Creating a semi-detached house")
	
		bldg.year_of_construction = 1950
		bldg.number_of_floors = 2
		bldg.height_of_floors = 2.35

		# Instantiate a ThermalZone class and set the Building as a parent of it.
		# Set some parameters of the thermal zone. Be careful: Dymola does not
		# like whitespaces in  names and filenames, thus we will delete them
		# anyway in TEASER.

		tz = ThermalZone(parent=bldg)
		tz.name = "House"
		tz.area = scaler[1]*(14.69+13.52+4.73+9.60)
		tz.volume = tz.area * bldg.number_of_floors * bldg.height_of_floors
		tz.infiltration_rate = 0.7 # Based on SAP

		# Instantiate BoundaryConditions and load conditions for `Living`.
		tz.use_conditions = BoundaryConditions(parent=tz)
		tz.use_conditions.load_use_conditions("Living", prj.data)

		# Define two building elements reflecting a pitched roof (south = 180 and
		# north = 0). Setting the the ThermalZone as a parent will automatically
		# assign this element to the thermal zone. We also set names, tilt and
		# coefficients for heat transfer on the inner and outer side of the
		# roofs. If the building has a flat roof, please use -1 as
		# orientation. Please read the docs to get more information on these
		# parameters.

		
		# To define the wall constructions we need to instantiate Layer and
		# Material objects and set attributes. id indicates the order of wall
		# construction from inside to outside (so 0 is on the inner surface). You
		# need to set this value!
		
		
		

		
		# outer walls
		# {'name_of_wall': [area, tilt, orientation]}
		# interior walls
		# {'name_of_wall': [area, tilt, orientation]}
		# interior floors
		# {'name_of_wall': [area]}
		
		w_n = scaler[2]*(6*4.9-(1.8*2.1+1.58*0.83+0.76*0.76+0.8*2.05))
		w_e = scaler[2]*(7.20*4.9-(0.74*0.89))
		w_s = scaler[2]*(6*4.9-(0.74*0.80+0.8*2.05+1.51*1.02+1.51*0.86))
		w_w = scaler[2]*(7.20*4.9)
		
		out_wall_dict = {"OuterWall_north": [w_n, 90.0, 0.0],
						 "OuterWall_east": [w_e, 90.0, 90.0],
						 "OuterWall_south": [w_s, 90.0, 180.0],
						 }
		 
		# Lump all inner walls into one 
		in_wall_dict = {"InnerWall_south": [scaler[3]*(2.4*(2.03+4.23+3.83)+2.30*(2*2.03+3.83+3.53)), 90.0, 0.0],
		"PartyWall_west": [w_w, 90.0, 270.0]
						 }
		
		# Only areas given
		in_floor_dict = {"InnerFloor1": [scaler[4]*(14.69+13.52+4.73+9.60)]
						}
		
		roof_dict = {"Roof_South": [0,  55, 180],
						"Roof_North": [0, 55, 0],
						"Roof_West": [0, 55, 270],
						"Roof_East": [0, 55, 90]
						}
		
		# Calculate the areas, assumed tilt 55 degrees
		roof_dict["Roof_South"][0] = scaler[5]*0.5*2.50*6.00/math.cos(math.radians(roof_dict["Roof_South"][1]))
		
		roof_dict["Roof_North"][0] = scaler[5]*0.5*2.50*6.00/math.cos(math.radians(roof_dict["Roof_North"][1]))
		
		roof_dict["Roof_East"][0] = scaler[5]*(0.5*2.5*(7.20)/math.cos(math.radians(roof_dict["Roof_East"][1])))
		
		roof_dict["Roof_West"][0] = scaler[5]*(0.5*2.5*(7.20)/math.cos(math.radians(roof_dict["Roof_East"][1])))			

		# For ground floors the orientation is always -2

		ground_floor_dict = {"GroundFloor": [scaler[4]*(14.69+13.52+4.73+9.60), 0.0, -2]}
						
		win_dict = {"Window_south1": [scaler[6]*0.74*0.89, 90.0, 180.0],
					"Window_south2": [scaler[6]*0.89*1.51, 90.0, 180.0],
					"Window_south3": [scaler[6]*1.02*1.51, 90.0, 180.0],
					"Window_north1": [scaler[6]*1.58*0.83, 90.0, 0],
					"Window_north2": [scaler[6]*0.96*0.76, 90.0, 0],
					"Door_back": [1.8*2.10, 90.0, 0],
					"Window_east": [scaler[6]*0.74*0.89, 90.0, 90]
					}
		
		door_dict = {"Door_front": [0.8*2.05, 90.0, 180.0],
					"Door_back1": [0.8*2.05, 90.0, 0]
					}
					
		# Start with the roof
		for key, value in roof_dict.items():
			roof = Rooftop(parent=tz)
			roof.name = key
			roof.tilt = value[1]
			roof.area = value[0]
			roof.orientation = value[2]
			roof.inner_convection = 4.3
			roof.outer_convection = 18.1
			roof.inner_radiation = 5.7
			roof.outer_radiation = 5.7
			
			# Plasterboard
			layer_s1 = Layer(parent=roof, id=0)
			layer_s1.thickness = 0.010

			material_s1 = Material(layer_s1)
			material_s1.name = "Plasterboard"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]
			
			# Insulation
			layer_s2 = Layer(parent=roof, id=1)
			layer_s2.thickness = scaler[7]*0.10

			material_s1 = Material(layer_s2)
			material_s1.name = "Glass_fibre"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]
			
			
			#Loft space
			layer_s3 = Layer(parent=roof, id=2)
			layer_s3.thickness = 0.5*2.15 # Average of the smallest height (conservative)

			material_s1 = Material(layer_s3)
			material_s1.name = "Cavity"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]
			
			# Roof tiles
			layer_s4 = Layer(parent=roof, id=3)
			layer_s4.thickness = 0.010

			material_s1 = Material(layer_s4)
			material_s1.name = "Roof_tile"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]
		
			
		
		# External Walls
		for key, value in out_wall_dict.items():
			# Instantiate class, key is the name
			out_wall = OuterWall(parent=tz)
			out_wall.name = key
			out_wall.inner_convection = 3.0
			out_wall.outer_convection = 14
			out_wall.inner_radiation = 5.7
			out_wall.outer_radiation = 5.7
		
			# area, tilt and orientation need to be set individually.

			out_wall.area = value[0]
			out_wall.tilt = value[1]
			out_wall.orientation = value[2]
			
			# External walls
			# Plaster
			layer_s1 = Layer(parent=out_wall, id=0)
			layer_s1.thickness = 0.016

			material_s1 = Material(layer_s1)
			material_s1.name = "Plaster"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]
			
			# Brick, inner 
			layer_s2 = Layer(parent=out_wall, id=1)
			layer_s2.thickness = 0.105

			material_s1 = Material(layer_s2)
			material_s1.name = "Brick_in"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]
			
			# Cavity
			layer_s3 = Layer(parent=out_wall, id=2)
			layer_s3.thickness = 0.065

			material_s1 = Material(layer_s3)
			material_s1.name = "Cavity"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]
			
			# Insulation
			layer_s4 = Layer(parent=out_wall, id=3)
			layer_s4.thickness = scaler[8]*0.065

			material_s1 = Material(layer_s4)
			material_s1.name = "Insulation"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]
			
			# Brick, outer
			layer_s5 = Layer(parent=out_wall, id=4)
			layer_s5.thickness = 0.105

			material_s1 = Material(layer_s5)
			material_s1.name = "Brick_out"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]

			

		# Inner walls

		for key, value in in_wall_dict.items():

			in_wall = InnerWall(parent=tz)
			in_wall.name = key
			in_wall.area = value[0]
			in_wall.tilt = value[1]
			in_wall.orientation = value[2]
			in_wall.inner_convection = 3.0
			in_wall.outer_convection = 3.0
			in_wall.inner_radiation = 5.7
			in_wall.outer_radiation = 5.7
			
			# Plaster
			layer_s1 = Layer(parent=in_wall, id=0)
			layer_s1.thickness = 0.016

			material_s1 = Material(layer_s1)
			material_s1.name = "Plaster"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]
			
			# Brick
			layer_s2 = Layer(parent=in_wall, id=1)
			layer_s2.thickness = 0.105 # Average of the smallest height (conservative)

			material_s1 = Material(layer_s2)
			material_s1.name = "Brick_in"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]
			
			# Plaster 
			layer_s3 = Layer(parent=in_wall, id=2)
			layer_s3.thickness = 0.016 # Average of the smallest height (conservative)

			material_s1 = Material(layer_s3)
			material_s1.name = "Plaster"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]
			
		# Inner floors
		
		for key, value in in_floor_dict.items():

			in_floor = Floor(parent=tz)
			in_floor.name = key
			in_floor.area = value[0]
			in_floor.inner_convection = 3.0
			in_floor.outer_convection = 3.0
			in_floor.inner_radiation = 5.7
			in_floor.outer_radiation = 5.7

			# Plaster
			layer_s1 = Layer(parent=in_floor, id=0)
			layer_s1.thickness = 0.005

			material_s1 = Material(layer_s1)
			material_s1.name = "Carpet"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]
			
			# timber 
			layer_s2 = Layer(parent=in_floor, id=1)
			layer_s2.thickness = 0.020

			material_s1 = Material(layer_s2)
			material_s1.name = "Timber"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]
			
			# Cavity
			layer_s3 = Layer(parent=in_floor, id=2)
			layer_s3.thickness = 0.200

			material_s1 = Material(layer_s3)
			material_s1.name = "Cavity"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]
			
			# Plasterboard
			layer_s4 = Layer(parent=in_floor, id=3)
			layer_s4.thickness = 0.010

			material_s1 = Material(layer_s4)
			material_s1.name = "Plasterboard"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]

		for key, value in ground_floor_dict.items():

			ground = GroundFloor(parent=tz)
			ground.name = key
			ground.area = value[0]
			ground.tilt = value[1]
			ground.orientation = value[2]
			ground.inner_convection = 3.0
			ground.outer_convection = 100000000000000
			ground.inner_radiation = 5.7
			ground.outer_radiation = 100000000000000
			
			# Carpet
			layer_s1 = Layer(parent=ground, id=0)
			layer_s1.thickness = 0.005
			
			material_s1 = Material(layer_s1)
			material_s1.name = "Carpet"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]
			
			# timber 
			layer_s2 = Layer(parent=ground, id=1)
			layer_s2.thickness = 0.1

			material_s1 = Material(layer_s2)
			material_s1.name = "Concrete"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]
			
			#Earth
			layer_s3 = Layer(parent=ground, id=2)
			layer_s3.thickness = 0.160

			material_s1 = Material(layer_s3)
			material_s1.name = "Earth"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]
		
		# Doors
		
		for key, value in door_dict.items():
			# Instantiate class, key is the name
			out_wall = OuterWall(parent=tz)
			out_wall.name = key
			out_wall.area = value[0]
			out_wall.tilt = value[1]
			out_wall.orientation = value[2]
			out_wall.inner_convection = 3.0
			out_wall.outer_convection = 14
			out_wall.inner_radiation = 5.7
			out_wall.outer_radiation = 5.7
			
			layer_s1 = Layer(parent=out_wall, id=0)
			layer_s1.thickness = 0.030

			material_s1 = Material(layer_s1)
			material_s1.name = "Softwood"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]
		
		
		# Windows
		for key, value in win_dict.items():

			win = Window(parent = tz)
			win.name = key
			win.area = value[0]
			win.tilt = value[1]
			win.orientation = value[2]

			# Additional to the already known attributes the window has
			# additional attributes. Window.g_value describes the solar gain
			# through windows, a_conv the convective heat transmission due to
			# absorption of the window on the inner side. shading_g_total and
			# shading_max_irr refers to the shading (solar gain reduction of the
			# shading and shading_max_irr the threshold of irradiance to
			# automatically apply shading).

			win.inner_convection = 3
			win.inner_radiation = 14
			win.outer_convection = 5.7
			win.outer_radiation = 5.7
			win.g_value = 0.84
			win.a_conv = 0.03
			win.shading_g_total = 0.0
			win.shading_max_irr = 180.0

			# Double-glazed windows:

			win_layer1 = Layer(parent=win)
			win_layer1.id = 0
			win_layer1.thickness = 0.006
			
			# Material for Glas
			win_material = Material(win_layer1)
			win_material.name = "GlasWindow"
			win_material.density = Mat_dict[material_s1.name][0]
			win_material.heat_capac = Mat_dict[material_s1.name][1]
			win_material.thermal_conduc = Mat_dict[material_s1.name][2]
			win_material.ir_emissivity = Mat_dict[material_s1.name][3]
			win_material.solar_absorp = Mat_dict[material_s1.name][4]
			win_material.transmittance = 0.8
			
			# Gap of 12 mm
			win_layer2 = Layer(parent=win)
			win_layer2.id = 1
			win_layer2.thickness = 0.012
			
			win_material = Material(win_layer2)
			win_material.name = "Cavity"
			win_material.density = Mat_dict[material_s1.name][0]
			win_material.heat_capac = Mat_dict[material_s1.name][1]
			win_material.thermal_conduc = Mat_dict[material_s1.name][2]
			win_material.ir_emissivity = Mat_dict[material_s1.name][3]
			win_material.solar_absorp = Mat_dict[material_s1.name][4]
			win_material.transmittance = 0.8
			
			
			#Glass
			win_layer3 = Layer(parent=win)
			win_layer3.id = 2
			win_layer3.thickness = 0.006
			
			# Material for Glas
			win_material = Material(win_layer3)
			win_material.name = "GlasWindow"
			win_material.density = Mat_dict[material_s1.name][0]
			win_material.heat_capac = Mat_dict[material_s1.name][1]
			win_material.thermal_conduc = Mat_dict[material_s1.name][2]
			win_material.ir_emissivity = Mat_dict[material_s1.name][3]
			win_material.solar_absorp = Mat_dict[material_s1.name][4]
			win_material.transmittance = 0.8
	
	
	'''
	%%%%%%%%%%%%%% Post-1919 Terrace %%%%%%%%%%%%%%%%%%%%%
	'''
	
	if type == "terrace":
		print("Creating a post 1919 terraced house")
	
		bldg.year_of_construction = 1950
		bldg.number_of_floors = 2
		bldg.height_of_floors = 2.3

		# Instantiate a ThermalZone class and set the Building as a parent of it.
		# Set some parameters of the thermal zone. Be careful: Dymola does not
		# like whitespaces in  names and filenames, thus we will delete them
		# anyway in TEASER.

		tz = ThermalZone(parent=bldg)
		tz.name = "House"
		tz.area = scaler[1]*(12.42+9.76+6.83+8.69)
		tz.volume = tz.area * bldg.number_of_floors * bldg.height_of_floors
		tz.infiltration_rate = 0.7

		# Instantiate BoundaryConditions and load conditions for `Living`.
		tz.use_conditions = BoundaryConditions(parent=tz)
		tz.use_conditions.load_use_conditions("Living", prj.data)
		
		w_n = scaler[2]*(5.8*4.8-(0.76*0.76+1.56*0.96+1.02*0.87+1.80*2.1))
		w_e = scaler[2]*6.8*4.8
		w_s = scaler[2]*(5.8*4.8-(1.02*0.87*2+1.56*0.96+0.8*2.05))
		w_w = scaler[2]*6.8*4.8
		
		out_wall_dict = {"OuterWall_north": [w_n, 90.0, 0.0],
						 "OuterWall_south": [w_s, 90.0, 180.0],
						 }
		 
		# Lump all inner walls into one 
		in_wall_dict = {"InnerWall_south": [scaler[3]*((4.3+3.83+2.93+4.43-(4.43+3.83-4.43-2.63-0.016*2-0.105))*2.5+(2.03+1.63+2.63+2.28+3.83-2.63+3.23+2.93+3.23-1.9)*2.35), 90.0, 0.0],
						 "PartyWall_east": [w_e, 90.0, 90.0],
						 "PartyWall_west": [w_w, 90.0, 270.0]
						 }
		
		# Only areas given
		in_floor_dict = {"InnerFloor1": [scaler[3]*(12.42+9.76+6.83+8.69)],
						}
		
		roof_dict = {"Roof_South": [0,  55, 180],
						"Roof_North": [0, 55, 0],
						"Roof_West": [0, 55, 270],
						"Roof_East": [0, 55, 90]
						}
		
		# Calculate the areas, assumed tilt 55 degrees
		roof_dict["Roof_South"][0] = scaler[2]*2.7*5.8
		
		roof_dict["Roof_North"][0] = scaler[2]*2.7*5.8
		
		roof_dict["Roof_East"][0] = scaler[2]*0.5*2.7*6.8*math.cos(math.radians(roof_dict["Roof_East"][1]))
		
		roof_dict["Roof_West"][0] = scaler[2]*0.5*2.7*6.8*math.cos(math.radians(roof_dict["Roof_East"][1]))				

		# For ground floors the orientation is always -2

		ground_floor_dict = {"GroundFloor": [scaler[1]*(12.42+9.76+6.83+8.69), 0.0, -2]}
						
		win_dict = {"Window_south1": [scaler[3]*1.02*0.87, 90.0, 180.0],
					"Window_south2": [scaler[3]*1.02*0.87, 90.0, 180.0],
					"Window_south3": [scaler[3]*1.56*0.96, 90.0, 180.0],
					"Window_north1": [scaler[3]*0.76*0.76, 90.0, 0],
					"Window_north2": [scaler[3]*1.56*0.96, 90.0, 0],
					"Window_north3": [scaler[3]*1.02*0.87, 90.0, 0],
					"Door_back": [1.8*2.10, 90.0, 0]
					}
		
		door_dict = {"Door_front": [0.8*2.05, 90.0, 180.0],
					}
		
		# Start with the roof
		for key, value in roof_dict.items():
			roof = Rooftop(parent=tz)
			roof.name = key
			roof.tilt = value[1]
			roof.area = value[0]
			roof.orientation = value[2]
			roof.inner_convection = 4.3
			roof.outer_convection = 18.1
			roof.inner_radiation = 5.7
			roof.outer_radiation = 5.7
			
			# Plasterboard
			layer_s1 = Layer(parent=roof, id=0)
			layer_s1.thickness = 0.010

			material_s1 = Material(layer_s1)
			material_s1.name = "Plasterboard"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]
			
			# Insulation
			layer_s2 = Layer(parent=roof, id=1)
			layer_s2.thickness = 0.10

			material_s1 = Material(layer_s2)
			material_s1.name = "Glass_fibre"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]
			
			
			#Loft space
			layer_s3 = Layer(parent=roof, id=2)
			layer_s3.thickness = 0.5*2.15 # Average of the smallest height (conservative)

			material_s1 = Material(layer_s3)
			material_s1.name = "Cavity"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]
			
			
			# Roof tiles
			layer_s4 = Layer(parent=roof, id=3)
			layer_s4.thickness = 0.010

			material_s1 = Material(layer_s4)
			material_s1.name = "Roof_tile"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]
		
			
		
		# External Walls
		for key, value in out_wall_dict.items():
			# Instantiate class, key is the name
			out_wall = OuterWall(parent=tz)
			out_wall.name = key
			out_wall.inner_convection = 3.0
			out_wall.outer_convection = 14
			out_wall.inner_radiation = 5.7
			out_wall.outer_radiation = 5.7
		
			# area, tilt and orientation need to be set individually.

			out_wall.area = value[0]
			out_wall.tilt = value[1]
			out_wall.orientation = value[2]
			
			# External walls
			# Plaster
			layer_s1 = Layer(parent=out_wall, id=0)
			layer_s1.thickness = 0.016

			material_s1 = Material(layer_s1)
			material_s1.name = "Plaster"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]
			
			# Brick, inner 
			layer_s2 = Layer(parent=out_wall, id=1)
			layer_s2.thickness = 0.105

			material_s1 = Material(layer_s2)
			material_s1.name = "Brick_in"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]
			
			# Insulation
			layer_s5 = Layer(parent=out_wall, id=2)
			layer_s5.thickness = 0.065

			material_s1 = Material(layer_s5)
			material_s1.name = "Cavity"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]
			
			# Cavity
			layer_s3 = Layer(parent=out_wall, id=3)
			layer_s3.thickness = scaler[4]*0.1

			material_s1 = Material(layer_s3)
			material_s1.name = "Insulation"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]
			
			# Brick, outer
			layer_s4 = Layer(parent=out_wall, id=3)
			layer_s4.thickness = 0.105

			material_s1 = Material(layer_s4)
			material_s1.name = "Brick_out"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]

			

		# Inner walls

		for key, value in in_wall_dict.items():

			in_wall = InnerWall(parent=tz)
			in_wall.name = key
			in_wall.area = value[0]
			in_wall.tilt = value[1]
			in_wall.orientation = value[2]
			in_wall.inner_convection = 3.0
			in_wall.outer_convection = 3.0
			in_wall.inner_radiation = 5.7
			in_wall.outer_radiation = 5.7
			
			# Plaster
			layer_s1 = Layer(parent=in_wall, id=0)
			layer_s1.thickness = 0.016

			material_s1 = Material(layer_s1)
			material_s1.name = "Plaster"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]
			
			# Brick
			layer_s2 = Layer(parent=in_wall, id=1)
			layer_s2.thickness = 0.105 # Average of the smallest height (conservative)

			material_s1 = Material(layer_s2)
			material_s1.name = "Brick_in"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]
			
			# Plaster 
			layer_s3 = Layer(parent=in_wall, id=2)
			layer_s3.thickness = 0.016 # Average of the smallest height (conservative)

			material_s1 = Material(layer_s3)
			material_s1.name = "Plaster"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]
			
		# Inner floors
		
		for key, value in in_floor_dict.items():

			in_floor = Floor(parent=tz)
			in_floor.name = key
			in_floor.area = value[0]
			in_floor.inner_convection = 3.0
			in_floor.outer_convection = 3.0
			in_floor.inner_radiation = 5.7
			in_floor.outer_radiation = 5.7

			# Plaster
			layer_s1 = Layer(parent=in_floor, id=0)
			layer_s1.thickness = 0.005

			material_s1 = Material(layer_s1)
			material_s1.name = "Carpet"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]
			
			# timber 
			layer_s2 = Layer(parent=in_floor, id=1)
			layer_s2.thickness = 0.020

			material_s1 = Material(layer_s2)
			material_s1.name = "Timber"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]
			
			# Cavity
			layer_s3 = Layer(parent=in_floor, id=2)
			layer_s3.thickness = 0.200

			material_s1 = Material(layer_s3)
			material_s1.name = "Cavity"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]
			
			# Plasterboard
			layer_s4 = Layer(parent=in_floor, id=3)
			layer_s4.thickness = 0.010

			material_s1 = Material(layer_s4)
			material_s1.name = "Plasterboard"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]

		for key, value in ground_floor_dict.items():

			ground = GroundFloor(parent=tz)
			ground.name = key
			ground.area = value[0]
			ground.tilt = value[1]
			ground.orientation = value[2]
			ground.inner_convection = 3.0
			ground.outer_convection = 100000000000000
			ground.inner_radiation = 5.7
			ground.outer_radiation = 100000000000000
			
			# Carpet
			layer_s1 = Layer(parent=ground, id=0)
			layer_s1.thickness = 0.005
			
			material_s1 = Material(layer_s1)
			material_s1.name = "Carpet"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]
			
			# timber 
			layer_s2 = Layer(parent=ground, id=1)
			layer_s2.thickness = 0.1

			material_s1 = Material(layer_s2)
			material_s1.name = "Concrete"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]
			
			#Earth
			layer_s3 = Layer(parent=ground, id=2)
			layer_s3.thickness = 0.160

			material_s1 = Material(layer_s3)
			material_s1.name = "Earth"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]
		
		# Doors
		
		for key, value in door_dict.items():
			# Instantiate class, key is the name
			out_wall = OuterWall(parent=tz)
			out_wall.name = key
			out_wall.area = value[0]
			out_wall.tilt = value[1]
			out_wall.orientation = value[2]
			out_wall.inner_convection = 3.0
			out_wall.outer_convection = 14
			out_wall.inner_radiation = 5.7
			out_wall.outer_radiation = 5.7
			
			layer_s1 = Layer(parent=out_wall, id=0)
			layer_s1.thickness = 0.030

			material_s1 = Material(layer_s1)
			material_s1.name = "Softwood"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]
		
		
		# Windows
		for key, value in win_dict.items():

			win = Window(parent = tz)
			win.name = key
			win.area = value[0]
			win.tilt = value[1]
			win.orientation = value[2]

			# Additional to the already known attributes the window has
			# additional attributes. Window.g_value describes the solar gain
			# through windows, a_conv the convective heat transmission due to
			# absorption of the window on the inner side. shading_g_total and
			# shading_max_irr refers to the shading (solar gain reduction of the
			# shading and shading_max_irr the threshold of irradiance to
			# automatically apply shading).

			win.inner_convection = 3
			win.inner_radiation = 14
			win.outer_convection = 5.7
			win.outer_radiation = 5.7
			win.g_value = 0.84
			win.a_conv = 0.03
			win.shading_g_total = 0.0
			win.shading_max_irr = 180.0

			# Double-glazed windows:

			win_layer1 = Layer(parent=win)
			win_layer1.id = 0
			win_layer1.thickness = 0.006
			
			# Material for Glas
			win_material = Material(win_layer1)
			win_material.name = "GlasWindow"
			win_material.density = Mat_dict[material_s1.name][0]
			win_material.heat_capac = Mat_dict[material_s1.name][1]
			win_material.thermal_conduc = Mat_dict[material_s1.name][2]
			win_material.ir_emissivity = Mat_dict[material_s1.name][3]
			win_material.solar_absorp = Mat_dict[material_s1.name][4]
			win_material.transmittance = 0.8
			
			# Gap of 12 mm
			win_layer2 = Layer(parent=win)
			win_layer2.id = 1
			win_layer2.thickness = 0.012
			
			win_material = Material(win_layer2)
			win_material.name = "Cavity"
			win_material.density = Mat_dict[material_s1.name][0]
			win_material.heat_capac = Mat_dict[material_s1.name][1]
			win_material.thermal_conduc = Mat_dict[material_s1.name][2]
			win_material.ir_emissivity = Mat_dict[material_s1.name][3]
			win_material.solar_absorp = Mat_dict[material_s1.name][4]
			win_material.transmittance = 0.8
			
			
			#Glass
			win_layer3 = Layer(parent=win)
			win_layer3.id = 2
			win_layer3.thickness = 0.006
			
			# Material for Glas
			win_material = Material(win_layer3)
			win_material.name = "GlasWindow"
			win_material.density = Mat_dict[material_s1.name][0]
			win_material.heat_capac = Mat_dict[material_s1.name][1]
			win_material.thermal_conduc = Mat_dict[material_s1.name][2]
			win_material.ir_emissivity = Mat_dict[material_s1.name][3]
			win_material.solar_absorp = Mat_dict[material_s1.name][4]
			win_material.transmittance = 0.8
			
	if type == "office_highcost-mid1980s":
		print("Creating a high-end mid 1980 office floor")
	
		bldg.year_of_construction = 1985
		bldg.number_of_floors = 1
		bldg.height_of_floors = 3.2

		# Instantiate a ThermalZone class and set the Building as a parent of it.
		# Set some parameters of the thermal zone. Be careful: Dymola does not
		# like whitespaces in  names and filenames, thus we will delete them
		# anyway in TEASER.

		tz = ThermalZone(parent=bldg)
		tz.name = "Office"
		tz.area = scaler[1]*288
		tz.volume = tz.area * bldg.number_of_floors * bldg.height_of_floors
		tz.infiltration_rate = 0.7

		# Instantiate BoundaryConditions and load conditions for `Living`.
		tz.use_conditions = BoundaryConditions(parent=tz)
		tz.use_conditions.load_use_conditions("Office", prj.data)
		
		w_e = scaler[2]*8*3.2-4*1.65-0.6*1.65
		w_w = scaler[2]*8*3.2-4*1.65-0.6*1.65
		w_s = scaler[2]*36*3.2-6*4*1.65-5*0.6*1.65
		
		out_wall_dict = {"OuterWall_east": [w_e, 90.0, 90],
							"OuterWall_south": [w_s, 90.0, 180],
							"OuterWall_west": [w_w, 90.0, 270],
						 }
		 
		# Lump all inner walls into one 
		in_wall_dict = {"InnerWall_south": [scaler[3]*115.2, 90, 0],
						"PartyWall_north": [scaler[2]*36*3.2, 90.0, 0]
						 }
		
		# Only areas given
		in_floor_dict = {"InnerFloor1": [scaler[1]*288],
							"InnerCeiling": [scaler[1]*288]
						}
		
		#roof_dict = {"Roof_South": [36*3.2,  55, 180],
		#				}			

		# For ground floors the orientation is always -2

		#ground_floor_dict = {"GroundFloor": [288, 0.0, -2]}
						
		win_dict = {"Window_south": [scaler[4]*6*4*1.65+5*0.6*1.65, 90.0, 180.0],
					"Window_east": [scaler[4]*4*1.65+0.6*1.65, 90.0, 180.0],
					"Window_west": [scaler[4]*4*1.65+0.6*1.65, 90.0, 180.0],
					}
					
		# External Walls
		for key, value in out_wall_dict.items():
			# Instantiate class, key is the name
			out_wall = OuterWall(parent=tz)
			out_wall.name = key
			out_wall.inner_convection = 3.0
			out_wall.outer_convection = 14
			out_wall.inner_radiation = 5.7
			out_wall.outer_radiation = 5.7
		
			# area, tilt and orientation need to be set individually.

			out_wall.area = value[0]
			out_wall.tilt = value[1]
			out_wall.orientation = value[2]
			
			# External walls
			# Dry lining
			layer_s1 = Layer(parent=out_wall, id=0)
			layer_s1.thickness = 0.01

			material_s1 = Material(layer_s1)
			material_s1.name = "Plaster"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]
			
			# Insulation
			layer_s2 = Layer(parent=out_wall, id=1)
			layer_s2.thickness = scaler[5]*0.070

			material_s1 = Material(layer_s2)
			material_s1.name = "Insulation"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]
			
			# Concrete Block
			layer_s3 = Layer(parent=out_wall, id=2)
			layer_s3.thickness = 0.140

			material_s1 = Material(layer_s3)
			material_s1.name = "ConcreteBlock"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]
			
			# Portland Stone
			layer_s4 = Layer(parent=out_wall, id=3)
			layer_s4.thickness = 0.050

			material_s1 = Material(layer_s4)
			material_s1.name = "PortlandStone"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]

		# Inner walls

		for key, value in in_wall_dict.items():

			in_wall = InnerWall(parent=tz)
			in_wall.name = key
			in_wall.area = value[0]
			in_wall.tilt = value[1]
			in_wall.orientation = value[2]
			in_wall.inner_convection = 3.0
			in_wall.outer_convection = 3.0
			in_wall.inner_radiation = 5.7
			in_wall.outer_radiation = 5.7
			
			# Plaster
			layer_s1 = Layer(parent=in_wall, id=0)
			layer_s1.thickness = 0.016

			material_s1 = Material(layer_s1)
			material_s1.name = "Plaster"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]
			
			# Brick
			layer_s2 = Layer(parent=in_wall, id=1)
			layer_s2.thickness = 0.100 # Average of the smallest height (conservative)

			material_s1 = Material(layer_s2)
			material_s1.name = "ConcreteWallPanel"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]
			
			# Plaster 
			layer_s3 = Layer(parent=in_wall, id=2)
			layer_s3.thickness = 0.016 # Average of the smallest height (conservative)

			material_s1 = Material(layer_s3)
			material_s1.name = "Plaster"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]
			
		# Inner floors
		
		for key, value in in_floor_dict.items():

			in_floor = Floor(parent=tz)
			in_floor.name = key
			in_floor.area = value[0]
			in_floor.inner_convection = 3.0
			in_floor.outer_convection = 3.0
			in_floor.inner_radiation = 5.7
			in_floor.outer_radiation = 5.7

			# Screed
			layer_s1 = Layer(parent=in_floor, id=0)
			layer_s1.thickness = 0.005

			material_s1 = Material(layer_s1)
			material_s1.name = "Screed"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]
			
			# Concrete
			layer_s2 = Layer(parent=in_floor, id=1)
			layer_s2.thickness = 0.370

			material_s1 = Material(layer_s2)
			material_s1.name = "ConcreteFloorPanel"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]
		
		# Windows
		for key, value in win_dict.items():

			win = Window(parent = tz)
			win.name = key
			win.area = value[0]
			win.tilt = value[1]
			win.orientation = value[2]

			# Additional to the already known attributes the window has
			# additional attributes. Window.g_value describes the solar gain
			# through windows, a_conv the convective heat transmission due to
			# absorption of the window on the inner side. shading_g_total and
			# shading_max_irr refers to the shading (solar gain reduction of the
			# shading and shading_max_irr the threshold of irradiance to
			# automatically apply shading).

			win.inner_convection = 3
			win.inner_radiation = 14
			win.outer_convection = 5.7
			win.outer_radiation = 5.7
			win.g_value = 0.84
			win.a_conv = 0.03
			win.shading_g_total = 0.0
			win.shading_max_irr = 180.0

			# Double-glazed windows:

			win_layer1 = Layer(parent=win)
			win_layer1.id = 0
			win_layer1.thickness = 0.006
			
			# Material for Glas
			win_material = Material(win_layer1)
			win_material.name = "GlasWindow"
			win_material.density = Mat_dict[material_s1.name][0]
			win_material.heat_capac = Mat_dict[material_s1.name][1]
			win_material.thermal_conduc = Mat_dict[material_s1.name][2]
			win_material.ir_emissivity = Mat_dict[material_s1.name][3]
			win_material.solar_absorp = Mat_dict[material_s1.name][4]
			win_material.transmittance = 0.8
			
			# Gap of 12 mm
			win_layer2 = Layer(parent=win)
			win_layer2.id = 1
			win_layer2.thickness = 0.012
			
			win_material = Material(win_layer2)
			win_material.name = "Cavity"
			win_material.density = Mat_dict[material_s1.name][0]
			win_material.heat_capac = Mat_dict[material_s1.name][1]
			win_material.thermal_conduc = Mat_dict[material_s1.name][2]
			win_material.ir_emissivity = Mat_dict[material_s1.name][3]
			win_material.solar_absorp = Mat_dict[material_s1.name][4]
			win_material.transmittance = 0.8
			
			
			#Glass
			win_layer3 = Layer(parent=win)
			win_layer3.id = 2
			win_layer3.thickness = 0.006
			
			# Material for Glas
			win_material = Material(win_layer3)
			win_material.name = "GlasWindow"
			win_material.density = Mat_dict[material_s1.name][0]
			win_material.heat_capac = Mat_dict[material_s1.name][1]
			win_material.thermal_conduc = Mat_dict[material_s1.name][2]
			win_material.ir_emissivity = Mat_dict[material_s1.name][3]
			win_material.solar_absorp = Mat_dict[material_s1.name][4]
			win_material.transmittance = 0.8
		
	
	if type == "office_lowenergy-early1980s":
		
		print("Creating low-energy 1980s office")
	
		bldg.year_of_construction = 1980
		bldg.number_of_floors = 1
		bldg.height_of_floors = 2.5

		# Instantiate a ThermalZone class and set the Building as a parent of it.
		# Set some parameters of the thermal zone. Be careful: Dymola does not
		# like whitespaces in  names and filenames, thus we will delete them
		# anyway in TEASER.

		tz = ThermalZone(parent=bldg)
		tz.name = "Office"
		tz.area = scaler[1]*4.7*3.65
		tz.volume = tz.area * bldg.number_of_floors * bldg.height_of_floors
		tz.infiltration_rate = 1

		# Instantiate BoundaryConditions and load conditions for `Living`.
		tz.use_conditions = BoundaryConditions(parent=tz)
		tz.use_conditions.load_use_conditions("Office", prj.data)
		
		w_s = scaler[2]*3.65*2.5-2.95*1.3
		
		out_wall_dict = {"OuterWall_south": [w_s, 90.0, 180],
						 }
		 
		# Lump all inner walls into one 
		in_wall_dict = {"InnerWall_south": [scaler[3]*2*4.7*2,5,90,0],
						"PartyWall_north": [scaler[2]*3.65*2.5, 90.0, 0]
						 }
		
		# Only areas given
		in_floor_dict = {"InnerFloor1": [scaler[4]*3.65*4.7],
							"InnerCeiling": [scaler[4]*3.65*4.7]
						}
		

		#ground_floor_dict = {"GroundFloor": [288, 0.0, -2]}
						
		win_dict = {"Window_south": [scaler[5]*2.95*1.3, 90.0, 180.0],
					}
					
		# External Walls
		for key, value in out_wall_dict.items():
			# Instantiate class, key is the name
			out_wall = OuterWall(parent=tz)
			out_wall.name = key
			out_wall.inner_convection = 3.0
			out_wall.outer_convection = 14
			out_wall.inner_radiation = 5.7
			out_wall.outer_radiation = 5.7
		
			# area, tilt and orientation need to be set individually.

			out_wall.area = value[0]
			out_wall.tilt = value[1]
			out_wall.orientation = value[2]
			
			# External walls
			# Dry lining
			layer_s1 = Layer(parent=out_wall, id=0)
			layer_s1.thickness = 0.01

			material_s1 = Material(layer_s1)
			material_s1.name = "Plaster"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]
			
			# Timber
			layer_s2 = Layer(parent=out_wall, id=1)
			layer_s2.thickness = 0.100

			material_s1 = Material(layer_s2)
			material_s1.name = "Timber"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]
			
			# Insulation
			layer_s3 = Layer(parent=out_wall, id=2)
			layer_s3.thickness = scaler[6]*0.150

			material_s1 = Material(layer_s3)
			material_s1.name = "Insulation"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]
			
			# Cavity
			layer_s4 = Layer(parent=out_wall, id=3)
			layer_s4.thickness = 0.150

			material_s1 = Material(layer_s4)
			material_s1.name = "Cavity"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]
			
			# Concrete
			layer_s5 = Layer(parent=out_wall, id=4)
			layer_s5.thickness = 0.10

			material_s1 = Material(layer_s5)
			material_s1.name = "ConcreteBlock"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]
			
			# Ceramic tiles
			layer_s6 = Layer(parent=out_wall, id=5)
			layer_s6.thickness = 0.0010

			material_s1 = Material(layer_s6)
			material_s1.name = "CeramicTiles"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]

		# Inner walls

		for key, value in in_wall_dict.items():

			in_wall = InnerWall(parent=tz)
			in_wall.name = key
			in_wall.area = value[0]
			in_wall.tilt = value[1]
			in_wall.orientation = value[2]
			in_wall.inner_convection = 3.0
			in_wall.outer_convection = 3.0
			in_wall.inner_radiation = 5.7
			in_wall.outer_radiation = 5.7
			
			# Plaster
			layer_s1 = Layer(parent=in_wall, id=0)
			layer_s1.thickness = 0.016

			material_s1 = Material(layer_s1)
			material_s1.name = "Plaster"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]
			
			# Brick
			layer_s2 = Layer(parent=in_wall, id=1)
			layer_s2.thickness = 0.100 # Average of the smallest height (conservative)

			material_s1 = Material(layer_s2)
			material_s1.name = "ConcreteWallPanel"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]
			
			# Plaster 
			layer_s3 = Layer(parent=in_wall, id=2)
			layer_s3.thickness = 0.016 # Average of the smallest height (conservative)

			material_s1 = Material(layer_s3)
			material_s1.name = "Plaster"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]
			
		# Inner floors
		
		for key, value in in_floor_dict.items():

			in_floor = Floor(parent=tz)
			in_floor.name = key
			in_floor.area = value[0]
			in_floor.inner_convection = 3.0
			in_floor.outer_convection = 3.0
			in_floor.inner_radiation = 5.7
			in_floor.outer_radiation = 5.7

			# Screed
			layer_s1 = Layer(parent=in_floor, id=0)
			layer_s1.thickness = 0.005

			material_s1 = Material(layer_s1)
			material_s1.name = "Screed"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]
			
			# Concrete
			layer_s2 = Layer(parent=in_floor, id=1)
			layer_s2.thickness = 0.205

			material_s1 = Material(layer_s2)
			material_s1.name = "ConcreteFloorPanel"
			material_s1.density = Mat_dict[material_s1.name][0]
			material_s1.heat_capac = Mat_dict[material_s1.name][1]
			material_s1.thermal_conduc = Mat_dict[material_s1.name][2]
			material_s1.ir_emissivity = Mat_dict[material_s1.name][3]
			material_s1.solar_absorp = Mat_dict[material_s1.name][4]
		
		# Windows
		for key, value in win_dict.items():

			win = Window(parent = tz)
			win.name = key
			win.area = value[0]
			win.tilt = value[1]
			win.orientation = value[2]

			# Additional to the already known attributes the window has
			# additional attributes. Window.g_value describes the solar gain
			# through windows, a_conv the convective heat transmission due to
			# absorption of the window on the inner side. shading_g_total and
			# shading_max_irr refers to the shading (solar gain reduction of the
			# shading and shading_max_irr the threshold of irradiance to
			# automatically apply shading).

			win.inner_convection = 3
			win.inner_radiation = 14
			win.outer_convection = 5.7
			win.outer_radiation = 5.7
			win.g_value = 0.84
			win.a_conv = 0.03
			win.shading_g_total = 0.0
			win.shading_max_irr = 180.0

			# Double-glazed windows:

			win_layer1 = Layer(parent=win)
			win_layer1.id = 0
			win_layer1.thickness = 0.006
			
			# Material for Glas
			win_material = Material(win_layer1)
			win_material.name = "GlasWindow"
			win_material.density = Mat_dict[material_s1.name][0]
			win_material.heat_capac = Mat_dict[material_s1.name][1]
			win_material.thermal_conduc = Mat_dict[material_s1.name][2]
			win_material.ir_emissivity = Mat_dict[material_s1.name][3]
			win_material.solar_absorp = Mat_dict[material_s1.name][4]
			win_material.transmittance = 0.8
			
			# Gap of 12 mm
			win_layer2 = Layer(parent=win)
			win_layer2.id = 1
			win_layer2.thickness = 0.012
			
			win_material = Material(win_layer2)
			win_material.name = "Cavity"
			win_material.density = Mat_dict[material_s1.name][0]
			win_material.heat_capac = Mat_dict[material_s1.name][1]
			win_material.thermal_conduc = Mat_dict[material_s1.name][2]
			win_material.ir_emissivity = Mat_dict[material_s1.name][3]
			win_material.solar_absorp = Mat_dict[material_s1.name][4]
			win_material.transmittance = 0.8
			
			
			#Glass
			win_layer3 = Layer(parent=win)
			win_layer3.id = 2
			win_layer3.thickness = 0.006
			
			# Material for Glas
			win_material = Material(win_layer3)
			win_material.name = "GlasWindow"
			win_material.density = Mat_dict[material_s1.name][0]
			win_material.heat_capac = Mat_dict[material_s1.name][1]
			win_material.thermal_conduc = Mat_dict[material_s1.name][2]
			win_material.ir_emissivity = Mat_dict[material_s1.name][3]
			win_material.solar_absorp = Mat_dict[material_s1.name][4]
			win_material.transmittance = 0.8
