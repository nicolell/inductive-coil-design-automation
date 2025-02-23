import math
import numpy as np
from magnetic_util import *

def initialize_file():
    return """(kicad_pcb
	(version 20240108)
	(generator "pcbnew")
	(generator_version "8.0")
	(general
		(thickness 1.6)
		(legacy_teardrops no)
	)
	(paper "A5")
	(layers
		(0 "F.Cu" signal)
		(1 "In1.Cu" signal)
		(2 "In2.Cu" signal)
		(3 "In3.Cu" signal)
		(4 "In4.Cu" signal)
		(31 "B.Cu" signal)
		(32 "B.Adhes" user "B.Adhesive")
		(33 "F.Adhes" user "F.Adhesive")
		(34 "B.Paste" user)
		(35 "F.Paste" user)
		(36 "B.SilkS" user "B.Silkscreen")
		(37 "F.SilkS" user "F.Silkscreen")
		(38 "B.Mask" user)
		(39 "F.Mask" user)
		(40 "Dwgs.User" user "User.Drawings")
		(41 "Cmts.User" user "User.Comments")
		(42 "Eco1.User" user "User.Eco1")
		(43 "Eco2.User" user "User.Eco2")
		(44 "Edge.Cuts" user)
		(45 "Margin" user)
		(46 "B.CrtYd" user "B.Courtyard")
		(47 "F.CrtYd" user "F.Courtyard")
		(48 "B.Fab" user)
		(49 "F.Fab" user)
		(50 "User.1" user)
		(51 "User.2" user)
		(52 "User.3" user)
		(53 "User.4" user)
		(54 "User.5" user)
		(55 "User.6" user)
		(56 "User.7" user)
		(57 "User.8" user)
		(58 "User.9" user)
	)
	(setup
		(stackup
			(layer "F.SilkS"
				(type "Top Silk Screen")
			)
			(layer "F.Paste"
				(type "Top Solder Paste")
			)
			(layer "F.Mask"
				(type "Top Solder Mask")
				(thickness 0.01)
			)
			(layer "F.Cu"
				(type "copper")
				(thickness 0.035)
			)
			(layer "dielectric 1"
				(type "prepreg")
				(thickness 0.1)
				(material "FR4")
				(epsilon_r 4.5)
				(loss_tangent 0.02)
			)
			(layer "In1.Cu"
				(type "copper")
				(thickness 0.035)
			)
			(layer "dielectric 2"
				(type "core")
				(thickness 0.535)
				(material "FR4")
				(epsilon_r 4.5)
				(loss_tangent 0.02)
			)
			(layer "In2.Cu"
				(type "copper")
				(thickness 0.035)
			)
			(layer "dielectric 3"
				(type "prepreg")
				(thickness 0.1)
				(material "FR4")
				(epsilon_r 4.5)
				(loss_tangent 0.02)
			)
			(layer "In3.Cu"
				(type "copper")
				(thickness 0.035)
			)
			(layer "dielectric 4"
				(type "core")
				(thickness 0.535)
				(material "FR4")
				(epsilon_r 4.5)
				(loss_tangent 0.02)
			)
			(layer "In4.Cu"
				(type "copper")
				(thickness 0.035)
			)
			(layer "dielectric 5"
				(type "prepreg")
				(thickness 0.1)
				(material "FR4")
				(epsilon_r 4.5)
				(loss_tangent 0.02)
			)
			(layer "B.Cu"
				(type "copper")
				(thickness 0.035)
			)
			(layer "B.Mask"
				(type "Bottom Solder Mask")
				(thickness 0.01)
			)
			(layer "B.Paste"
				(type "Bottom Solder Paste")
			)
			(layer "B.SilkS"
				(type "Bottom Silk Screen")
			)
			(copper_finish "None")
			(dielectric_constraints no)
		)
		(pad_to_mask_clearance 0)
		(allow_soldermask_bridges_in_footprints no)
		(pcbplotparams
			(layerselection 0x00010fc_ffffffff)
			(plot_on_all_layers_selection 0x0000000_00000000)
			(disableapertmacros no)
			(usegerberextensions no)
			(usegerberattributes yes)
			(usegerberadvancedattributes yes)
			(creategerberjobfile yes)
			(dashed_line_dash_ratio 12.000000)
			(dashed_line_gap_ratio 3.000000)
			(svgprecision 4)
			(plotframeref no)
			(viasonmask no)
			(mode 1)
			(useauxorigin no)
			(hpglpennumber 1)
			(hpglpenspeed 20)
			(hpglpendiameter 15.000000)
			(pdf_front_fp_property_popups yes)
			(pdf_back_fp_property_popups yes)
			(dxfpolygonmode yes)
			(dxfimperialunits yes)
			(dxfusepcbnewfont yes)
			(psnegative no)
			(psa4output no)
			(plotreference yes)
			(plotvalue yes)
			(plotfptext yes)
			(plotinvisibletext no)
			(sketchpadsonfab no)
			(subtractmaskfromsilk no)
			(outputformat 1)
			(mirror no)
			(drillshape 1)
			(scaleselection 1)
			(outputdirectory "")
		)
	)
	(net 0 "")
"""

