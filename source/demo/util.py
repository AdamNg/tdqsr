import os
import json

import logging

class Utilities():

    @staticmethod
    def load_json(pth_to_data: str):
        logging.debug(f'loading path {pth_to_data}')
        _pth = os.path.abspath(pth_to_data)
        logging.debug(f'resolve absolute path {_pth}')
        
        assert os.path.exists(_pth)

        _data = json.load(open(_pth))
        logging.debug(f'loaded data {_data}')
        return _data

    @staticmethod
    def cache_json(data, pth_to_data:str , mode: str='w'):
        logging.debug(f'caching to path {pth_to_data}')
        logging.debug(f'caching data {data}')
        assert isinstance(data, dict)
        _pth = os.path.abspath(pth_to_data)
        logging.debug(f'resolve absolute path {pth_to_data}')
        return json.dump(data, open(_pth, mode=mode))