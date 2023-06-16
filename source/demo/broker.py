import logging

import random
from typing import List, Dict, Optional
from functools import reduce

from .position import Positions, PositionBase
from ..base import Broker as BrokerBase

class Broker(BrokerBase):

    def __init__(self, initial_positions: Positions, initial_aum: float):
        logging.debug(f'constructing Broker object')
        logging.debug(f'constructing w/ initial_positions {initial_positions}')
        logging.debug(f'constructing w/ initial_aum {initial_aum}')

        assert isinstance(initial_aum, float) and initial_aum > 0.
        assert isinstance(initial_positions, Positions)
        
        logging.debug(f'construction (base class)')
        super().__init__(initial_positions if not initial_positions.empty else Positions({Positions.uninvested_mnemonic():initial_aum}), initial_aum)

    def update(self, positions:Optional[Positions]=None, aum:Optional[float]=None)->None:

        logging.debug(f'updating Broker object')
        logging.debug(f'updating positions {positions}')
        logging.debug(f'updating aum {aum}')

        # this should be in the base class
        if not positions is None:
            # AN TODO: logging
            assert isinstance(positions, Positions)
            self.positions = positions
        if not aum is None:
            # AN TODO: logging
            assert isinstance(aum, float) and aum > 0.
            self.aum = aum
        
        logging.debug(f'updated with values (aum = {self.aum}, positions = {self.positions})')
        pass
        
    def get_live_aum(self,) -> float:
        _px = self.get_live_prices()
        _pos = self.positions.get_positions()

        # cash placeholder for (de)leverage / long-short
        _px[Positions.uninvested_mnemonic()] = _px.get(Positions.uninvested_mnemonic(), 1.)
        _pos[Positions.uninvested_mnemonic()] = _pos.get(Positions.uninvested_mnemonic(), 0.)

        # sanity check
        assert set(_px.keys()) == set(_pos.keys())

        return reduce(lambda acc, val: acc+val, [_px[_k] * _pos[_k] for _k in _px.keys()])

    def get_live_prices(self, positions:Optional[Dict[str, float]]=None) -> Dict[str, float]:

        logging.debug(f'retrieving live prices (rfq)')
        logging.debug(f'retrieving on positions {positions}')
        if positions is None:
            _px = super().get_live_prices()
        
        else:
            _px = {asset: random.uniform(10,30) if not asset == Positions.uninvested_mnemonic() else 1. for asset in positions.keys()}

        _px[Positions.uninvested_mnemonic()] = 1.
        logging.debug(f'retrieving values {_px}')
        return _px
    
    def execute_trades(self, execution_positions: Positions) -> None:
        logging.info(f'executing (changes) in positions {execution_positions}')
        assert isinstance(execution_positions, Positions)
        return super().execute_trades(PositionBase(execution_positions.get_asset_positions()))
    
    def to_string(self,)->str:
        return f'{__class__} ({dict(aum=self.aum, positions=self.positions)})'

    def __str__(self,)->str:
        return self.to_string()