def make_line(text, start_x, start_y, end_x, end_y, line_width=1.27, layer="F.Cu"):
    seg = f"""(segment
		(start {start_x} {start_y})
		(end {end_x} {end_y})
		(width {line_width})
		(layer "{layer}")
		(net 0)
	)
"""
    return text + seg

def save_lines(start_x, start_y, end_x, end_y, save_arr):
	#start = np.array([start_x, start_y])
	#end = np.array([end_x, end_y])

	#tmp = np.array([[start_x, start_y, 0], [end_x, end_y, 0]])
	#save_arr.append(tmp)
	save_arr.append(f"{start_x/10:.2f},{start_y/10:.2f},0,1")
	#save_arr.append(f"{end_x:.2f},{end_y:.2f},0,1")

def write_lines_to_file(file_name, lines, mode='w'):
	d = open(file_name, mode)
	for line in lines:
		d.write(line + '\n')
	d.close()


def make_arc(text, start, mid, stop, line_width=1.27, layer="F.Cu"):
	start_x, start_y = start
	mid_x, mid_y = mid
	stop_x, stop_y = stop
	seg = f"""(gr_arc
		(start {start_x} {start_y})
		(mid {mid_x} {mid_y})
		(end {stop_x} {stop_y})
		(stroke
			(width {line_width})
			(type default)
		)
		(layer "{layer}")
	)
	"""
	return text + seg
    
def make_via(text, x, y, width=1.27, drill=0.5, layers=None):
	if layers is None:
		layers = ["F.Cu", "B.Cu"]
	layers = [f"\"{l}\"" for l in layers]
	layer_str = ' '.join(layers)
	via = f"""(via
		(at {x} {y})
		(size {width})
		(drill {drill})
		(layers {layer_str})
		(net 0)
	)"""
	return text + via


