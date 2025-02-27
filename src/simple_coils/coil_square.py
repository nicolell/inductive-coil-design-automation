from coil import *

class Square_Coil(Coil):
    def make_full_turns(self, start_x, start_y, initial_diameter):
        x = start_x
        y = start_y
        offset = initial_diameter
        lines = []

        # Do all full turns
        for turn in range(int(self.turns)):
            # Draw four sides of the square, forming a spiral with spacing between turns
            inner_diam = offset - self.size
            if inner_diam <= 0:
                print("too many turns! coil can't be created fully")
                return exit(-1)

            # Go down
            lines.append((x, y, x, y + offset))
            y += offset  # Update y to end of this line

            # Go right
            lines.append((x, y, x + offset, y))
            x += offset  # Update x to end of this line

            offset -= self.spacing + self.size  # Reduce offset to add spacing

            # Go up
            lines.append((x, y, x, y - offset))
            y -= offset  # Update y to end of this line

            # Go left
            lines.append((x, y, x - offset, y))
            x -= offset  # Update x to end of this line

            # Reduce offset again for the next loop
            offset -= self.spacing + self.size
        print("Inner diameter:", round(inner_diam,2))
        return lines, offset, x, y


    def make_partial_turns(self):
        # <=1 turn -> length of segment is at most diameter
        # Handle any partial turn if needed
        frac_turn = self.turns - int(self.turns)
        initial_offset = self.diameter
        offset = self.diameter
        x = self.x
        y = self.y
        final_x = self.x
        final_y = self.y
        if frac_turn >= 0.75: # third line has length diameter
            # first line should be smaller
            offset -= self.spacing + self.size
            initial_offset = offset - (self.spacing + self.size)
            self.text = make_line(self.text, x, y, x + offset, y, self.size, self.layers[0])  # Go right
            x += offset  # Update x to end of this line

            self.text = make_line(self.text, x, y, x, y + offset, self.size, self.layers[0])  # Go up
            self.lines.append((x, y, x, y + offset))
            y += offset  # Update y to end of this line

            offset += self.spacing + self.size  # Increase offset to add spacing
            self.text = make_line(self.text, x, y, x - offset, y, self.size, self.layers[0])  # Go left
            self.lines.append((x, y, x - offset, y))
            x -= offset  # Update x to end of this line

            frac_turn -= 0.75
            self.text = make_line(self.text, x, y, x, y - offset * frac_turn, self.size, self.layers[0])
            final_x = x
            final_y = y - offset * frac_turn
            self.lines.append((x, y, x, y - offset * frac_turn))
            last_dir = 0 # 0 for up/down

        elif frac_turn >= 0.5: # first, second line have length diameter
            # use full offset for partial turn
            initial_offset = offset - (self.spacing + self.size)
            self.text = make_line(self.text, x, y, x + offset, y, self.size, self.layers[0])  # Go right
            x += offset  # Update x to end of this line

            self.text = make_line(self.text, x, y, x, y + offset, self.size, self.layers[0])  # Go up
            self.lines.append((x, y, x, y + offset))
            y += offset  # Update y to end of this line

            offset += (self.spacing + self.size)  # Increase offset to add spacing
            frac_turn -= 0.5
            self.text = make_line(self.text, x, y, x - offset * frac_turn, y, self.size, self.layers[0])  # Go left
            self.lines.append((x, y, x - offset * frac_turn, y))
            x -= offset * frac_turn  # Update x to end of this line
            final_x = x
            final_y = y 
            last_dir = 0 # 0 for up/down
        elif frac_turn >= 0.25: # first line has length diameter
            # use full offset for partial turn
            initial_offset = offset - (self.spacing + self.size)
            self.text = make_line(self.text, x, y, x + offset, y, self.size, self.layers[0])  # Go right
            # lines.append((x, y, x + offset, y))
            x += offset  # Update x to end of this line

            frac_turn -= 0.25
            self.text = make_line(self.text, x, y, x, y + offset * frac_turn, self.size, self.layers[0])  # Go up
            self.lines.append((x, y, x, y + offset * frac_turn))
            y += offset * frac_turn  # Update y to end of this line

            final_x = x
            final_y = y # - offset * frac_turn
            last_dir = 1 # 0 for up/down
        else:
            self.text = make_line(self.text, self.x, self.y, self.x + self.diameter * frac_turn, self.y, self.size, self.layers[0])
            self.lines.append((self.x, self.y, self.x + self.diameter * frac_turn, self.y))
            final_x = self.x + self.diameter * frac_turn
            final_y = self.y
            last_dir = 1

        return self.text, self.lines, initial_offset, final_x, final_y, last_dir


    def create_coil(self):
        # self.diameter *= 10 # convert to cm
        if self.layers is None:
            self.layers = ["F.Cu", "B.Cu"]

        text = initialize_file()  # Initialize the file or canvas to draw on

        lines = []
        # if applicable, make partial turns
        text, lines, initial_offset, final_x, final_y, last_dir = self.make_partial_turns()

        # make turns until diameter reached
        lines, offset, x, y = self.make_full_turns(start_x=self.x, start_y=self.y, initial_diameter=initial_offset)

        # get number of lines to be created: 1 turn = 4 lines for square shape
        num_turns = int(self.turns) * 4
        # take the nast num_turns lines and draw them
        start_index = 0 if len(lines)-num_turns < 0 else len(lines)-num_turns
        for x_start, y_start, x_end, y_end in lines[start_index:]:
            text = make_line(text, x_start, y_start, x_end, y_end, self.size, self.layers[0])

        # add via in the origin of the coil
        _, _, via_x, via_y = lines[-1]

        text = make_via(text,via_x, via_y, self.size, self.drill, self.layers)

        # add pinheader at the end point of the coil
        if int(self.turns) - self.turns == 0:
            _, pin_y, _, _ = lines[0]
            _, _, pin_x, _ = lines[3]
        else:
            pin_x = final_x
            pin_y = final_y
        
        # connect bottom layer to via and pinheader
        if int(self.turns) - self.turns == 0:
            text = make_pinheader(text, pin_x, pin_y, layer=self.layers[0])
            text = make_line(text, via_x, via_y, via_x, pin_y, self.size, layer=self.layers[-1])
            text = make_line(text, via_x, pin_y, pin_x, pin_y, self.size, layer=self.layers[-1])
        else:
            
            if last_dir == 0:
                text = make_pinheader(text, pin_x, pin_y, layer=self.layers[0])
                pin_x -= 2.54
                text = make_line(text, via_x, via_y, pin_x, via_y, self.size, layer=self.layers[-1])
                text = make_line(text, pin_x, via_y, pin_x, pin_y, self.size, layer=self.layers[-1])
            else:
                text = make_pinheader(text, pin_x + 2.54, pin_y, layer=self.layers[0])
                pin_x += 2.54
                text = make_line(text, pin_x, via_y, pin_x, pin_y, self.size, layer=self.layers[-1])
                text = make_line(text, via_x, via_y, pin_x, via_y, self.size, layer=self.layers[-1])     
        return text


if __name__ == '__main__':
    # adjust parameters as needed
    diameter = 45 # mm
    spacing = 1.27 # mm
    size = 1.27 # mm
    turns = 9 
    NAME = f'results/{turns}_turn_square_coil'

    square = Square_Coil(diameter=diameter, spacing=spacing, size=size, turns=turns)
    text = square.create_coil()
    print_to_file(outfile=NAME, text=text)
    print("Coil in file: ", NAME)