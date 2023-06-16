import logging
from typing import Dict
from ..base import Positions as PositionBase

class Positions(PositionBase):

    __uninvested_mnemonic = 'CASH'

    @staticmethod
    def uninvested_mnemonic()->str:
        return Positions.__uninvested_mnemonic

    def __init__(self, positions: Dict[str, float]):
        logging.debug(f'constructing Positions object')
        logging.debug(f'constructing positions {positions}')
        # verbose sanity check
        assert isinstance(positions, dict)
        for k,v in positions.items():
            assert isinstance(k, str)
            assert isinstance(v, float)

        # base
        logging.debug(f'construction (base class)')
        super().__init__(positions)
    
    def get_positions(self,) -> Dict[str, float]:
        return self._pos
    
    @property
    def positions(self,) -> Dict[str, float]:
        return self._pos
    
    def get_position(self, asset) -> float:
        return self.get_positions.get(asset, 0.)

    def get_asset_positions(self, )->Dict[str, float]:
        return {k:v for k,v in self._pos.items() if not k == Positions.uninvested_mnemonic()} 

    @property
    def empty(self):
        return len(self.get_positions()) == 0
    
    def __add__(self, others):
        assert isinstance(others, Positions)

        return Positions({k : self.positions.get(k,0.) + others.positions.get(k, 0.) for k in set(self.positions.keys()).union(self.positions.keys())})
    
    def __sub__(self, others):
        assert isinstance(others, Positions)

        return Positions({k : self.positions.get(k,0.) - others.positions.get(k, 0.) for k in set(self.positions.keys()).union(self.positions.keys())})
    
    def to_string(self,)->str:
        return f'{__class__}({str(self.positions)})'
    
    def __str__(self,) -> str:
        return f'{__class__} ({self.to_string()})'