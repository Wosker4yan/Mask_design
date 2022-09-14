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

        nd.connect_path(base_wg.pin['a0'],base_wg.pin['b0'],  abs(length))
        #nd.put_stub()

    return C
def mmi(    width2 = 2,
    input_wg_length = 5,
    length_input_taper = 10,
    output_width = 2,
    bb_length = 16.172,
    width_bb = 5,
    width1 = 0.8,
    output_taper_length = 10,
    output_wg_length = 10,
            port = 1):
    with nd.Cell(name='mmi') as C:
        length_output = input_wg_length + length_input_taper + bb_length

        input_strt = ic2.strt(length=input_wg_length, width=width1).put()

        ic2.taper(length=length_input_taper, width1=width1, width2=width2).put()

        ic2.strt(length=bb_length, width=width_bb).put()


        ic2.taper(length=output_taper_length, width1=width2, width2=width1).put(length_output, 1.32)

        output_taper = ic2.taper(length=output_taper_length, width1=output_width, width2=width1).put(length_output, -1.32)


        p1 = nd.Pin(name='input', show=True).put(input_strt.pin['a0'])
        p2 = nd.Pin(name='output', show=True).put(output_taper.pin['b0'])
    return C

if __name__ == '__main__':
    with nd.Cell(name='topcell') as topcell:
        from nazca.pathfinder import findpath

        mmi1 = mmi()
        mmi2= mmi()
        xxx = mmi1.put()
        mmi2.put(xxx.pin['output'],0,0)
    nd.export_gds(topcell, 'xxx.gds')


#FINISH THIS ON SUNDAY