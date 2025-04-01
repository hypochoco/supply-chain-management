from __future__ import annotations
from dataclasses import dataclass 
from docplex.mp.context import *
from docplex.mp.model import Model
from typing import Optional
import numpy as np 
import math
@dataclass()
class LPInstance:
   
    numCustomers : int        		# the number of customers	   
    numFacilities : int           	# the number of facilities
    allocCostCF : np.ndarray   	# allocCostCF[c][f] is the service cost paid each time customer c is served by facility f
    demandC :  np.ndarray   	     		# demandC[c] is the demand of customer c
    openingCostF: np.ndarray   	        # openingCostF[f] is the opening cost of facility f
    capacityF :np.ndarray   	        	# capacityF[f] is the capacity of facility f
    numMaxVehiclePerFacility : int   	 # maximum number of vehicles to use at an open facility 
    truckDistLimit : float        # total driving distance limit for trucks
    truckUsageCost : float		# fixed usage cost paid if a truck is used 
    distanceCF :  np.ndarray   	       # distanceCF[c][f] is the roundtrip distance between customer c and facility f 



def getLPInstance(fileName : str) -> Optional[LPInstance]:
  try:
    with open(fileName,"r") as fl:
      numCustomers,numFacilities = [int(i) for i in fl.readline().split()]
      numMaxVehiclePerFacility = numCustomers 
      print(f"numCustomers: {numCustomers} numFacilities: {numFacilities} numVehicle: {numMaxVehiclePerFacility}")
      allocCostCF = np.zeros((numCustomers,numFacilities))
       

      allocCostraw = [float(i) for i in fl.readline().split()]
      index = 0
      for i in range(numCustomers):
         for j in range(numFacilities):
            allocCostCF[i,j] = allocCostraw[index]
            index+=1
      
      demandC = np.array([float(i) for i in fl.readline().split()])
    
      openingCostF = np.array([float(i) for i in fl.readline().split()])

      capacityF = np.array([float(i) for i in fl.readline().split()])

      truckDistLimit,truckUsageCost = [float(i) for i in fl.readline().split()]
      
      distanceCF =  np.zeros((numCustomers,numFacilities))
      distanceCFraw = [float(i) for i in fl.readline().split()]
      index = 0
      for i in range(numCustomers):
         for j in range(numFacilities):
            distanceCF[i,j] = distanceCFraw[index]
            index+=1
      return LPInstance(
         numCustomers=numCustomers,
         numFacilities=numFacilities,
         allocCostCF=allocCostCF,
         demandC=demandC,
         openingCostF=openingCostF,
         capacityF=capacityF,
         numMaxVehiclePerFacility=numMaxVehiclePerFacility,
         truckDistLimit=truckDistLimit,
         truckUsageCost=truckUsageCost,
         distanceCF=distanceCF
         )


  except Exception as e:
     print(f"Could not read problem instance file due to error: {e}")
     return None 



class LPSolver:

  def __init__(self,filename : str):
     self.lpinst = getLPInstance(filename)
     self.model = Model() #CPLEX solver

  def solve(self):
     pass 
  

def dietProblem():
    # Diet Problem from Lecture Notes
    m = Model()
    # Note that these are continous variables and not integers 
    mvars = m.continuous_var_list(2,0,1000)
    carbs = m.scal_prod(terms=mvars,coefs=[100,250])
    m.add_constraint(carbs >= 500)
    
    m.add_constraint(m.scal_prod(terms=mvars,coefs=[100,50]) >= 250) # Fat
    m.add_constraint(m.scal_prod(terms=mvars,coefs=[150,200]) >= 600) # Protein

    m.minimize(m.scal_prod(terms=mvars,coefs=[25,15]))

    sol  = m.solve()
    obj_value = math.ceil(m.objective_value) 
    if sol:
       m.print_information()
       print(f"Meat: {mvars[0].solution_value}")
       print(f"Bread: {mvars[1].solution_value}")
       print(f"Objective Value: {obj_value}")
    else:
       print("No solution found!")