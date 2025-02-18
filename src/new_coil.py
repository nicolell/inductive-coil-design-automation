from math import log, pi, sqrt
import math
import sys
from coil_util import *

def main():
    # some default values
    innerDiameter = 27100  # microns
    outerDiameter = 32000  # microns
    segmentLength = 100  # 1mm length in microns
    turnsTotal = 9
    trackWidth = 1270  # microns
    trackGap = 1270  # microns
    drill = 0.5 # mm
    straight = True # force second layer to have two straight lines to get to the pinheader instead of a diagonal one
    vertices = 0
    pos_x = 100 # x coordinate to start the coil at
    pos_y = 100 # y coordinate to start the coil at
    lines = [] # array to save all lines in

    # we now parse arguments parsed via the command line
    if len(sys.argv) == 1:
        printUsage()
        sys.exit(0)

    counter = 1
    while counter < len(sys.argv):
        if sys.argv[counter].startswith("-n"):
            turnsTotal = float(sys.argv[counter + 1])
            counter += 2
        elif sys.argv[counter].startswith("-i"):
            innerDiameter = int(sys.argv[counter + 1])
            counter += 2
        elif sys.argv[counter].startswith("-o"):
            outerDiameter = int(sys.argv[counter + 1])
            counter += 2
        elif sys.argv[counter].startswith("-l"):
            segmentLength = int(sys.argv[counter + 1])
            counter += 2
        elif sys.argv[counter].startswith("-w"):
            trackWidth = int(sys.argv[counter + 1])
            counter += 2
        elif sys.argv[counter].startswith("-v"):
            vertices = int(sys.argv[counter][2:])
            if vertices in (1, 2):
                print("Assuming inductor is helical.")
                vertices = 0
            counter += 1
        elif sys.argv[counter].startswith("-g"):
            trackGap = int(sys.argv[counter + 1])
            counter += 2
        elif sys.argv[counter].startswith("-d"):
            drill = float(sys.argv[counter + 1])
            counter += 2
        elif sys.argv[counter].startswith("-s"):
            straight = False
            counter += 1
        else:
            printUsage()
            sys.exit(0)

    # some basic preliminaries for all scenarios

    # dynamically compute inner diameter s.t. outer diameter can be adhered to 
    if int(turnsTotal) == turnsTotal:
        innerDiameter = outerDiameter - 2.0 * (turnsTotal * trackWidth + (turnsTotal - 1) * trackGap)
    else:
        innerDiameter = outerDiameter - 2.0 * ((int(turnsTotal)+1) * trackWidth + (turnsTotal - 1) * trackGap)
    startRadius = (innerDiameter)/2.0 

    nextRadius = startRadius 

    # now some preliminaries for heliical inductors
    # we now sort out appropriate angular step sizes for the loops and
    # the loop spacings based on the inner and outer dimensions given
    theta = 0 
    nextTheta = 0 

    # we figure out the circumference, well, at least a reasonable
    # approximation of a real number using the set of long integers
    # circumference = pi * outerDiameter 

    # we base segments per loop on the outermost loop circumference
    segmentsPerLoop = pi*outerDiameter/segmentLength 
    # we figure out a step size in radians to step around the spiral
    # which is 2pi radians divided by number of segments
    deltaTheta = (2.0 * pi)/segmentsPerLoop 

    # we now define some flags
    nextTurnPlease = False 
    
    # if trackgap not given, calculate an appropriate one
    if not trackGap:
        if (turnsTotal > 1): # the usual scenario
            trackGap = ((outerDiameter - innerDiameter)/2.0 - (turnsTotal*trackWidth))/(turnsTotal-1)  # nm
        else: # stops a divide by zero error if only one loop requested
            trackGap = (innerDiameter/2.0)  # i.e. startRadius


    radiusIncrementPerTurn = (trackWidth+trackGap) 
    radiusIncrementPerSegment = radiusIncrementPerTurn/(segmentsPerLoop) 

    # we use x1,y1,x2,y2 as variables for the beginning and end coords of line segments
    x1 = 0 
    y1 = 0 
    x2 = 0 
    y2 = 0 
    # we use x1scaled,y1scaled,x2scaled,y2scaled as variables for
    # the beginning and end coords of scaled helical coil segments
    # for capacitance length calculation
    x1scaled = 0 
    y1scaled = 0 
    x2scaled = 0 
    y2scaled = 0 

    layerNumber = 15  # front for kicad

    if vertices == 0:
        moduleName = f"{turnsTotal}_turn_helical_inductor"
    elif vertices == 3:
        moduleName = f"{turnsTotal}_turn_triangular_inductor"
    elif vertices == 4:
        moduleName = f"{turnsTotal}_turn_square_inductor"
    elif vertices == 5:
        moduleName = f"{turnsTotal}_turn_pentagonal_inductor"
    elif vertices == 6:
        moduleName = f"{turnsTotal}_turn_hexagonal_inductor"
    elif vertices == 7:
        moduleName = f"{turnsTotal}_turn_heptagonal_inductor"
    elif vertices == 8:
        moduleName = f"{turnsTotal}_turn_octagonal_inductor"
    elif vertices == 9:
        moduleName = f"{turnsTotal}_turn_nonagonal_inductor"
    elif vertices == 10:
        moduleName = f"{turnsTotal}_turn_decagonal_inductor"
    else:
        moduleName = f"{turnsTotal}_turn_{vertices}_gon_inductor"
    moduleName = "results/" + moduleName


    outputFileName = moduleName + ".kicad_pcb" 

    print(f"Generating {turnsTotal} turn inductor:\t" + outputFileName) 

    print(f"Using track gap of: {trackGap} microns.") 
    print(f"Using track width of: {trackWidth} microns.")
    print(f"Using via drill size of: {drill} mm.")

    footprintOutput = open(outputFileName, 'w')

    header_string = ""
    header_string += initialize_file()

    footprintOutput.write(header_string)

    currentLoopStartX = 0
    currentLoopStartY = 0

    trackWidthMM = trackWidth / 1000.0
    trackGapMM = trackGap / 1000.0

    # we need to calculate the effective length of the distributed capacitor
    cumulativeCapacitorLengthMM = 0.0

    # and length of trace will allow coil resistance to be calculated
    cumulativeCoilLengthMM = 0.0

    # Extract integer and fractional parts of turnsTotal
    fullTurns = int(turnsTotal)
    fractionalTurn = turnsTotal - fullTurns

    start_x = 0
    start_y = 0
    rad = True
    x_max = 0
    y_min = 0
    y_max = 0
    # Loop for full turns
    for spiralCounter in range(fullTurns):

        if vertices != 0:  # we are making an n-gon, as opposed to a helical coil
            # the following if then else structure figures out a starting theta
            # for the n-gon in an attempt to give an aesthetically pleasing coil
            if (vertices % 2) == 1:
                theta = (math.pi / (2 * vertices))
            elif (vertices % 2) == 0:
                theta = (math.pi / vertices)
            else:
                theta = 0.0

            # we figure out the radius at a vertex using some trigonometry
            nextRadius = startRadius / math.cos(math.pi / vertices) + (spiralCounter * (radiusIncrementPerTurn / math.cos(math.pi / vertices)))

            # we step through, one vertex after another, until we complete a turn
            for vertexCount in range(vertices):
                if vertexCount < (vertices - 2):
                    x1 = (nextRadius * math.cos(vertexCount * 2 * math.pi / vertices + theta)) / 1000.0
                    y1 = (nextRadius * math.sin(vertexCount * 2 * math.pi / vertices + theta)) / 1000.0
                    x2 = ((nextRadius * math.cos((vertexCount + 1) * 2 * math.pi / vertices + theta)) / 1000.0)
                    y2 = ((nextRadius * math.sin((vertexCount + 1) * 2 * math.pi / vertices + theta)) / 1000.0)
                elif vertexCount == (vertices - 2):
                    x1 = (nextRadius * math.cos(vertexCount * 2 * math.pi / vertices + theta)) / 1000.0
                    y1 = (nextRadius * math.sin(vertexCount * 2 * math.pi / vertices + theta)) / 1000.0
                    x2 = ((nextRadius * math.cos((vertexCount + 1) * 2 * math.pi / vertices + theta)) / 1000.0)
                    y2 = ((nextRadius * math.sin((vertexCount + 1) * 2 * math.pi / vertices + theta)) / 1000.0)
                    # the second to last line segment making up the n-gon
                    # need to be lengthened to allow the final segment of
                    # of the current turn to finish where the next turn starts
                    x2 = x1 + ((x2 - x1) * (calculateSegmentLength(x1, y1, x2, y2) + (radiusIncrementPerTurn / (math.sin(2.0 * math.pi / vertices) * 1000))) / calculateSegmentLength(x1, y1, x2, y2))
                    y2 = y1 + ((y2 - y1) * (calculateSegmentLength(x1, y1, x2, y2) + (radiusIncrementPerTurn / (math.sin(2.0 * math.pi / vertices) * 1000))) / calculateSegmentLength(x1, y1, x2, y2))
                else:  # last segment of current loop
                    nextRadius = startRadius / math.cos(math.pi / vertices) + ((spiralCounter + 1) * (radiusIncrementPerTurn / math.cos(math.pi / vertices)))
                    x1 = x2 - pos_x  # copy the previous coords
                    y1 = y2 - pos_y  # copy the previous coords
                    x2 = ((nextRadius * math.cos((vertexCount + 1) * 2 * math.pi / vertices + theta)) / 1000.0)
                    y2 = ((nextRadius * math.sin((vertexCount + 1) * 2 * math.pi / vertices + theta)) / 1000.0)

                # put coil into desired coordinates
                x1 += pos_x
                x2 += pos_x
                y1 += pos_y
                y2 += pos_y
                # keep track of minimum & maximum x, y values for pinheader placement
                if vertexCount < vertices -1:
                    x_max = x1 if x1 > x_max else x_max
                    x_max = x2 if x2 > x_max else x_max
                    y_min = y1 if y1 < y_min else y_min
                    y_min = y2 if y2 < y_min else y_min
                    y_max = y1 if y1 > y_max else y_max
                    y_max = y2 if y2 > y_max else y_max

                if spiralCounter == 0 and vertexCount == 0:
                    start_x = x1
                    start_y = y1

                # we only have capacitance between turns, so we stop
                # summing capacitance length when generating the
                # final turn, i.e. stop at (turnsTotal - 1)
                if spiralCounter < (turnsTotal - 1):
                    cumulativeCapacitorLengthMM += calculateSegmentLength(x1, y1, x2, y2) + ((radiusIncrementPerTurn / 1000.0) * math.tan(math.pi / vertices))

                # we add the segment length to the total coil length
                cumulativeCoilLengthMM += calculateSegmentLength(x1, y1, x2, y2)

                # create coil line from (x1,y1) to (x2,y2)
                line = make_line("", f"{x1:.3f}", f"{y1:.3f}", f"{x2:.3f}", f"{y2:.3f}", trackWidthMM, "F.Cu")
                save_lines(start_x=x1, start_y=y1, end_x=x2, end_y=y2, save_arr=lines)
                footprintOutput.write(line)

        # end n-gon IF statement 
        elif vertices == 0:  # not an n-gon, it is a helical coil
            while not nextTurnPlease:
                nextTheta = theta + deltaTheta
                nextRadius = startRadius + radiusIncrementPerSegment
                # we figure out the coordinates in mm as double variables
                x1 = ((startRadius * math.cos(theta)) / 1000.0)
                y1 = ((startRadius * math.sin(theta)) / 1000.0)
                x2 = ((nextRadius * math.cos(nextTheta)) / 1000.0)
                y2 = ((nextRadius * math.sin(nextTheta)) / 1000.0)

                # we numerically integrate the length of the midline
                # between turns, hence the use of the + (trackGap / 2.0)
                # to establish the midline of the gap
                x1scaled = ((startRadius + (trackGap / 2.0)) * math.cos(theta)) / 1000.0
                y1scaled = ((startRadius + (trackGap / 2.0)) * math.sin(theta)) / 1000.0
                x2scaled = ((nextRadius + (trackGap / 2.0)) * math.cos(nextTheta)) / 1000.0
                y2scaled = ((nextRadius + (trackGap / 2.0)) * math.sin(nextTheta)) / 1000.0

                # put coil into desired coordinates
                x1 += pos_x
                x2 += pos_x
                y1 += pos_y
                y2 += pos_y
                # keep track of minimum & maximum x, y values for pinheader placement
                x_max = x1 if x1 > x_max else x_max
                x_max = x2 if x2 > x_max else x_max
                y_min = y1 if y1 < y_min else y_min
                y_min = y2 if y2 < y_min else y_min
                y_max = y1 if y1 > y_max else y_max
                y_max = y2 if y2 > y_max else y_max

                # there is only capacitance between turns, so we stop summing
                # capacitor length at (turnsTotal - 1)
                if spiralCounter < (turnsTotal - 1):
                    cumulativeCapacitorLengthMM += calculateSegmentLength(x1scaled, y1scaled, x2scaled, y2scaled)

                # we add the segment length to the total coil length
                cumulativeCoilLengthMM += calculateSegmentLength(x1, y1, x2, y2)

                # store coil origin coordinates
                if rad:
                    rad = False
                    start_x = x1
                    start_y = y1

                # create coil line from (x1,y1) to (x2,y2)
                line = make_line("", f"{x1:.3f}", f"{y1:.3f}", f"{x2:.3f}", f"{y2:.3f}", trackWidthMM, "F.Cu")
                save_lines(start_x=x1, start_y=y1, end_x=x2, end_y=y2, save_arr=lines)
                footprintOutput.write(line)

                startRadius = nextRadius
                theta = nextTheta
                if theta > (2 * math.pi):
                    theta -= (2.0 * math.pi)
                    nextTurnPlease = True

            nextTurnPlease = False

    # Handle the fractional turn
    if fractionalTurn > 0:
        if vertices != 0:  # n-gon case
            # Calculate the angle for the fractional turn
            fractionalAngle = fractionalTurn * 2 * math.pi

            # Calculate the radius for the fractional turn
            nextRadius = startRadius / math.cos(math.pi / vertices) + (fullTurns * (radiusIncrementPerTurn / math.cos(math.pi / vertices)))

            # Calculate the number of vertices to cover the fractional angle
            numVerticesFractional = int(fractionalAngle / (2 * math.pi / vertices))

            # Draw the partial turn
            for vertexCount in range(numVerticesFractional):
                x1 = (nextRadius * math.cos(vertexCount * 2 * math.pi / vertices + theta)) / 1000.0
                y1 = (nextRadius * math.sin(vertexCount * 2 * math.pi / vertices + theta)) / 1000.0
                x2 = ((nextRadius * math.cos((vertexCount + 1) * 2 * math.pi / vertices + theta)) / 1000.0)
                y2 = ((nextRadius * math.sin((vertexCount + 1) * 2 * math.pi / vertices + theta)) / 1000.0)

                # put coil into desired coordinates
                x1 += pos_x
                x2 += pos_x
                y1 += pos_y
                y2 += pos_y
                # keep track of minimum & maximum x, y values for pinheader placement
                if vertexCount < numVerticesFractional -1:
                    x_max = x1 if x1 > x_max else x_max
                    x_max = x2 if x2 > x_max else x_max
                    y_min = y1 if y1 < y_min else y_min
                    y_min = y2 if y2 < y_min else y_min
                    y_max = y1 if y1 > y_max else y_max
                    y_max = y2 if y2 > y_max else y_max

                # Add the segment length to the total coil length
                cumulativeCoilLengthMM += calculateSegmentLength(x1, y1, x2, y2)

                # Output the segment
                line = make_line("", f"{x1:.3f}", f"{y1:.3f}", f"{x2:.3f}", f"{y2:.3f}", trackWidthMM, "F.Cu")
                save_lines(start_x=x1, start_y=y1, end_x=x2, end_y=y2, save_arr=lines)
                footprintOutput.write(line)

        elif vertices == 0:  # helical coil case
            # Calculate the angle for the fractional turn
            fractionalAngle = fractionalTurn * 2 * math.pi

            # Draw the partial turn
            while theta < fractionalAngle:
                nextTheta = theta + deltaTheta
                nextRadius = startRadius + radiusIncrementPerSegment

                x1 = ((startRadius * math.cos(theta)) / 1000.0)
                y1 = ((startRadius * math.sin(theta)) / 1000.0)
                x2 = ((nextRadius * math.cos(nextTheta)) / 1000.0)
                y2 = ((nextRadius * math.sin(nextTheta)) / 1000.0)

                # put coil into desired coordinates
                x1 += pos_x
                x2 += pos_x
                y1 += pos_y
                y2 += pos_y
                # keep track of minimum & maximum x, y values for pinheader placement
                if nextTheta < fractionalAngle:
                    x_max = x1 if x1 > x_max else x_max
                    x_max = x2 if x2 > x_max else x_max
                    y_min = y1 if y1 < y_min else y_min
                    y_min = y2 if y2 < y_min else y_min
                    y_max = y1 if y1 > y_max else y_max
                    y_max = y2 if y2 > y_max else y_max

                # Add the segment length to the total coil length
                cumulativeCoilLengthMM += calculateSegmentLength(x1, y1, x2, y2)

                # Output the segment
                line = make_line("", f"{x1:.3f}", f"{y1:.3f}", f"{x2:.3f}", f"{y2:.3f}", trackWidthMM, "F.Cu")
                save_lines(start_x=x1, start_y=y1, end_x=x2, end_y=y2, save_arr=lines)
                footprintOutput.write(line)

                startRadius = nextRadius
                theta = nextTheta

    # x2, y2 are coordinates of the line 
    # put pinheader there
    # depending on orientation of last line, top layer line goes through 1 or 2 of the pinheader
    left = int(x1) > int(x2)
    right = int(x1) < int(x2)
    up = int(y1) > int(y2)
    down = int(y1) < int(y2)
    vertical_first = True
    y_offset, x_offset, angle = 0, 0, 0
    if left: # last line goes left
        if down: # down
            print(y2, y_max)
            if y2 > y_max: # nothing above -> horizontal
                x_offset = -2.54
                angle = 90
            else:
                y_offset = +2.54
        else:  # only left
            print(int(x2) , int(outerDiameter/1000 + x_max - pos_x + (trackGap+ trackWidth)/1000))
            if int(x2) < int(outerDiameter/1000 + x_max - pos_x + (trackGap+ trackWidth)/1000): # nothing left -> vertical
                y_offset = +2.54
            else:
                x_offset = -2.54
                angle = 90
        vertical_first = False
    elif right:
        if down:
            if int(y2) > int(y_max): # nothing below -> horizontal pinheader possible
               # if int(x2) - 5 > int(x_max): # enough space to the left
                x_offset = -2.54
                angle = 90
                #else:
                #    y_offset = +2.54
            else:
                x2 += 2.54
                angle = 90
                vertical_first = False
        elif up:
            print(y2, outerDiameter/1000 + y_max - pos_y)
            print(pos_y, y_max-pos_y)
            if int(y2) < int(outerDiameter/1000 + y_max - pos_y): # nothing above -> horizontal pinheader possible
                    x2 += 2.54
                    angle = 90
            else:
                y2 -=2.54
        else: # only right
            if int(x2) > int(x_max): # nothing right -> vertical pinheader
                y2 -=2.54
            else:
                x2 += 2.54
                angle = 90
                vertical_first = False
    else: # only up or down
        if up:
            if int(y2) < int(y_min): # nothing above -> horizontal pinheader possible
                if int(x2) + 5 < int(-x_max): # enough space to the right
                    x2 += 2.54
                    angle = 90
                else:
                    y2 -=2.54
            else:
                y2 -=2.54
        elif down: # down
            print(y2, y_max, y_min, y1)
            if int(y2) > int(y_max): # nothing below -> horizontal pinheader possible
                x_offset = -2.54
                angle = 90
            else:
                y_offset = +2.54
        else:
            y2 -= 2.54
    # check for incompatibility
    if angle == 0 and x2 == x2 + x_offset and y2 < y2 + y_offset:
        vertical_first = True

    line = make_pinheader("", x2, y2, "F.Cu", angle)
    
    if straight: # connect bottom layer in vertical + horizontal lines only
        if not vertical_first:
            # go vertical from origin
            line = make_line(line, start_x, start_y, x2+x_offset, start_y, trackWidthMM, layer="B.Cu")
            #save_lines(start_x=start_x, start_y=start_y, end_x=x2+x_offset, end_y=start_y, save_arr=lines)
            
            # go horizontal from previous line
            line = make_line(line, x2+x_offset, start_y, x2+x_offset, y2+y_offset, trackWidthMM, layer="B.Cu")
            #save_lines(start_x=x2+x_offset, start_y=start_y, end_x=x2+x_offset, end_y=y2+y_offset, save_arr=lines)
        else:
            # go horizontal from origin
            line = make_line(line, start_x, start_y, start_x, y2+y_offset, trackWidthMM, layer="B.Cu")
            #save_lines(start_x=start_x, start_y=start_y, end_x=start_x, end_y=y2+y_offset, save_arr=lines)
            # go vertical from previous line
            line = make_line(line, start_x, y2+y_offset, x2+x_offset, y2+y_offset, trackWidthMM, layer="B.Cu")
            #save_lines(start_x=start_x, start_y=y2+y_offset, end_x=x2+x_offset, end_y=y2+y_offset, save_arr=lines)
    else: # connect bottom layer diagonally
        line = make_line(line, start_x, start_y, x2+x_offset, y2+y_offset, trackWidthMM, layer="B.Cu")
        #save_lines(start_x=start_x, start_y=start_y, end_x=x2+x_offset, end_y=y2+y_offset, save_arr=lines)
    # add via to the coil origin
    line = make_via(line, start_x, start_y, trackWidthMM, drill, layers=["F.Cu", "B.Cu"])
    footprintOutput.write(line)


    print(f"Outer diameter of coil (mm): {outerDiameter / 1000.0}")
    print(f"Inner diameter of coil (mm): {innerDiameter / 1000.0}")
    if vertices != 0:
        print(f"Inductor has {vertices} vertices.")
    else:
        print("Inductor is helical")

    print("Total coil length (mm): ", end="")
    print(f"{cumulativeCoilLengthMM:.4f}")

    print("DC resistance of coil assuming copper resistivity = 1.75E-8 ohm.m")
    print("\t35.56 micron copper thickness: ", end="")
    print(f"{1.75E-8 * (cumulativeCoilLengthMM / 1000.0) / ((trackWidthMM / 1000.0) * (3.556E-5)):.4f} ohm")
    print("\t71.12 micron copper thickness: ", end="")
    print(f"{1.75E-8 * (cumulativeCoilLengthMM / 1000.0) / ((trackWidthMM / 1000.0) * (7.112E-5)):.4f} ohm")

    print("Total capacitor length (mm): ", end="")
    print(f"{cumulativeCapacitorLengthMM:.4f}")

    finalCapacitanceF = calculateCapacitance(trackGapMM, cumulativeCapacitorLengthMM)

    print(f"Total calculated capacitance (F): {finalCapacitanceF}")
    print("Total calculated capacitance (pF): ", end="")
    print(f"{finalCapacitanceF * 1E12:.4f}")

    # the following variables are used to calculate inductance
    # using the "Greenhouse" equation for flat "pancake" inductors
    # we set the default values to those needed for a helical coil
    greenhouseC1 = 1.00  # Square 1.27, Hexagonal 1.09, Circle 1.00
    greenhouseC2 = 2.46  # Square 2.07, Hexagonal 2.23, Circle 2.46
    greenhouseC3 = 0.00  # Square 0.18, Hexagonal 0.00, Circle 0.00
    greenhouseC4 = 0.20  # Square 0.13, Hexagonal 0.17, Circle 0.20

    if vertices == 4:
        greenhouseC1 = 1.27  # Square 1.27, Hexagonal 1.09, Circle 1.00
        greenhouseC2 = 2.07  # Square 2.07, Hexagonal 2.23, Circle 2.46
        greenhouseC3 = 0.18  # Square 0.18, Hexagonal 0.00, Circle 0.00
        greenhouseC4 = 0.13  # Square 0.13, Hexagonal 0.17, Circle 0.20
    elif vertices == 6:
        greenhouseC1 = 1.09  # Square 1.27, Hexagonal 1.09, Circle 1.00
        greenhouseC2 = 2.23  # Square 2.07, Hexagonal 2.23, Circle 2.46
        greenhouseC3 = 0.00  # Square 0.18, Hexagonal 0.00, Circle 0.00
        greenhouseC4 = 0.17  # Square 0.13, Hexagonal 0.17, Circle 0.20
    elif vertices == 8:
        greenhouseC1 = 1.07  # Square 1.27, Hexagonal 1.09, Circle 1.00
        greenhouseC2 = 2.29  # Square 2.07, Hexagonal 2.23, Circle 2.46
        greenhouseC3 = 0.00  # Square 0.18, Hexagonal 0.00, Circle 0.00
        greenhouseC4 = 0.19  # Square 0.13, Hexagonal 0.17, Circle 0.20
    elif vertices != 0:
        print("Using inductance equation for circle due to a"
            " lack of published parameters\nfor the inductance of "
            f"{vertices} vertex inductors.")

    finalInductanceH = calculateInductance(turnsTotal, innerDiameter, outerDiameter, greenhouseC1, greenhouseC2, greenhouseC3, greenhouseC4)

    print(f"Calculated inductance (Henries): {finalInductanceH}")
    print("Calculated inductance (uH): ", end="")
    print(f"{finalInductanceH * 1_000_000:.4f}")
    print("Calculated self resonant frequency (Hz): ", end="")
    print(f"{calculateSelfResonance(finalInductanceH, finalCapacitanceF):.0f}")
    print("Calculated self resonant frequency (MHz): ", end="")
    print(f"{calculateSelfResonance(finalInductanceH, finalCapacitanceF) / 1E6:.4f}")

    # and we close the footprint file before finishing up
    footprintOutput.write("\n)")
    footprintOutput.close()

    # save last line of the coil and plot magnetic field
    lines.append(f"{x2/10:.2f},{y2/10:.2f},0,1")
    write_lines_to_file(f"{moduleName}.txt", lines)
    corner = (int(pos_x/10-outerDiameter/20000)+1, int(pos_y/10-outerDiameter/20000)+1)
    plane='z'
    level = 1
    magnetic_field(moduleName, corner, outerDiameter/10000, plane, level)
    


