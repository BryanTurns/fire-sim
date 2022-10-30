from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

#ok

def graphData(data):

    flameCountList = data['flameCount'] 
    totalFireChanceList = data['totalFireChance'] 
    blocksBurnedList = data['blocksBurned']
    percentBurnedList =[0]*(len(blocksBurnedList)//2)
    numBlocks = data['numBlocks']
    x = 0


    #time list
    timeList = []
    for t in range(len(flameCountList)):
        timeList.append(t+1)
   
    # for i in range(len(blocksBurnedList)):
    #     percentBurnedList.append(blocksBurnedList[i]*100/numBlocks)

    while x<len(timeList):
        percentBurnedList.append(blocksBurnedList[x]*100/numBlocks)
        x+=2


    
    print("DADJISJIDJLASJD")
    print(percentBurnedList)

    #find sum of all fire chances
    totalFireChance=0
    for x in totalFireChanceList:
        totalFireChance+=x

    #find avg fire chance
    avgFireChance=totalFireChance/len(totalFireChanceList)
    avgFireChanceList=[0]*len(totalFireChanceList)
    #fill empty array of avgFireChance to graph
    for i in range(len(totalFireChanceList)):
        avgFireChanceList[i]=avgFireChance


    
    fig, axis = plt.subplots(2, 2)

    axis[0,0].plot(timeList, flameCountList)
    axis[0,0].set_title('# Things on Fire vs. Time')
    axis[0,0].set_xlabel('Time')
    axis[0,0].set_ylabel('# Things on Fire')
    axis[0,1].plot(timeList, totalFireChanceList)
    axis[0,1].set_title('Fire Chance of City vs. Time')
    axis[0,1].set_xlabel('Time')
    axis[0,1].set_ylabel('Fire Chance of City')
    axis[1,0].plot(timeList, avgFireChanceList)
    axis[1,0].set_title('Average Fire Chance vs. Time')
    axis[1,0].set_xlabel('Time')
    axis[1,0].set_ylabel('Average Fire Chance')
    axis[1,1].plot(timeList, percentBurnedList)
    axis[1,1].set_title('% Land Burned vs. Time')
    axis[1,1].set_xlabel('Time')
    axis[1,1].set_ylabel('% Land Burned')

   
    fig.tight_layout(pad=1.0)
    plt.show()
    

    # Some example data to display
    #x = np.linspace(0, 2 * np.pi, 400)
    
    #y = np.sin(x ** 2)