def make_pinheader(text, x, y, layer="F.Cu", angle=0): # 90 is horizontal
	pin = f"""(footprint "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical"
		(layer "{layer}")
		(uuid "6eb7a419-c70b-48ac-bdb9-ad2a813fb730")
		(at {x} {y} -{angle})
		(descr "Through hole straight pin header, 1x02, 2.54mm pitch, single row")
		(tags "Through hole pin header THT 1x02 2.54mm single row")
		(property "Reference" "REF**"
			(at 2.54 -2.54 {angle})
			(layer "F.SilkS")
			(uuid "0680d32b-a290-48eb-93ca-355456b61191")
			(effects
				(font
					(size 1 1)
					(thickness 0.15)
				)
			)
		)
		(property "Value" "PinHeader_1x02_P2.54mm_Vertical"
			(at 0 4.87 {angle})
			(layer "F.Fab")
			(hide yes)
			(uuid "740ee695-8230-4635-945d-42ac37bfcb3c")
			(effects
				(font
					(size 1 1)
					(thickness 0.15)
				)
			)
		)
		(property "Footprint" "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical"
			(at 0 0 -{angle})
			(unlocked yes)
			(layer "F.Fab")
			(hide yes)
			(uuid "528fc2a4-bdbb-4033-b541-03d2b0cd29f0")
			(effects
				(font
					(size 1.27 1.27)
					(thickness 0.15)
				)
			)
		)
		(property "Datasheet" ""
			(at 0 0 -{angle})
			(unlocked yes)
			(layer "F.Fab")
			(hide yes)
			(uuid "832ba727-a2a3-4fb6-9277-da26167ed1f9")
			(effects
				(font
					(size 1.27 1.27)
					(thickness 0.15)
				)
			)
		)
		(property "Description" ""
			(at 0 0 -{angle})
			(unlocked yes)
			(layer "F.Fab")
			(hide yes)
			(uuid "81723a60-4c3b-40e4-a562-f5ab33c5ca2e")
			(effects
				(font
					(size 1.27 1.27)
					(thickness 0.15)
				)
			)
		)
		(attr through_hole)
		(fp_line
			(start -1.33 3.87)
			(end 1.33 3.87)
			(stroke
				(width 0.12)
				(type solid)
			)
			(layer "F.SilkS")
			(uuid "8af0ab53-c557-49b9-901c-d8ca81fde64f")
		)
		(fp_line
			(start -1.33 1.27)
			(end -1.33 3.87)
			(stroke
				(width 0.12)
				(type solid)
			)
			(layer "F.SilkS")
			(uuid "f6b104f0-b883-4dc5-bf77-e8ccebc5043e")
		)
		(fp_line
			(start -1.33 1.27)
			(end 1.33 1.27)
			(stroke
				(width 0.12)
				(type solid)
			)
			(layer "F.SilkS")
			(uuid "797a3d78-8b51-41e3-9e45-8511ae68195f")
		)
		(fp_line
			(start 1.33 1.27)
			(end 1.33 3.87)
			(stroke
				(width 0.12)
				(type solid)
			)
			(layer "F.SilkS")
			(uuid "95dd8e1b-880a-4727-94e2-b733f9426049")
		)
		(fp_line
			(start -1.33 0)
			(end -1.33 -1.33)
			(stroke
				(width 0.12)
				(type solid)
			)
			(layer "F.SilkS")
			(uuid "32397c4b-e02b-424f-8344-a90b88116759")
		)
		(fp_line
			(start -1.33 -1.33)
			(end 0 -1.33)
			(stroke
				(width 0.12)
				(type solid)
			)
			(layer "F.SilkS")
			(uuid "1d6741bb-df91-4e3a-ad65-6c6ec0c2cd84")
		)
		(fp_line
			(start -1.8 4.35)
			(end 1.8 4.35)
			(stroke
				(width 0.05)
				(type solid)
			)
			(layer "F.CrtYd")
			(uuid "2fb36f01-0e6e-4752-9828-c37c530ed6bd")
		)
		(fp_line
			(start 1.8 4.35)
			(end 1.8 -1.8)
			(stroke
				(width 0.05)
				(type solid)
			)
			(layer "F.CrtYd")
			(uuid "5e27fc63-1f3f-4fd5-b127-611919e71a2c")
		)
		(fp_line
			(start -1.8 -1.8)
			(end -1.8 4.35)
			(stroke
				(width 0.05)
				(type solid)
			)
			(layer "F.CrtYd")
			(uuid "4c8c780f-32bf-4d8f-8806-dd5840ec6e32")
		)
		(fp_line
			(start 1.8 -1.8)
			(end -1.8 -1.8)
			(stroke
				(width 0.05)
				(type solid)
			)
			(layer "F.CrtYd")
			(uuid "d08eeb09-cbd8-4e86-83f2-bd7c0c16bc81")
		)
		(fp_line
			(start -1.27 3.81)
			(end -1.27 -0.635)
			(stroke
				(width 0.1)
				(type solid)
			)
			(layer "F.Fab")
			(uuid "0ba514bb-90e1-45a3-a592-5d33ec89770b")
		)
		(fp_line
			(start 1.27 3.81)
			(end -1.27 3.81)
			(stroke
				(width 0.1)
				(type solid)
			)
			(layer "F.Fab")
			(uuid "14688920-1caf-43aa-9baa-67988222c648")
		)
		(fp_line
			(start -1.27 -0.635)
			(end -0.635 -1.27)
			(stroke
				(width 0.1)
				(type solid)
			)
			(layer "F.Fab")
			(uuid "50305548-a49d-43db-b304-aa4971858d82")
		)
		(fp_line
			(start -0.635 -1.27)
			(end 1.27 -1.27)
			(stroke
				(width 0.1)
				(type solid)
			)
			(layer "F.Fab")
			(uuid "5779fa26-a86b-463f-b925-0141e598636b")
		)
		(fp_line
			(start 1.27 -1.27)
			(end 1.27 3.81)
			(stroke
				(width 0.1)
				(type solid)
			)
			(layer "F.Fab")
			(uuid "3ec9be6e-75d5-4c17-b487-825ff9c2c8fa")
		)"""
	pin += """
		(fp_text user "${REFERENCE}"
			(at 0 1.27 0)
			(layer "F.Fab")
			(uuid "55633b86-4004-4522-b28a-1a3d9cbc57a8")
			(effects
				(font
					(size 1 1)
					(thickness 0.15)
				)
			)
		)
		(pad "1" thru_hole rect
			(at 0 0 270)
			(size 1.7 1.7)
			(drill 1)
			(layers "*.Cu" "*.Mask")
			(remove_unused_layers no)
			(uuid "da626a66-dbf0-4ddb-8151-45b2d8a02aa6")
		)
		(pad "2" thru_hole oval
			(at 0 2.54 270)
			(size 1.7 1.7)
			(drill 1)
			(layers "*.Cu" "*.Mask")
			(remove_unused_layers no)
			(uuid "7f58b30c-f9fb-4563-b0da-aebad8ab491d")
		)
		(model "${KICAD8_3DMODEL_DIR}/Connector_PinHeader_2.54mm.3dshapes/PinHeader_1x02_P2.54mm_Vertical.wrl"
			(offset
				(xyz 0 0 0)
			)
			(scale
				(xyz 1 1 1)
			)
			(rotate
				(xyz 0 0 0)
			)
		)
	)
    """
	return text + pin


def printUsage():
    s = """
    Usage:

            python3 src/new_coil.py -option value

                    -vN export an N-gonal inductor instead of default helical inductor

                        i.e. -v3 for triangle, -v4 for square, -v6 for hexagon

                    -i long  inner diameter of coil in microns

                    -o long  outer diameter of coil in microns

                    -w long  track width in microns

                    -n long  number of turns

                    -g long  track gap in microns

                    -d long  via drill in mm

                    -l long  length of segment used to approximate circular arc in microns

                    -h prints this

    Example usage:

            python3 src/new_coil.py -o 50000 -w 1270 -v7 -n 5 -g 1270 -d 0.5

            produces a heptagonal coil with 5 turns, 50 mm outer diameter, 1.27 mm track width, 1.27 mm track grap,  0.5 mm via drill
    """
    print(s)




def print_to_file(outfile, text):
	with open(f'{outfile}.kicad_pcb', 'w') as outfile:
            outfile.write(text + "\n)")
            outfile.close()