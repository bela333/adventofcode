import numpy as np



with open("input.txt") as f:
    octo = np.array([[int(num) for num in line.strip()] for line in f])
    flashes = 0
    #Step
    for _ in range(100):
        #Have a list of octos that can flash this round
        can_flash = np.full_like(octo, True, dtype=bool)
        #Increase power
        octo += 1
        #Find octos that should flash
        flashing = octo>9
        #While there are flashing octos
        while flashing.any():
            for (y, x), v in np.ndenumerate(flashing):
                if v:
                    flashes += 1
                    #Make sure octos that flashed can't flash any more
                    can_flash[y, x] = False
                    for _y in range(-1, 2):
                        _y = y+_y
                        if _y < 0 or _y >= octo.shape[0]:
                            continue
                        for _x in range(-1, 2):
                            _x = x+_x
                            if _x < 0 or _x >= octo.shape[1]:
                                continue
                            #increase power level of neighbouring octos
                            octo[_y,_x] += 1
            #Find octos that still need to flash in this round
            flashing = (octo*can_flash)>9
        #Reset octos that flashed already
        octo[octo>9] = 0
    print(flashes)