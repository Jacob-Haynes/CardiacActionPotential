import numpy as np

class Grid(object):
    def __init__(self,timee, i, j, heart, active,gridSize,threshold,pointTotal,AP,diffuse,sampleRate):
        self.timee = timee
        self.i = i
        self.j = j
        self.iTrig = 0
        self.jTrig = 0
        self.heart = heart
        self.active = active
        self.gridSize = gridSize
        self.threshold = threshold
        self.pointTotal = pointTotal
        self.skip = 0
        'get 100 values for s_t - dummy amount for now'
        self.s_t = []
        self.cellValue = 0.1
        self.cellLoop = 0
        self.AP = AP
        self.diffuse = diffuse
        self.sampleRate = sampleRate
    def s_t_calc(self):
        self.s_t = []
        for self.activePeriod in range(100*self.sampleRate):
            'sometimes 100 s_t values might go out of time range.'
            'eg is time is 450 and modellength is 500, can only get 50 s_t values'
            'so looks to see if loop is less than pointtotal'
            if self.timee+self.activePeriod < self.pointTotal:
                'set s_t value from referenced cell'
                self.s_t.append(self.heart[self.timee+self.activePeriod][self.i+self.iTrig][self.j+self.jTrig])

        return self.s_t
    def pulseChange(self):
        self.cellValue = 0.1
        'want to define active period as points when pulse is greater than zero'
        while not self.cellValue < -0.3:
            'can only looks over values of AP, if gets to end of AP length, terminate'
            if self.cellLoop == len(self.AP) - 1:
                return
            'also check to see if near end of time of simulation'
            if self.timee+self.cellLoop+self.diffuse < self.pointTotal:
                'set cell values equal to AP values as goes through loop through time'
                'round to make printing values more aesthetic'
                self.cellValue = round(self.AP[self.cellLoop],3)
                self.heart[self.timee+self.cellLoop+self.diffuse][self.i][self.j] = self.cellValue
                'if active was set to zero before, set it as 1 -"normal cell is now active"'
                if self.active[self.timee+self.cellLoop][self.i][self.j] == 0:
                    self.active[self.timee+self.cellLoop][self.i][self.j] = 1
                'if active was 2, set to 3 "uniblocked cell now active"'
                if self.active[self.timee+self.cellLoop][self.i][self.j] == 2:
                    self.active[self.timee+self.cellLoop][self.i][self.j] = 3
            'add one to loop variable'
            self.cellLoop += 1
        'value of cell should be less than zero now, but want to keep cell active in refractory period'
        'so do same again until cell value almost back to zero'
        while not self.cellValue > -0.3:
            if self.cellLoop== len(self.AP) - 1:
                return
            elif self.timee+self.cellLoop+self.diffuse < self.pointTotal:
                self.cellValue = round(self.AP[self.cellLoop],3)
                self.heart[self.timee+self.cellLoop+self.diffuse][self.i][self.j] = self.cellValue
                if self.active[self.timee+self.cellLoop][self.i][self.j] == 0:
                    self.active[self.timee+self.cellLoop][self.i][self.j] = 1
                elif self.active[self.timee+self.cellLoop][self.i][self.j] == 2:
                    self.active[self.timee+self.cellLoop][self.i][self.j] = 3
            self.cellLoop += 1
        return
    def gridChange(self):
        'define two variables where cell is going to get s_t from. eg jTrig = -1 means look at left to left'
        self.jTrig = 0
        self.iTrig = 0
        'if cell isnt active, and current time - diffuse time isnt out of range'
        if self.active[self.timee][self.i][self.j] == 0 and self.timee - self.diffuse > 0:
            'if j>0 required as j-1 would be out of range is j = 0'
            if self.j > 0:
                'look to see if j -1 cell has a voltage about threshold'
                if self.heart[self.timee][self.i][self.j-1] > self.threshold:
                    'if it does, set jTrig to -1'
                    self.jTrig = -1
                    self.iTrig = 0
                    'get values for s_t from that cell'
                    self.s_t_calc()
                    'set skip = 1, to tell code to do calculations with s_t values just got'
                    self.skip = 1
                    return self.s_t
            'look at i-1'
            if self.i > 0:
                if self.heart[self.timee][self.i-1][self.j] > self.threshold:
                    self.jTrig = 0
                    self.iTrig = -1
                    self.s_t_calc()
                    self.skip = 1
                    return self.s_t
            'look at j+1, if j is not at end of row'
            if self.j < self.gridSize-1:
                if self.heart[self.timee][self.i][self.j+1] > self.threshold:
                    self.jTrig = 1
                    self.iTrig = 0
                    self.s_t_calc()
                    self.skip = 1
                    return self.s_t
            'look at i+1 is i is not at end of row'
            if self.i < self.gridSize-1:
                if self.heart[self.timee][self.i+1][self.j] > self.threshold:
                    self.jTrig = 0
                    self.iTrig = 1
                    self.s_t_calc()
                    self.skip = 1
                    return self.s_t
        'if cell is unidirectional bloker, only want to look at cells in one direction, j+1'
        if self.active[self.timee][self.i][self.j] == 2 and self.timee - self.diffuse >0 :
            'look at cell to right, j+1'
            if self.j < self.gridSize-1:
                if self.heart[self.timee][self.i][self.j+1] > self.threshold:
                    self.jTrig = 1
                    self.iTrig = 0
                    self.s_t_calc()
                    self.skip = 1
                    return self.s_t

        'if cell active value is not 0 or 2, just skip as cell is either active or omniblocker'
        self.skip = 0
        return self.skip
