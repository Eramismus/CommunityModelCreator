# This code is for creating building models from REFIT dataset
import os
import xml.etree.ElementTree as ET
import teaser.logic.utilities as utilities
from teaser.project import Project
from mako.template import Template
from mako.lookup import TemplateLookup
import dill
from standardhouse import create_stand_dwelling
import numpy as np

def store_namespace(filename,class_name):
	with open(str(filename+'.pkl'), 'wb') as file:
		dill.dump(class_name, file)
	print("Object" + str(class_name) + " stored to " + str(filename))
	
def load_namespace(filename):
	with open(str(filename+'.pkl'), 'rb') as file:
		a = dill.load(file)
	print("Object loaded from " + str(filename))
	return a
	
def create_package(path, name, uses=None, within=None):
    """creates a package.mo file

    private function, do not call

    Parameters
    ----------

    path : string
        path of where the package.mo should be placed
    name : string
        name of the Modelica package
    within : string
        path of Modelica package containing this package

    """

    package_template = Template(filename="\\aggr_code_templates\\package")
    out_file = open(
        utilities.get_full_path(os.path.join(path, "package.mo")), 'w')
    out_file.write(package_template.render_unicode(
        name=name,
        within=within,
        uses=uses))
    out_file.close()

def create_package_order(path, package_list, addition=None, extra=None):
    """creates a package.order file

    private function, do not call

    Parameters
    ----------

    path : string
        path of where the package.order should be placed
    package_list : [string]
        name of all models or packages contained in the package
    addition : string
        if there should be a suffix in front of package_list.string it can
        be specified
    extra : string
        an extra package or model not contained in package_list can be
        specified

    """

    order_template = Template(filename="\\aggr_code_templates\\package_order")

    out_file = open(
        utilities.get_full_path(path + "/" + "package" + ".order"), 'w')
    out_file.write(order_template.render_unicode
                   (list=package_list, addition=addition, extra=extra))
    out_file.close()
	

def create_aggregated_AixLib(prj,path,model_name):
	lookup = TemplateLookup(directories=["aggr_code_templates\\"])
	aggr_template = Template(
		filename="",
		lookup=lookup)

	uses = [
		'Modelica(version="' + prj.modelica_info.version + '")',
		'IBPSA(version="' + prj.buildings[-1].library_attr.version + '")',
		str(prj.name)+'(version="1")']

	#print(prj.buildings.name)
	#print(prj.modelica_info)
	utilities.create_path(os.path.join(path,model_name))
		
	out_file = open(os.path.join(path,model_name, model_name + ".mo"), 'w')
	
	out_file.write(aggr_template.render_unicode(
			project_name = prj.name,
			model_name = model_name,
			numbuilds = len(prj.buildings),
            bldg_list=prj.buildings,
            modelica_info=prj.modelica_info))
	out_file.close()
	
	create_package(
        path=os.path.join(path,model_name),
        name=model_name,
        uses=uses,
        within=None)
	create_package_order(
        path=os.path.join(path,model_name),
        package_list=[model_name],
		addition=None,
        extra=None)
		
	with open(os.path.join(path,"package.order"), "a") as myfile:
		myfile.write(model_name)
	myfile.close()

def create_aggregated_IBPSA(prj,path,model_name,template="aggr_code_templates\\Aggregated_IBPSA_mpc"):
	lookup = TemplateLookup(directories=["\\aggr_code_templates\\"])
	aggr_template = Template(
		filename=template,
		lookup=lookup)

	uses = [
		'Modelica(version="' + prj.modelica_info.version + '")',
		'IBPSA(version="' + prj.buildings[-1].library_attr.version + '")',
		str(prj.name)+'(version="1")']

	#print(prj.buildings.name)
	#print(prj.modelica_info)
	utilities.create_path(os.path.join(path,model_name))
		
	out_file = open(os.path.join(path,model_name, model_name + ".mo"), 'w')
	
	out_file.write(aggr_template.render_unicode(
			project_name = prj.name,
			model_name = model_name,
			numbuilds = len(prj.buildings),
            bldg_list=prj.buildings,
            modelica_info=prj.modelica_info))
	out_file.close()
	
	create_package(
        path=os.path.join(path,model_name),
        name=model_name,
        uses=uses,
        within=None)
	create_package_order(
        path=os.path.join(path,model_name),
        package_list=[model_name],
		addition=None,
        extra=None)
		
	with open(os.path.join(path,"package.order"), "a") as myfile:
		myfile.write(model_name)
	myfile.close()

