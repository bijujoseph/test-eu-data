import argparse
import logging as logger
import pandas as pd
from pydash import strings

logger.basicConfig(level='INFO',
                    format='%(levelname).1s %(asctime)s %(filename)s:%(lineno)s [%(funcName)s] %(message)s')

def canonicalize_state_code(s):
    return strings.trim(strings.upper_case(s))

def canonicalize_county_name(s):
    s1 = strings.replace(s, " county", "", ignore_case=True)
    return strings.trim(strings.lower_case(s1))


def save_json(args, df, filename):
    df.to_json(f'staging/{args.year}/{filename}')

def save_csv(args, df, filename):
    df.to_csv(f'staging/{args.year}/{filename}', index=False)

def load_hud_county_zip(args):
    fields = ["zip", "county", "usps_zip_pref_state"]
    df = pd.DataFrame(pd.read_excel(f'staging/{args.year}/COUNTY_ZIP_122021.xlsx', usecols=fields))
    df.rename(columns={'zip': 'zipcode', "county": "county_fips", "usps_zip_pref_state": "hud_state_code"}, inplace=True)
    df["state_code"] = df["hud_state_code"].apply(canonicalize_state_code)
    return df

def load_euc_counties(args):
    df = pd.DataFrame(pd.read_csv(f'staging/{args.year}/euc_counties.csv'))
    # clean county names
    df["county_name"] = df["county_name"].apply(canonicalize_county_name)
    df["state_code"] = df["state_code"].apply(canonicalize_state_code)
    return df

def load_census_counties(args):
    fields = ["USPS", "GEOID", "NAME"]
    df = pd.DataFrame(pd.read_csv(f'staging/{args.year}/2021_Gaz_counties_national.txt', sep='\t', header=0, usecols=fields))
    # clean the data frame .
    df.rename(columns={'USPS': 'state_code', "NAME": "county_name", "GEOID": "county_fips"}, inplace=True)
    df["county_name"] = df["county_name"].apply(canonicalize_county_name)
    df["state_code"] = df["state_code"].apply(canonicalize_state_code)
    return df


def all(args):
    logger.info("Processing all stages")
    counties = load_census_counties(args)
    euc_counties = load_euc_counties(args)
    euc_counties_fips = euc_counties.merge(counties, on=["state_code", "county_name"], how="left")
    save_csv(args, euc_counties_fips, "euc_counties_fips.csv")
    hud_county_fips_zipcodes = load_hud_county_zip(args)
    save_csv(args, hud_county_fips_zipcodes, "county_fips_zipcodes.csv")
    euc_counties_zipcodes = euc_counties_fips.merge(hud_county_fips_zipcodes.drop(columns=["state_code"], axis=1), on=["county_fips"], how="left")

    euc_counties_zipcodes.drop(columns=["county_fips", "hud_state_code"],inplace= True)
    save_csv(args, euc_counties_zipcodes, "euc_counties_zipcodes_crosswalk.csv")
    save_json(args, euc_counties_zipcodes, "euc_counties_zipcodes_crosswalk.json")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--stage', default='all')
    parser.add_argument('-y', '--year', default=2022)
    args = parser.parse_args()
    if args.stage == 'all':
        all(args)


if __name__=='__main__':
    main()
