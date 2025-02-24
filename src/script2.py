'''
create 9 coils per layer, across 5 Cu layers on the same PCB board
'''
from new_coil import * 
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
    layer_coordinates = {
    "F.Cu": [(49.53, 49.53), (0, 49.53), (-49.53, 49.53), (0, 0), (49.53, 0), (-49.53, 0), (49.53, -49.53), (0, -49.53), (-49.53, -49.53)],
    "In1.Cu": [(-33.02, 49.53), (16.51, 49.53), (-33.02, 0), (16.51, 0), (-33.02, -49.53), (16.51, -49.53)],
    "In2.Cu": [(-16.51, 49.53), (33.02, 49.53), (-16.51, 0), (33.02, 0), (-16.51, -49.53), (33.02, -49.53)],
    "In3.Cu": [(-49.53, 33.02), (-16.51, 33.02), (-49.53, -16.51), (-16.51, -16.51)],
    "In4.Cu": [(16.51, 33.02), (49.53, 33.02), (16.51, -16.51), (49.53, -16.51)]
    }

    turnsTotal = 91
    vertices = 4
    outer = 47240
    w = 127
    g = 127

    moduleName = f"results/{turnsTotal}_turn_{polygon_names.get(vertices, f'{vertices}-gon')}_inductor"
    outputFileName = moduleName + ".kicad_pcb" 

    fd = open(outputFileName, 'w')
    print(outputFileName)
    fd.write(initialize_file())
    fd.close()
    
    for layer, coordinates in layer_coordinates.items():
        for coordinate in coordinates:
            main(0, outer, 100, turnsTotal, w, g, 0.5, True, vertices, coordinate[0], coordinate[1], layer, coil_only=True)
    fd = open(outputFileName, 'a')
    fd.write(")")
    fd.close()