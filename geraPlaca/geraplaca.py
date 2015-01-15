#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
real    2m32.300s
user    2m30.413s
sys 0m1.701s
'''

import sys

def main():

    if len(sys.argv) > 1:
        
        placas = open(sys.argv[1], "w")

        for L1 in xrange(65, 91):
            for L2 in xrange(65, 91):
                for L3 in xrange(65, 91):
                    for N in xrange(0, 10000):
                        placas.write("%c%c%c-%04d\n" %(L1, L2, L3, N));

        placas.close()

    else:
        print "Informe um nome para o arquivo."                    

if __name__ == '__main__':
    main()