def calculateSelfResonance(inductanceHenries, capacitance):
    # method employed described in http://dx.doi.org/10.4236/cs.2013.42032
    # "Design and Optimization of Printed Circuit Board
    # Inductors for Wireless Power Transfer System" by
    # Ashraf B. Islam, Syed K. Islam, Fahmida S. Tulip
    # Circuits and Systems, 2013, 4, 237-244

    # we use frequency = 1/(2*pi*sqrt(LC)) 
    return (1.0/(2.0*pi*sqrt(inductanceHenries*capacitance))) 


def calculateSegmentLength(xOne, yOne, xTwo, yTwo):

    lengthSquared = ((xOne - xTwo) * (xOne - xTwo))+((yOne - yTwo) * (yOne - yTwo)) 
    return sqrt(lengthSquared) 


def calculateCapacitance(trackGapMilliM, gapLengthMilliM):
    # method employed described in http://dx.doi.org/10.4236/cs.2013.42032
    # "Design and Optimization of Printed Circuit Board
    # Inductors for Wireless Power Transfer System" by
    # Ashraf B. Islam, Syed K. Islam, Fahmida S. Tulip
    # Circuits and Systems, 2013, 4, 237-244
    etaRC = 3.1  # solder mask relative permittivity a.k.a. dielectric constant
    etaRS = 4.7  # approx, fibreglass relative permittivity (dielectric constant)
            # etaRA = 1.006 for air at STP at ~ 0.9MHz
    alpha = 0.9  # for FR4 coating
    beta = 0.1  # for FR4 substrate	
    eta0 = 8.854E-12  # dielectric constant of a vacuum	
    copperThicknessM = 0.00003556  # in metres = 35.56 microns for 1oz/ft^2 copper
    trackGapM = trackGapMilliM/1000.0  # convert mm to metres
    gapLengthM = gapLengthMilliM/1000.0  # convert mm to metres
    calculatedCapacitance = (alpha*etaRC + beta*etaRS)*eta0*copperThicknessM*gapLengthM/trackGapM 
    # i.e. the formula for parallel plates of a capacitor
    #            = (plateArea/gap)*dielectricConstantOfVacuum*relativePermittivity
    return calculatedCapacitance


def calculateInductance(turns, dIn, dOut, c1, c2, c3, c4):
    # method employed described in http://dx.doi.org/10.4236/cs.2013.42032
    # "Design and Optimization of Printed Circuit Board
    # Inductors for Wireless Power Transfer System" by
    # Ashraf B. Islam, Syed K. Islam, Fahmida S. Tulip
    # Circuits and Systems, 2013, 4, 237-244
    dAvg = ((dOut + dIn)/1000000.0)/2.0  # convert distance in microns to metres
    sigma = (dOut - dIn)/(1.0*(dOut + dIn))  # sigma = "coil fill ratio"
    mu = 4*pi/10000000  # vacuum permeability = 4*pi * 10^(-7)
    inductance = 0 
    inductance = ((mu * turns * turns * dAvg * c1)/2.0)*(log(c2/sigma) + c3*sigma + c4*sigma*sigma) 
    return inductance  # in Henries (H)


if __name__ == "__main__":
    main()