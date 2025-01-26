import json
from linkedin_api import Linkedin

if __name__ == "__main__":
    with open('credentials.json') as f:
        credentials = json.load(f)

    if credentials:
        linkedin = Linkedin(credentials['username'], credentials['password'])

        results = linkedin.search_people(keyword_company='LocalStudent', keyword_first_name='Marco', keyword_last_name='Tan', limit=5, include_private_profiles=True)
        profile = linkedin.get_profile(urn_id=results[0]['urn_id'])

        if profile:
            linkedin.add_connection(profile['public_id'], message='Hello Marco! My name is Mr. Mohn E. Baggs and I would like to recruit you for a job in Abu Dhabi.');
