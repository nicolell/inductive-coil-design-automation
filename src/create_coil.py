from coil_util import *

# creates coil starting from the outside, ensuring the correct diameter

def make_full_turns(start_x, start_y, diameter, size, spacing, turns, adhere_strictly=True):
	text = initialize_file()
	x = start_x
	y = start_y
	offset = diameter
	lines = []

	# Do all full turns
	for turn in range(int(turns)):
		# Draw four sides of the square, forming a spiral with spacing between turns
		inner_diam = offset - size
		#print("inner diameter:", inner_diam)
		if inner_diam <= 0:
			print("too many turns! coil can't be created fully")
			return exit(-1)

		# Go down
		lines.append((x, y, x, y + offset))
		y += offset  # Update y to end of this line

		# Go right
		lines.append((x, y, x + offset, y))
		x += offset  # Update x to end of this line

		offset -= spacing + size  # Reduce offset to add spacing

		# Go up
		lines.append((x, y, x, y - offset))
		y -= offset  # Update y to end of this line

		# Go left
		lines.append((x, y, x - offset, y))
		x -= offset  # Update x to end of this line

		# Reduce offset again for the next loop
		offset -= spacing + size



	print("inner diameter:", round(inner_diam,2))
	return lines, offset, x, y


def make_partial_turns(text, x, y, offset, spacing, lines, turns, line_width, layer):
	# <=1 turn -> length of segment is at most diameter
		# Handle any partial turn if needed
	frac_turn = turns - int(turns)
	initial_offset = offset
	final_x = x
	final_y = y
	if frac_turn >= 0.75: # third line has length diameter
		# first line should be smaller
		offset -= spacing * 2
		initial_offset = offset - 2* spacing
		text = make_line(text, x, y, x + offset, y, line_width, layer)  # Go right
		#lines.append((x, y, x + offset, y))
		x += offset  # Update x to end of this line

		text = make_line(text, x, y, x, y + offset, line_width, layer)  # Go up
		lines.append((x, y, x, y + offset))
		y += offset  # Update y to end of this line

		offset += 2 * spacing  # Increase offset to add spacing
		text = make_line(text, x, y, x - offset, y, line_width, layer)  # Go left
		lines.append((x, y, x - offset, y))
		x -= offset  # Update x to end of this line

		frac_turn -= 0.75
		print(frac_turn)
		print(offset * frac_turn)
		text = make_line(text, x, y, x, y - offset * frac_turn, line_width, layer)
		final_x = x
		final_y = y - offset * frac_turn
		lines.append((x, y, x, y - offset * frac_turn))
		last_dir = 0 # 0 for up/down

	elif frac_turn >= 0.5: # first, second line have length diameter
		# use full offset for partial turn
		initial_offset = offset - 2* spacing
		text = make_line(text, x, y, x + offset, y, line_width, layer)  # Go right
		#lines.append((x, y, x + offset, y))
		x += offset  # Update x to end of this line

		text = make_line(text, x, y, x, y + offset, line_width, layer)  # Go up
		lines.append((x, y, x, y + offset))
		y += offset  # Update y to end of this line

		offset += 2 * spacing  # Increase offset to add spacing
		frac_turn -= 0.5
		text = make_line(text, x, y, x - offset * frac_turn, y, line_width, layer)  # Go left
		lines.append((x, y, x - offset * frac_turn, y))
		x -= offset * frac_turn  # Update x to end of this line
		final_x = x
		final_y = y 
		last_dir = 0 # 0 for up/down
	elif frac_turn >= 0.25: # first line has length diameter
		# use full offset for partial turn
		initial_offset = offset - 2* spacing
		text = make_line(text, x, y, x + offset, y, line_width, layer)  # Go right
		#lines.append((x, y, x + offset, y))
		x += offset  # Update x to end of this line

		frac_turn -= 0.25
		text = make_line(text, x, y, x, y + offset * frac_turn, line_width, layer)  # Go up
		lines.append((x, y, x, y + offset * frac_turn))
		y += offset * frac_turn  # Update y to end of this line


		final_x = x
		final_y = y #- offset * frac_turn
		last_dir = 1 # 0 for up/down
	else:
		text = make_line(text, x, y, x - offset * frac_turn, y, line_width, layer)
		lines.append((x, y, x - offset * frac_turn, y))
		final_x = x - offset * frac_turn
		final_y = y
		last_dir = 1

	return text, lines, initial_offset, final_x, final_y, last_dir



