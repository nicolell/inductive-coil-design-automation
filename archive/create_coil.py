from src.coil_util import *

# creates coil starting from the inside, might not ensure the exact outer diameter given

def make_full_turns(start_x, start_y, diameter, size, spacing, turns, adhere_strictly=True):
	text = initialize_file()
	x = start_x
	y = start_y
	offset = size + spacing
	lines = []

	while True:
		if len(lines) > 0:
			xx, yy, xx2, yy2 = lines[-1]
			mul = 2 if adhere_strictly else 1
			off = mul* (size + spacing) if int(turns) - turns == 0 else (mul+1) * (size + spacing)
			# TODO adjust condition?: currently the final diameter may a bit bigger than the input one, is this okay or should I cut it off before so that it's always <=?
			if abs(xx - xx2) + off >= diameter or abs(yy - yy2) + off >= diameter:
				#print(abs(xx - xx2))
				#print(abs(yy - yy2))
				#print("current turn", full_turn)
				break

		# Draw four sides of the square, forming a spiral with spacing between turns
		# text = make_line(text, x, y, x + offset, y)  # Go right
		lines.append((x, y, x + offset, y))
		x += offset  # Update x to end of this line

		#text = make_line(text, x, y, x, y + offset)  # Go up
		lines.append((x, y, x, y + offset))
		y += offset  # Update y to end of this line

		offset += 2 * spacing  # Increase offset to add spacing

		#text = make_line(text, x, y, x - offset, y)  # Go left
		lines.append((x, y, x - offset, y))
		x -= offset  # Update x to end of this line

		#text = make_line(text, x, y, x, y - offset)  # Go down
		lines.append((x, y, x, y - offset))
		y -= offset  # Update y to end of this line

		# Increase offset again for the next loop
		offset += 2 * spacing
	
	return lines, offset, x, y


def make_partial_turns(text, x, y, offset, spacing, lines, turns, line_width, layer):
		# Handle any partial turn if needed
	frac_turn = turns - int(turns)
	if frac_turn != 0:
		if frac_turn >= 1/4:
			text = make_line(text, x, y, x + offset, y, line_width, layer)  # Go right
			lines.append((x, y, x + offset, y))
			x += offset  # Update x to end of this line
			frac_turn -= 1/4
		else: 
			text = make_line(text, x, y, x + offset * frac_turn, y, line_width, layer)
			lines.append((x, y, x + offset * frac_turn, y))
			return text, lines

		if frac_turn >= 1/4:
			text = make_line(text, x, y, x, y + offset, line_width, layer)  # Go up
			lines.append((x, y, x, y + offset))
			y += offset  # Update y to end of this line
			frac_turn -= 1/4
		else:
			text = make_line(text, x, y, x, y + offset * frac_turn, line_width, layer)
			lines.append((x, y, x, y + offset * frac_turn))
			return text, lines
	
		if frac_turn >= 1/4:
			offset += 2 * spacing  # Increase offset to add spacing

			text = make_line(text, x, y, x - offset, y, line_width, layer)  # Go left
			lines.append((x, y, x - offset, y))
			x -= offset  # Update x to end of this line
			frac_turn -= 1/4
		else: 
			text = make_line(text, x, y, x - offset * frac_turn, y, line_width, layer)
			lines.append((x, y, x - offset * frac_turn, y))
			return text, lines

		if frac_turn >= 1/4:
			text = make_line(text, x, y, x, y - offset, line_width, layer)  # Go down
			lines.append((x, y, x, y - offset))
		else: 
			text = make_line(text, x, y, x, y - offset * frac_turn, line_width, layer)
			lines.append((x, y, x, y - offset * frac_turn))
	return text, lines



def square_spiral(start_x, start_y, diameter=10, size=1.27, drill=0.5, spacing=1.27, turns=5, adhere_strictly=True, layers=None):
	diameter *= 10 # convert to cm
	if layers is None:
		layers = ["F.Cu", "B.Cu"]

	text = initialize_file()  # Initialize the file or canvas to draw on

	# make turns until diameter reached
	lines, offset, x, y = make_full_turns(start_x=start_x, start_y=start_y, diameter=diameter, size=size, spacing=spacing, turns=turns, adhere_strictly=adhere_strictly)

	# get number of lines to be created: 1 turn = 4 lines for square shape
	num_turns = int(turns) * 4
	# take the nast num_turns lines and draw them
	start_index = 0 if len(lines)-num_turns < 0 else len(lines)-num_turns
	for x_start, y_start, x_end, y_end in lines[start_index:]:
		text = make_line(text, x_start, y_start, x_end, y_end, size, layers[0])

	# add via in the origin of the coil
	via_x, via_y, _, _ = lines[start_index]
	text = make_via(text,via_x, via_y, size, drill, layers)

	# if applicable, make partial turns
	text, lines = make_partial_turns(text=text, x=x, y=y, offset=offset, spacing=spacing, lines=lines, turns=turns, line_width=size, layer=layers[0])

	# add pinheader at the end point of the coil
	_, _, _, pin_y = lines[-1]
	pin_x, _, _, _ = lines[-4]
	text = make_pinheader(text, pin_x, pin_y, layer=layers[0])
	# connect bottom layer to via and pinheader
	#text = make_line(text, via_x, via_y, pin_x - 2.54, via_y, size, layer=layers[-1])
	#text = make_line(text, pin_x - 2.54, via_y, pin_x - 2.54, pin_y, size, layer=layers[-1])
	text = make_line(text, via_x, via_y, via_x, pin_y, size, layer=layers[-1])
	text = make_line(text, via_x, pin_y, pin_x, pin_y, size, layer=layers[-1])
	
	return text


if __name__ == '__main__':
    #text = initialize_file()
	NAME = '../results/TEST3'
	start_x = 100
	start_y = 100
    
	#text = square_spiral(start_x=start_x, start_y=start_y, diameter=30, size=1.27, drill=0.5, spacing=1.27, turns=4.8)
	text = square_spiral(start_x=start_x, start_y=start_y, turns=15, diameter=5, adhere_strictly=True)
	print_to_file(outfile=NAME, text=text)
