# initialize logging environment
import sys
import logging
logging.basicConfig(
    format='%(asctime)s | %(levelname)s : %(message)s',
    level=logging.INFO, stream=sys.stdout,)

from source.demo import Utilities, RebalancingSystem

the_system = RebalancingSystem()

some_wgt = Utilities.load_json(r'./data/targetWeights_20230321.json')

some_hedge_position = the_system.rebalance(some_wgt)


