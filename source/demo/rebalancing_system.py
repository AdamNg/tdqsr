import logging

from typing import List, Dict, Optional
from functools import reduce

from .position import Positions
from .broker import Broker

class RebalancingSystem():

    def __init__(self, broker: Optional[Broker] = Broker(initial_positions=Positions(dict()),initial_aum=100.),):
        logging.debug(f'constructing RebalancingSystem object')
        logging.debug(f'constructing w/ broker = {broker}')
        assert isinstance(broker, Broker)
        self._broker = broker

    @property
    def broker(self,)->Broker:
        return self._broker

    def rebalance(self, execution_weights:Optional[Dict[str, float]]=None) -> Dict[str, float]:
        logging.info(f'rebalancing with execution_weights {execution_weights}')
        assert isinstance(execution_weights, dict)
        for k,v in execution_weights.items():
            assert isinstance(k, str)
            assert isinstance(v, float)
        
        _wgt = execution_weights
        _wgt[Positions.uninvested_mnemonic()] = 1 - reduce(lambda acc, val:acc+val, list(weight for asset, weight in execution_weights.items() if not asset == Positions.uninvested_mnemonic()))


        _aum = self.broker.get_live_aum()
        _px = self.broker.get_live_prices(_wgt)
        logging.info(f'rebalancing on aum = {_aum}')
        logging.info(f'rebalancing over prices = {_px}')
        logging.info(f'rebalancing to weights = {_wgt}')

        _unit = {asset: _aum * weight / _px[asset] for asset, weight in execution_weights.items()}
        logging.info(f'rebalancing to units = {_unit}')

        _new_position = Positions(_unit)
        _execution_positions = _new_position - self.broker.positions
        logging.info(f'rebalancing from units {self.broker.positions.get_asset_positions()}')
        logging.info(f'rebalancing to units {_new_position.get_asset_positions()}')
        logging.info(f'rebalancing execution units {_execution_positions.get_asset_positions()} ')

        # AN TODO: actual trading (net positions)
        self.broker.execute_trades(_new_position)
        self.broker.update(positions=_new_position, aum = _aum)
        
        return _execution_positions.get_asset_positions()
    
    def to_string(self,)->str:
        return str(dict(broker=self.broker))

    def __str__(self,) -> str:
        return f'{__class__}({self.to_string()})'