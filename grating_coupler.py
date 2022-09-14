# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 10:49:59 2022

@author: Vahram

nd.Polygon(layer=bb_body, points=[(0,0), (gap,0), (math.tan(angle)*width+gap,width), (math.tan(angle)*width,width)])




"""
'fix stuff!'
import nazca as nd
import nazca.geometries as geom
import math

# add layers to xsection (automatically add the xsection)

# draw waveguide in created xsection
teeth = nd.Polygon(layer=19, points=[(0, 0), (220, 0), (220, 180), (0, 180)])


offset = 0.1
#Layer for every single thing if only one mask applied
nd.add_layer(name='Si_base', layer=1, accuracy=0.001)
nd.add_layer(name='BOX', layer=2, accuracy=0.001)
nd.add_layer(name='Si_guide', layer=3, accuracy=0.001)
nd.add_layer(name='SiO2_gap', layer=4, accuracy=0.001)
nd.add_layer(name='SiN', layer=5, accuracy=0.001)

# create layers in a xsection
#xsection is for several mask applied with different growths and different layers
nd.add_layer2xsection(xsection='XS1', layer=1, growx=4*offset)
nd.add_layer2xsection(xsection='XS1', layer=2, growx=3*offset)
nd.add_layer2xsection(xsection='XS1', layer=3, growx=2*offset)
nd.add_layer2xsection(xsection='XS1', layer=4, growx=offset)



nd.add_layer2xsection(xsection='XS2', layer=1, growx=4*offset)
nd.add_layer2xsection(xsection='XS2', layer=2, growx=3*offset)
nd.add_layer2xsection(xsection='XS2', layer=3, growx=2*offset)


ic1 = nd.interconnects.Interconnect(xs='XS1',width=5)#can specify width in interconnect


ic2 = nd.interconnects.Interconnect(xs='XS2',width=5)#can specify width in interconnect



@nd.bb_util.hashme('gc', 'period', 'angle')
def gc_coupler(angle=0, length=50, width=5, period=0.3, ff=0.5):
    with nd.Cell(hashme=True) as C:

        number_of_teeth = length / period


        if angle > 0:
            base_wg = ic1.strt(length=length + math.tan(angle*math.pi/180) * width, width=width).put(0, 0)
        elif angle < 0:
            base_wg = ic1.strt(length=length - math.tan(angle*math.pi/180) * width, width=width).put(0, 0)

        else:
            base_wg = ic1.strt(length=length + math.tan(angle*math.pi/180) * width, width=width).put(0, 0)

        W = period * ff

        for i in range(round(number_of_teeth)):
            length_teeth = number_of_teeth * period
            if angle < 0:
                nd.Polygon(
                    points=[(0, 0), (W, 0), (math.tan(angle*math.pi/180) * width + W, width), (math.tan(angle*math.pi/180) * width, width)],
                    layer='SiN').put(0 + length_teeth / 2 - length / 2 + period * i - math.tan(angle*math.pi/180) * width,
                                       0 - 0.5 * width, 0)
            else:
                nd.Polygon(
                    points=[(0, 0), (W, 0), (math.tan(angle*math.pi/180) * width + W, width), (math.tan(angle*math.pi/180) * width, width)],
                    layer='SiN').put(0 + length_teeth / 2 - length / 2 + period * i, 0 - 0.5 * width, 0)

        base_wg.raise_pins(['a0','b0'],['a0','b0'])

        #nd.connect_path(base_wg.pin['a0'],base_wg.pin['b0'],  abs(length))
        #nd.put_stub()

    return C


if __name__ == '__main__':
    with nd.Cell(name='topcell') as topcell:
        from nazca.pathfinder import findpath

        gc1 = gc_coupler(width= 5, angle=20).put(0, -15)

        ic2.taper(width1= 5, width2 = 0.45, length =10).put(gc1.pin['a0'],0,0)
        ic2.taper(width1= 5, width2 = 0.45, length =10).put(gc1.pin['b0'],0,0)




    nd.export_plt(topcell, 'gc_test.gds')


