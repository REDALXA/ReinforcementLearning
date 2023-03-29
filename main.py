mass = 1000
Energy_sub = 0
Energy_bra = 0
aux = 500
ess_max = 30000

class Train:
    def __init__(self, position):
        self.position = position
        self.velocity = 0
        self.acceleration = 0
        self.mass = mass

    def traction_power(self, gravity, resistance):
        power = self.velocity * (gravity + resistance + self.mass * self.acceleration)
        return power

class Ess:
    def __init__(self):
        self.SOC = 0.25
        self.charge = True

def event(train, ess):
    substation_power = 0
    resistor_power = 0
    if train.traction_power() > (0-aux) : ## system needs energy
        if ess.charge :
            substation_power = aux + train.traction_power()
        else :
            soc_diff = (aux + train.traction_power()) / ess_max
            if ess.SOC - soc_diff >= 0.25 :
                substation_power = 0 ## energy consumption comes from ESS
                ess.SOC -= soc_diff
            else : ## SOC is less tahn demanded so substation still has to be used
                ## logic for joint capacitor and substation energy usage 
            ## write logic to update SOC ESS
    else : ## train is releasing energy
        if ess.charge :
            soc_diff = (aux + train.traction_power()) / ess_max
            if ess.SOC - soc_diff <= 0.9 :
                resistor_power = 0 ## energy consumption comes from ESS
                ess.SOC -= soc_diff
            else : ## braking power is more than ess max energy so energy will be disipated as heat
                
        else : ## since no ess is charging, excess has to be disipated
            resistor_power -= train.traction_power()
            resistor_power += aux 

    return (substation_power, resistor_power)

