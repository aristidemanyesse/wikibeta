import graphene
from competitionApp.routes import competitionAppQuery, competitionAppMutation
from graphene_django_extras import all_directives

class RootQuery(
    competitionAppQuery,
    graphene.ObjectType):
    pass


class RootMutations(
    competitionAppMutation,
    graphene.ObjectType
):
    pass


schema = graphene.Schema(query=RootQuery, mutation=RootMutations,  directives=all_directives)