def square_spiral(start_x, start_y, diameter=10, size=1.27, drill=0.5, spacing=1.27, turns=5, adhere_strictly=True, layers=None):
	diameter *= 10 # convert to cm
	if layers is None:
		layers = ["F.Cu", "B.Cu"]

	text = initialize_file()  # Initialize the file or canvas to draw on

	lines = []
	# if applicable, make partial turns
	text, lines, initial_offset, final_x, final_y, last_dir = make_partial_turns(text=text, x=start_x, y=start_y, offset=diameter, spacing=spacing, lines=lines, turns=turns, line_width=size, layer=layers[0])

	# make turns until diameter reached
	lines, offset, x, y = make_full_turns(start_x=start_x, start_y=start_y, diameter=initial_offset, size=size, spacing=spacing, turns=turns, adhere_strictly=adhere_strictly)

	# get number of lines to be created: 1 turn = 4 lines for square shape
	num_turns = int(turns) * 4
	# take the nast num_turns lines and draw them
	start_index = 0 if len(lines)-num_turns < 0 else len(lines)-num_turns
	for x_start, y_start, x_end, y_end in lines[start_index:]:
		text = make_line(text, x_start, y_start, x_end, y_end, size, layers[0])

	# add via in the origin of the coil
	_, _, via_x, via_y = lines[-1]

	text = make_via(text,via_x, via_y, size, drill, layers)


	# add pinheader at the end point of the coil
	#pin_y = final_y
	#pin_x = final_x
	if int(turns) - turns == 0:
		_, pin_y, _, _ = lines[0]
		_, _, pin_x, _ = lines[3]
	else:
		pin_x = final_x
		pin_y = final_y
		#pin_x += -2.54 if last_dir == 0 else 0
		#pin_y += 0 if last_dir == 0 else 
	
	# connect bottom layer to via and pinheader
	#text = make_line(text, via_x, via_y, pin_x - 2.54, via_y, size, layer=layers[-1])
	#text = make_line(text, pin_x - 2.54, via_y, pin_x - 2.54, pin_y, size, layer=layers[-1])
	if int(turns) - turns == 0:
		text = make_pinheader(text, pin_x, pin_y, layer=layers[0])
		text = make_line(text, via_x, via_y, via_x, pin_y, size, layer=layers[-1])
		text = make_line(text, via_x, pin_y, pin_x, pin_y, size, layer=layers[-1])
	else:
		
		if last_dir == 0:
			text = make_pinheader(text, pin_x, pin_y, layer=layers[0])
			pin_x -= 2.54
			text = make_line(text, via_x, via_y, pin_x, via_y, size, layer=layers[-1])
			text = make_line(text, pin_x, via_y, pin_x, pin_y, size, layer=layers[-1])
		else:
			text = make_pinheader(text, pin_x + 2.54, pin_y, layer=layers[0])
			pin_x += 2.54

			text = make_line(text, pin_x, via_y, pin_x, pin_y, size, layer=layers[-1])
			text = make_line(text, via_x, via_y, pin_x, via_y, size, layer=layers[-1])
	
	
	return text


if __name__ == '__main__':
    #text = initialize_file()
	NAME = '../results/TEST5'
	start_x = 100
	start_y = 100
    
	#text = square_spiral(start_x=start_x, start_y=start_y, diameter=30, size=1.27, drill=0.5, spacing=1.27, turns=4.8)
	text = square_spiral(start_x=start_x, start_y=start_y, turns=5, diameter=5, adhere_strictly=True)
	print_to_file(outfile=NAME, text=text)
