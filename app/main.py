import os
import logging
logging.basicConfig(level=os.getenv("LOG_LEVEL", "info").upper())

from ariadne import ObjectType, QueryType, MutationType, gql, make_executable_schema
from ariadne.asgi import GraphQL
from asgi_lifespan import LifespanManager
from graphqlclient import GraphQLClient
from starlette.applications import Starlette

# .env
from dotenv import load_dotenv

from app.qclient import QClient

# import resolvers
# import resolvers
from app.resolvers.resolvers import resolver_compute_resultant, \
    resolver_make_butterwork_filter_mapper, \
    resolver_lfilter_1D_mapper, \
    resolver_compute_intensity, \
    resolver_compute_impact, \
    resolver_compute_1D_DFT, \
    resolver_create_data, \
    resolver_project_data

#import the schema
from app.types.types import dsp_types
# Load environment variables
load_dotenv()


def getClient():
    qClient = None
    qEndpoint = os.getenv('MAANA_ENDPOINT_URL')

    if not qEndpoint:
        logging.info('Maana Q endpoint is not set')
        return None
    else:
        # Build as closure to keep scope clean.
        def buildClient(client=qClient):
            # Cached in regular use cases.
            if (client is None):
                logging.info('Building graphql client...')
                client = QClient(os.getenv('MAANA_ENDPOINT_URL'))
            return client
        return buildClient()


# Define types using Schema Definition Language (https://graphql.org/learn/schema/)
# Wrapping string in gql function provides validation and better error traceback
type_defs = gql(dsp_types)

# Map resolver functions to Query fields using QueryType
query = QueryType()
# Resolvers are simple python functions
resolver_compute_resultant(query)
resolver_make_butterwork_filter_mapper(query)
resolver_lfilter_1D_mapper(query)
resolver_compute_intensity(query)
resolver_compute_impact(query)
resolver_compute_1D_DFT(query)
resolver_create_data(query)
resolver_project_data(query)


# Create executable GraphQL schema
schema = make_executable_schema(type_defs, [query])

# --- ASGI app


async def startup():
    logging.info("Starting up...")
    logging.info("... done!")


async def shutdown():
    logging.info("Shutting down...")
    logging.info("... done!")

# Create an ASGI app using the schema, running in debug mode
# Set context with authenticated graphql client.
app = Starlette(debug=True, on_startup=[startup], on_shutdown=[shutdown])
app.mount('/', GraphQL(schema, debug=True ))
                       #context_value={'client': getClient()}))
