import graphene
from bettingApp.routes import *
from competitionApp.routes import competitionAppQuery, competitionAppMutation
from graphene_django_extras import all_directives
from fixtureApp.routes import * 
from predictionApp.routes import *
from statsApp.routes import *
from teamApp.routes import *

class RootQuery(
    bettingAppQuery,
    competitionAppQuery,
    fixtureAppQuery,
    predictionAppQuery,
    statsAppQuery,
    teamAppQuery,
    graphene.ObjectType):
    pass


class RootMutations(
    bettingAppMutation,
    competitionAppMutation,
    fixtureAppMutation,
    predictionAppMutation,
    statsAppMutation,
    teamAppMutation,
    graphene.ObjectType
):
    pass


schema = graphene.Schema(query=RootQuery, mutation=RootMutations,  directives=all_directives)
