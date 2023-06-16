import random
from typing import List, Dict

class Positions:

    def __init__(self, positions: Dict[str, float]):
        self._pos = positions

    def get_universe(self) -> List[str]:
        return list(self._pos.keys())
    
class Broker:
    def __init__(self, initial_positions: Positions, initial_aum: float):
        self.positions = initial_positions
        self.aum = initial_aum
    
    def get_live_prices(self,) -> Dict[str, float]:
        prices = {asset: random.uniform(10,30) for asset in self.positions.get_universe()}
        return prices
    
    def execute_trades(self, execution_positions: Positions) -> None:
        pass
