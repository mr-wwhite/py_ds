from pytrends.request import TrendReq
import pandas as pd

import warnings
warnings.filterwarnings("ignore")

pytrend = TrendReq(hl='en-US', tz=360, timeout=(10,25), proxies=['https://34.203.233.13:80',], retries=2, backoff_factor=0.1, requests_args={'verify':False})
#pytrend = TrendReq()

top_teams = ['Liverpool', 'Manchester City', 'Arsenal', 'Chelsea', 'Manchester United']
countries = ["united_states", "india", "united_kingdom", "portugal", "italy", "russia", "greece", "australia",
             "france", "belgium", "indonesia", "canada", "mexico", "germany","brazil", "argentina", "chile",
             "south_africa", "malaysia", "thailand", "ukraine", "ireland"]
keyword_suggestions = []
pytrend.build_payload(kw_list=top_teams)

team_interest_by_region = pytrend.interest_by_region()
team_interest_by_region.to_csv("team_interest_by_region.csv")

team_interest_over_time = pytrend.interest_over_time()
team_interest_over_time.to_csv("team_interest_over_time.csv")

trending_searches_by_country = {}

for country in countries:
    trending_searches_by_country[country] = pytrend.trending_searches(pn=country).values.tolist()

trending_searches = pd.DataFrame(trending_searches_by_country)

for cname in trending_searches:
    trending_searches[cname] = trending_searches[cname].astype(str)
    trending_searches[cname] = trending_searches[cname].str.replace("[", "")
    trending_searches[cname] = trending_searches[cname].str.replace("]", "")
    trending_searches[cname] = trending_searches[cname].str.replace("'", "")

trending_searches = trending_searches.head(10)
trending_searches.to_csv("trending_searches.csv")

trending_searches_containing_top_teams = {}

for top_team in top_teams:
    top_team_list = []
    for col in trending_searches:
        if(trending_searches[col].str.contains(top_team).any()):
            top_team_list.append(str(col))
    trending_searches_containing_top_teams[top_team] = top_team_list

# print(trending_searches_containing_top_teams)
countries_searching_for_top_teams = pd.DataFrame.from_dict(trending_searches_containing_top_teams, orient="index").transpose()
countries_searching_for_top_teams.to_csv("countries_searching_for_top_teams.csv")