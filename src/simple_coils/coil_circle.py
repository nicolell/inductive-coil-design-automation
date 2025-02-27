from coil import *

class Circle_Coil(Coil):

    def make_arc(self, start, mid, stop):
        start_x, start_y = start
        mid_x, mid_y = mid
        stop_x, stop_y = stop
        seg = f"""(gr_arc
            (start {start_x} {start_y})
            (mid {mid_x} {mid_y})
            (end {stop_x} {stop_y})
            (stroke
                (width {self.size})
                (type default)
            )
            (layer "{self.layers[0]}")
        )
        """
        self.text = self.text + seg
        return self.text

    def make_full_turns(self, layer_index=0, clockwise=True):
        center_x = self.x
        center_y = self.y
        final_x = center_x
        final_y = center_y
        
        offset = self.spacing + self.size
        frac_turn = self.turns - int(self.turns)
        diameter = self.diameter
        if frac_turn !=  0:
            diameter -= offset
        radius = diameter/ 2 - offset/2
        
        print(f"Inner Radius: {radius}")
        # Do all full turns
        m = -1 if layer_index % 2 != 0 else 1
        m *= 1 if clockwise else -1
        
        for turn in range(int(self.turns)):
            if turn == 0:
                self.origin = (radius + offset + center_x, center_y-2.54) # x,y origin
            if radius <= offset:
                print("radius too small")
                break
            if not bool(m + 1):
                self.make_arc(start=(radius + center_x, center_y), 
                            mid=(center_x, center_y - m * radius), 
                            stop=(-radius + center_x, center_y))
                self.make_arc(start=(-radius + center_x, center_y), 
                            mid=(offset / 2 + center_x, m * (radius + offset / 2) + center_y), 
                            stop=(radius + offset + center_x, center_y))
            else:
                self.make_arc(start=(-radius + center_x, center_y), 
                            mid=(center_x, center_y - m * radius), 
                            stop=(radius + center_x, center_y))
                self.make_arc(start=(radius + offset + center_x, center_y), 
                            mid=(offset / 2 + center_x, m * (radius + offset / 2) + center_y), 
                            stop=(-radius + center_x, center_y))
            self.end = (radius + center_x, center_y)
            radius -= offset
        final_x = -radius + center_x
        final_y = center_y

        return self.lines, offset, final_x, final_y


    def make_partial_turns(self, layer_index=0, clockwise=True):
        # <=1 turn -> length of segment is at most diameter
        # Handle any partial turn if needed
        frac_turn = self.turns - int(self.turns)
        initial_offset = self.diameter
        offset = self.diameter
        center_x = self.x + self.diameter / 2 + self.size
        center_y = self.y
        final_x = self.x
        final_y = self.y
        radius = self.diameter/ 2
        center_x -= radius + self.size
        m = -1 if layer_index % 2 != 0 else 1
        m *= 1 if clockwise else -1
        if frac_turn == 1:
            # this performs a full turn
            radius += self.size 
            offset = self.size + self.spacing
            if not bool(m + 1):
                self.make_arc(start=(radius + center_x, center_y), 
                            mid=(center_x, center_y - m * radius ), 
                            stop=(-radius + center_x, center_y))
                self.make_arc(start=(-radius + center_x, center_y), 
                            mid=(offset / 2 + center_x, m * (radius+ offset / 2) + center_y), 
                            stop=(radius + offset + center_x, center_y))
            else:
                self.make_arc(start=(-radius+ center_x, center_y), 
                            mid=(center_x, center_y - m * radius ), 
                            stop=(radius + center_x, center_y))
                self.make_arc(start=(radius  + offset + center_x, center_y), 
                            mid=(offset / 2 + center_x, m * (radius  + offset / 2) + center_y), 
                            stop=(-radius  + center_x, center_y))
            last_dir = 0
        elif frac_turn == 0.5:
            # this performs half a turn
            radius += self.size 
            offset = self.size + self.spacing
            if not bool(m + 1):
                self.make_arc(start=(radius + center_x, center_y), 
                            mid=(center_x, center_y - m * radius ), 
                            stop=(-radius + center_x, center_y))
            else:
                self.make_arc(start=(-radius+ center_x, center_y), 
                            mid=(center_x, center_y - m * radius ), 
                            stop=(radius + center_x, center_y))
            last_dir = 1
        else: 
            # TODO allow for other fractional turns
            last_dir = 1
            pass

        return self.text, self.lines, initial_offset, final_x, final_y, last_dir


    def create_coil(self):
        #self.diameter *= 10 # convert to cm
        if self.layers is None:
            self.layers = ["F.Cu", "B.Cu"]

        text = initialize_file()  # header

        lines = []
        # if applicable, make partial turns
        text, lines, initial_offset, final_x, final_y, last_dir = self.make_partial_turns()

        # make turns until diameter reached
        lines, offset, final_x, final_y = self.make_full_turns()

        # get number of lines to be created: 1 turn = 4 lines for square shape
        num_turns = int(self.turns) 
        # take the last num_turns lines and draw them
        start_index = 0 if len(lines)-num_turns < 0 else len(lines)-num_turns
        for x_start, y_start, x_end, y_end in lines[start_index:]:
            text = make_line(text, x_start, y_start, x_end, y_end, self.size, self.layers[0])

        text = ""
        # add via in the origin of the coil
        via_x, via_y = self.end
        text = make_via(text,via_x, via_y, self.size, self.drill, self.layers)

        # add pinheader at the end point of the coil
        if int(self.turns) - self.turns == 0:
            pin_x, pin_y = self.origin
        else:
            pin_x = final_x
            pin_y = final_y

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
        
        self.text += text
        
        return self.text


if __name__ == '__main__':
    # adjust parameters as needed
    diameter = 45 # mm
    spacing = 1.27 # mm
    size = 1.27 # mm
    turns = 9
    NAME = f'results/{turns}_turn_circle_coil'

    circle = Circle_Coil(diameter=diameter, spacing=spacing, size=size, turns=turns)
    text = circle.create_coil()
    print_to_file(outfile=NAME, text=text)
    print("Coil in file: ", NAME)