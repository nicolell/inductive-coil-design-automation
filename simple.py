

def initialize_file():
    return """(kicad_pcb
	(version 20240108)
	(generator "pcbnew")
	(generator_version "8.0")
	(general
		(thickness 1.6)
		(legacy_teardrops no)
	)
	(paper "A4")
	(layers
		(0 "F.Cu" signal)
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


def make_line(text, start_x, start_y, end_x, end_y):
    seg = f"""(segment
		(start {start_x} {start_y})
		(end {end_x} {end_y})
		(width 1.27)
		(layer "F.Cu")
		(net 0)
	)
"""
    return text + seg
    
def make_via(text, x, y):
    via = f"""(via
		(at {x} {y})
		(size 1.27)
		(drill 0.5)
		(layers "F.Cu" "B.Cu")
		(net 0)
	)
    """
    return text + via

def square_spiral(start_x, start_y, diameter, size, spacing, turns):
	# TODO add vias in specified positions & maybe lines to the outside to connect to bottom layer

	text = initialize_file()  # Initialize the file or canvas to draw on

	#if int(diameter / (int(turns) * (spacing + size))) < 1:
		# must start spiral at other x,y and leave hollow space in the middle


	x = start_x
	y = start_y
	offset = size + spacing  # Start with the initial line length as the "size"
	
	for full_turn in range(int(turns)):
		# Draw four sides of the square, forming a spiral with spacing between turns
		text = make_line(text, x, y, x + offset, y)  # Go right
		x += offset  # Update x to end of this line

		text = make_line(text, x, y, x, y + offset)  # Go up
		y += offset  # Update y to end of this line

		offset += 2 * spacing  # Increase offset to add spacing

		text = make_line(text, x, y, x - offset, y)  # Go left
		x -= offset  # Update x to end of this line

		text = make_line(text, x, y, x, y - offset)  # Go down
		y -= offset  # Update y to end of this line

		# Increase offset again for the next loop
		offset += 2 * spacing  

	# Handle any partial turn if needed
	frac_turn = turns - int(turns)
	if frac_turn != 0:
		if frac_turn >= 1/4:
			text = make_line(text, x, y, x + offset, y)  # Go right
			x += offset  # Update x to end of this line
			frac_turn -= 1/4
		else: 
			text = make_line(text, x, y, x + offset * frac_turn, y)
			return text

		if frac_turn >= 1/4:
			text = make_line(text, x, y, x, y + offset)  # Go up
			y += offset  # Update y to end of this line
			frac_turn -= 1/4
		else:
			text = make_line(text, x, y, x, y + offset * frac_turn)
			return text
	
		if frac_turn >= 1/4:
			offset += 2 * spacing  # Increase offset to add spacing

			text = make_line(text, x, y, x - offset, y)  # Go left
			x -= offset  # Update x to end of this line
			frac_turn -= 1/4
		else: 
			text = make_line(text, x, y, x - offset * frac_turn, y)
			return text

		if frac_turn >= 1/4:
			text = make_line(text, x, y, x, y - offset)  # Go down
		else: 
			text = make_line(text, x, y, x, y - offset * frac_turn)

	return text


if __name__ == '__main__':
    #text = initialize_file()
    NAME = 'results/TEST2'
    start_x = 100
    start_y = 100
    
    text = square_spiral(start_x=start_x, start_y=start_y, diameter=10, size=1.27, spacing=1.27, turns=4.2)
    with open(f'{NAME}.kicad_pcb', 'w') as outfile:
            outfile.write(text + "\n)")
            outfile.close()
