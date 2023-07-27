import boto3
from botocore.exceptions import ClientError
import googlemaps


def get_secret():
    secret_name = "googlemaps"
    region_name = "eu-west-3"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    # Decrypts secret using the associated KMS key.
    secret = get_secret_value_response['SecretString']
    return secret


def is_open():
    API_KEY = get_secret()
    map_client = googlemaps.Client(API_KEY)
    location_name = 'Goasstall, Hinterglemm, Austria'
    # Instantiate Place Search request using `places(*args, **kwargs)` from the library
    # Use the `stored location` as an argument for query
    place_search = map_client.places(location_name)
    # Get the search results

    search_results = place_search.get('results')

    # Store the place_id from the result to be used

    place_id = (search_results[0]['place_id'])

    # Instantiate Place Details request using the `place(*args, **kwargs)` from the library
    # Use the stored place_id as an argument for the request

    place_details = map_client.place(place_id)

    # Get the Place Details result

    details_results = place_details.get('result')

    # Print the result specifying what you only need which is the `opening_hours` field
    if details_results['business_status'] == 'CLOSED_TEMPORARILY':
        return False
    else:
        return details_results['opening_hours']['open_now']
