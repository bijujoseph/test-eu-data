import pandas as pd
import logging


logger = logging.getLogger(__name__)

class Generator:

    def __init__(self, config, year):
        super().__init__()
        self.config = config
        self.year = year

    def generate(self):
        """
        Will generate the data files.
        :return:
        """
        pass



    def load_df(self, path, format):
        if format == 'csv' or format == 'tsv':
            return pd.DataFrame(pd.read_csv(path))
        if format == 'xlsx' or format == 'excel':
            return pd.DataFrame(pd.read_excel(path))

    def load_census_counties(self):
       pass

    def load_qpp_euc_counties(self):
       pass

    def load_hud_county_zip(self):
        pass