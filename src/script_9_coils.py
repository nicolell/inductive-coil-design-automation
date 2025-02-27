'''
create 9 coils per layer, across 5 Cu layers on the same PCB board
'''
from main import * 
polygon_names = {
        0: "helical",
        3: "triangular",
        4: "square",
        5: "pentagonal",
        6: "hexagonal",
        7: "heptagonal",
        8: "octagonal",
        9: "nonagonal",
        10: "decagonal"
}

if __name__ == '__main__':
    # (x,y) coordinates for the origins of each coil, respectively, divided by layer
    layer_coordinates = {
    "F.Cu": [(49.53, 49.53), (0, 49.53), (-49.53, 49.53), (0, 0), (49.53, 0), (-49.53, 0), (49.53, -49.53), (0, -49.53), (-49.53, -49.53)],
    "In1.Cu": [(-33.02, 49.53), (16.51, 49.53), (-33.02, 0), (16.51, 0), (-33.02, -49.53), (16.51, -49.53)],
    "In2.Cu": [(-16.51, 49.53), (33.02, 49.53), (-16.51, 0), (33.02, 0), (-16.51, -49.53), (33.02, -49.53)],
    "In3.Cu": [(-49.53, 33.02), (-16.51, 33.02), (-49.53, -16.51), (-16.51, -16.51)],
    "In4.Cu": [(16.51, 33.02), (49.53, 33.02), (16.51, -16.51), (49.53, -16.51)]
    }

    # TODO: adjust these parameters as needed
    turnsTotal = 91 # number of turns
    vertices = 8 # number of vertices of the polygon -> 8 = octagon
    outer = 47240 # diameter of the coil in micrometers
    w = 127 # track width in micrometers
    g = 127 # track spacing in micrometers
    via_drill = 150 # via diameter in micrometers
    via_outer = 250 # via drill in micrometers
    # end of parameters

    # plot magnetic field of a single coil with the specified parameters
    main(0, outer, 100, turnsTotal, w, g, via_drill, True, vertices, 0, 0, "F.Cu", coil_only=False, via_outer=via_outer, no_plots=False)

    # create layout with 9 such coils per layer
    moduleName = f"results/{turnsTotal}_turn_{polygon_names.get(vertices, f'{vertices}-gon')}_inductor"
    outputFileName = moduleName + ".kicad_pcb" 
    fd = open(outputFileName, 'w')
    print(outputFileName)
    fd.write(initialize_file())
    fd.close()
    for layer, coordinates in layer_coordinates.items():
        for coordinate in coordinates:
            main(0, outer, 100, turnsTotal, w, g, via_drill, True, vertices, coordinate[0], coordinate[1], layer, coil_only=True, via_outer=via_outer, no_plots=True)
    fd = open(outputFileName, 'a')
    fd.write(")")
    fd.close()