def create_ibpsa_mpc_model(prj,bldg,zone,path):
	lookup = TemplateLookup(directories=["\\aggr_code_templates\\"])
	mpc_template = Template(
		filename="\\aggr_code_templates\\IBPSA_TwoElements_heatpump_radiator",
		lookup=lookup)
		
	uses = [
		'Modelica(version="' + prj.modelica_info.version + '")',
		'IBPSA(version="' + prj.buildings[-1].library_attr.version + '")']

	#print(prj.buildings.name)
	#print(prj.modelica_info)
	bldg_path = os.path.join(path, bldg.name)
	#utilities.create_path(utilities.get_full_path(bldg_path))
	#utilities.create_path(utilities.get_full_path(
            #os.path.join(bldg_path, bldg.name + "_Models")))
	
	zone_path = os.path.join(path,bldg.name,bldg.name + "_Models")
	
	for zone in bldg.thermal_zones:
		out_file = open(utilities.get_full_path(os.path.join(
                zone_path, bldg.name + '_' + zone.name + '_mpc.mo')), 'w')
		out_file.write(mpc_template.render_unicode(zone=zone))
		out_file.close()
		
		with open(os.path.join(zone_path,"package.order"), "a") as myfile:
			myfile.write(str(zone.parent.name+'_'+zone.name+'_mpc\n'))
		myfile.close()

def create_ibpsa_PI_model(prj,bldg,zone,path):
	lookup = TemplateLookup(directories=["\\aggr_code_templates\\"])
	mpc_template = Template(
		filename="\\aggr_code_templates\\IBPSA_TwoElements_PI_heatpump_radiator",
		lookup=lookup)
		
	uses = [
		'Modelica(version="' + prj.modelica_info.version + '")',
		'IBPSA(version="' + prj.buildings[-1].library_attr.version + '")']

	#print(prj.buildings.name)
	#print(prj.modelica_info)
	bldg_path = os.path.join(path, bldg.name)
	#utilities.create_path(utilities.get_full_path(bldg_path))
	#utilities.create_path(utilities.get_full_path(
            #os.path.join(bldg_path, bldg.name + "_Models")))
	
	zone_path = os.path.join(path,bldg.name,bldg.name + "_Models")
	
	for zone in bldg.thermal_zones:
		out_file = open(utilities.get_full_path(os.path.join(
                zone_path, bldg.name + '_' + zone.name + '_PI.mo')), 'w')
		out_file.write(mpc_template.render_unicode(zone=zone))
		out_file.close()
		
		with open(os.path.join(zone_path,"package.order"), "a") as myfile:
			myfile.write(str(zone.parent.name+'_'+zone.name+'_PI\n'))
		myfile.close()
		
def create_mpcpy_package(prj,bldg,zone,path):
	print("Creating packages for mpcpy")
	lookup = TemplateLookup(directories=["\\aggr_code_templates\\"])
	mpc_template = Template(
		filename="\\aggr_code_templates\\mpcpy_package",
		lookup=lookup)
		
	uses = [
		'Modelica(version="' + prj.modelica_info.version + '")',
		'IBPSA(version="' + prj.buildings[-1].library_attr.version + '")']

	#print(prj.buildings.name)
	#print(prj.modelica_info)
	#utilities.create_path(utilities.get_full_path(bldg_path))
	#utilities.create_path(utilities.get_full_path(
            #os.path.join(bldg_path, bldg.name + "_Models")))
	
	for zone in bldg.thermal_zones:
		out_file = open(os.path.join(
                path, bldg.name + '_' + zone.name + '_mpcpy.mo'), 'w')
		out_file.write(mpc_template.render_unicode(zone=zone,
				project_name = prj.name,
				uses = uses)
				)
		out_file.close()
		
def create_aggregated_RC(path, bldg_list, package_name, model_name, RC_package, RC_model):
	lookup = TemplateLookup(directories=["\\aggr_code_templates\\"])
	aggr_template = Template(
		filename="\\aggr_code_templates\\Aggregated_R2CW_mpc",
		lookup=lookup)
	
	
	utilities.create_path(os.path.join(path,package_name))
		
	out_file = open(os.path.join(path, package_name, package_name + ".mo"), 'w')
	
	out_file.write(aggr_template.render_unicode(
			package_name = package_name,
			model_name = model_name,
			numbuilds = len(bldg_list),
            RC_model = RC_model,
			RC_package = RC_package,
			bldg_list=bldg_list)
			)
	out_file.close()

def main():

	prj = Project(load_data=True)
	prj.name = "ResidentialCommunityUK_rad"
	
	# Building types: detached, terrace, office_lowenergy-early1980s, office_highcost-mid1980s.
	
	# Community created based on
	
	prj = load_namespace('teaser_prj_residentialUK')
	prj.name = "ResidentialCommunityUK_rad_2elements"
	
	prj.used_library_calc = 'IBPSA'
	prj.number_of_elements_calc = 3
	
	prj.weather_file_path = os.path.join('path_to_weather_file', 'Nottingham_TRY.mos')

	prj.calc_all_buildings(raise_errors=True)
	store_namespace('teaser_prj_residential',prj)
	
	bldg_list=[]
	for bldg in prj.buildings:
		bldg_list.append(bldg.name)
	store_namespace('teaser_bldgs_residential',bldg_list)

	prj.export_parameters_txt(path="\\models")
	
	prj.export_ibpsa(
					internal_id=None,
					path="\models\\"
					)
	
	for bldg in prj.buildings:
		for zone in bldg.thermal_zones:
			path = os.path.join("\models\\", prj.name)
			create_ibpsa_mpc_model(prj,bldg,zone,path=path)
			create_ibpsa_PI_model(prj,bldg,zone,path=path)
	
main()