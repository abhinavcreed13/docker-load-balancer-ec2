import urllib.request
import argparse
import random
from datetime import datetime
import numpy as np
import time
from util import get_args

def hit_url(args, it, inter_arrival_times):
    response = urllib.request.urlopen(args.url).read()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(f"Iter: {it}, Time: {current_time}, Reponse: {str(response)}")
    if it != args.iter:
        print(f"Next request in: {abs(inter_arrival_times[it])} seconds")
        time.sleep(abs(inter_arrival_times[it]))

def simulate_load(args):
    if args.time_dist == "poisson":
        inter_arrival_times = [random.expovariate(args.lamb) for i in range(1,args.iter+1)]
        for it in range(1,args.iter+1):
            hit_url(args, it, inter_arrival_times)
    elif args.time_dist == "normal":
        inter_arrival_times = list(np.random.normal(args.mu, args.sigma,args.iter))
        for it in range(0,args.iter):
            hit_url(args, it, inter_arrival_times)

if __name__ == '__main__':
    args = get_args()
    simulate_load(args)





