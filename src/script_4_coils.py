'''
create 4 coils across 4 Cu layers on the same PCB board
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
    # adjust/add parameters as needed:
    turnsTotal = 9
    vertices = 4
    outer = 47000

    moduleName = f"results/{turnsTotal}_turn_{polygon_names.get(vertices, f'{vertices}-gon')}_inductor"
    outputFileName = moduleName + ".kicad_pcb" 

    fd = open(outputFileName, 'w')
    print(outputFileName)
    fd.write(initialize_file())
    fd.close()
    main(0, outer, 100, turnsTotal, 1270, 1270, 150, True, vertices, 38, 38, "In1.Cu", coil_only=True, no_plots=False, via_outer=250)
    main(0, outer, 100, turnsTotal, 1270, 1270, 150, True, vertices, 90, 38, "In2.Cu", coil_only=True, no_plots=True, via_outer=250)
    main(0, outer, 100, turnsTotal, 1270, 1270, 150, True, vertices, 38, 90, "In3.Cu", coil_only=True, no_plots=True, via_outer=250)
    main(0, outer, 100, turnsTotal, 1270, 1270, 150, True, vertices, 90, 90, "In4.Cu", coil_only=True, no_plots=True, via_outer=250)
    fd = open(outputFileName, 'a')
    fd.write(")")
    fd.close()