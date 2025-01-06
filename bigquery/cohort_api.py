import requests
from typing import Dict, Any

PHENOML_API_URL = "https://experiment.pheno.ml"

class CohortAPI:
    def __init__(self, client_id: str, client_secret: str):
        self.base_url = PHENOML_API_URL
        self.client_id = client_id
        self.client_secret = client_secret

    def get_cohort_response(self, search_query: str, exclude_deceased: bool, verbose: bool) -> Dict[str, Any]:
        """Send a cohort request and retrieve the response. Returns a dictionary with the SQL query and the extraction results if verbose is true."""
        auth_endpoint = self.base_url + "/api/collections/users/auth-with-password"
        cohort_endpoint = self.base_url + "/construe/cohort"
        
        auth_response = requests.post(auth_endpoint, json= {"identity":self.client_id, "password":self.client_secret})
        auth_response.raise_for_status()
        auth_token = auth_response.json().get('token')

        headers = {
            "Authorization": f"Bearer {auth_token}",
            "Content-Type": "application/json"
        }

        cohort_request_body = {
            "config": {
                "include_rationale": verbose,
                "include_extract_results": verbose, #Optional, defaults to false. Set to true if you want to see the detailed code extraction results
                "exclude_deceased": exclude_deceased, #Optional, defaults to true. Set to true if you want to exclude deceased patients
                "sql_syntax": "bigquery",
            },
            "text": search_query
        }
        
        cohort_response = requests.post(cohort_endpoint, json=cohort_request_body, headers=headers)
        cohort_response.raise_for_status()
        response = cohort_response.json()
        
        formatted_response = {
            'sql': response['sql'],
            'queries': []
        }
        
        code_extracts = []
        for query in response['queries']:
            query_info = {
                'resource': query['resource'],
                'exclude': query['exclude'],
                'searchParams': query['searchParams']
            }
            formatted_response['queries'].append(query_info)
            
            # Extract codes if present
            if 'codeExtractResults' in query:
                for result in query['codeExtractResults']:
                    for code in result['codes']:
                        code_extracts.append({
                            'resource': query['resource'],
                            'system': result['systemName'],
                            'code': code['code'],
                            'description': code['description']
                        })
        
        if code_extracts:
            formatted_response['code_extracts'] = code_extracts
            
        return formatted_response
    