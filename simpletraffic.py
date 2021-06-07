# -*- coding: utf-8 -*-
"""
Created on Sat May  1 14:12:37 2021

@author: MertUnsal
"""
import random 
import numpy as np
import matplotlib.pyplot as plt

#NOTE THAT THE I,J NOTATION IS NOT CONSISTENT WITH THE PAPER

class SimpleTraffic:
    
    def __init__(self, h, l, cars = []):
        
        self.l = l # length of the road 
        self.h = h
        self.road = np.zeros((self.h,self.l))  # one can access the cars in lane i by road[i] and the car at i,j with road[i][j]
        self.cars_inital = cars
        self.cars = cars # holds tuples which represent the position of the cars (i,j)
        #self.block = np.zeros(self.h) #turns out this is unnecessary #holds if the cars at the end of the road can leave freely or not
        self.carnum = len(self.cars)
        for car in self.cars:
            i,j = car
            self.road[i][j] = 1
        self.density = self.carnum/(self.l*self.h)
        
    def generate_cars(self, rate = -1):
        
        # generating cars in the beginning of the road
        
        # calculate the probability of a car being generated in the empty lanes
        if rate > 1 or rate < 0:
            rate = random.random()
            
        # find the empty lanes
        empty_lanes = []
        for i in range(self.h):
            if self.road[i][0] == 0:
                empty_lanes.append(i)
                
                
        for lane in empty_lanes:
            
            p = random.random()
            if p <= rate:
                self.cars.append((lane,0))
                self.carnum += 1
                self.road[lane][0] = 1            
            
        #update density and carnum
        self.carnum = len(self.cars)
        self.density = self.carnum/(self.l*self.h)
        
        
    def print_road(self):
        
        for i in range(self.h):
            for j in range(self.l):
                if self.road[i][j] == 1:
                    print("* ", end = "")
                else:
                    print("- ", end = "")
            print()
        
        
    def next_step(self):
        
        delete_car_indexes = []
        road_indexes = []
        cars_moved = 0
        
        for k in range(self.carnum):
            i, j = self.cars[k]
            
            if j == self.l-1:
                # bad implementation for deleting the car, should be improved with a data structure to hold the list of cars
                self.road[i][j] = -1 # this will be set to zero later
                road_indexes.append((i,j))
                delete_car_indexes.append(k)
                cars_moved += 1
                
                
            elif self.road[i][j+1] == 0:
                self.road[i][j+1] = 1
                self.road[i][j] = -1 # this will be set to zero later
                road_indexes.append((i,j))
                self.cars[k] = (i,j + 1)
                cars_moved += 1
            
        # delete the cars that exit the road (bad implementation)
        for k in delete_car_indexes:
            self.cars.pop(k)
            
        # set roads back to 0
        for pos in road_indexes:
            i, j = pos
            self.road[i][j] = 0
        
        # update density and carnum
        self.carnum = len(self.cars)
        self.density = self.carnum/(self.l*self.h)
        
        return cars_moved
    
    def simulate(self, N, r, reset = False):
        # N is the number of rounds of the simulation
        # rate is passed to generate_cars, if rate is None then the simulation tries to keep the density as constant as possible
        densities = []
        cars_moved = []
        for i in range(N):
            self.generate_cars(r)
            densities.append(self.density)
            cars = self.next_step()
            cars_moved.append(cars)
            
        if reset:
            self.reset()

        
        return densities, cars_moved
    
    def reset(self):
        self.road = np.zeros((self.h,self.l))
        self.cars = []
        #self.block = np.zeros(self.h)
        for car in self.cars:
            i,j = car
            self.road[i][j] = 1
        self.carnum = len(self.cars)
        self.density = self.carnum/(self.l*self.h)
        
'''
traffic = SimpleTraffic(20, 100)
densities, cars_moved = traffic.simulate(350, 0.4, True)
plt.figure(figsize = (40,16))
plt.scatter(densities, cars_moved)
plt.xlabel("Density", fontsize = 30)
plt.ylabel("Flow Rate", fontsize = 30)
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.title("Fundamental Diagram for Cellular Automata", fontsize = 40)
plt.plot()
'''

def numerical(k0, dx, T, dt, v):
     # solution[i] holds the array of solution at time i*dt
    t = 0
    i = 0
    
    solution = [k0]
    
    while t < T:
        new = []
        data = solution[i][0]
        new.append(0)
        for j in range(1,len(solution[i])-1):
            data = solution[i][j]
            gradk = (solution[i][j] - solution[i][j-1])/(dx)
            nextdata = data - v * gradk * dt
            new.append(nextdata)
        new.append(0)
        solution.append(new)
        i += 1
        t += dt
        
    return solution
        
tab = np.linspace(-100, 100, 2000) 
k0 = np.exp(-0.01*tab**2)
dx = 0.1
T = 5
dt = 0.001
v = 10
final = numerical(k0,dx,T, dt, v)
plt.figure(figsize = (40,16))
for j in range(0,5001,1000):
    plt.plot(tab[500:], final[j][500:], label = f'T = {j*dt}')
plt.legend(fontsize = 18)

        
        