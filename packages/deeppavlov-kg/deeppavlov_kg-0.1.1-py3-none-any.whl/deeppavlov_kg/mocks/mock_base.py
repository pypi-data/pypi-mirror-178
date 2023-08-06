import argparse
import datetime

from terminusdb_client import WOQLClient, WOQLQuery as WOQL
from terminusdb_client.woqlschema import WOQLSchema, DocumentTemplate, LexicalKey
from terminusdb_client.schema.schema import TerminusClass

from deeppavlov_kg.core.graph import Neo4jKnowledgeGraph, TerminusdbKnowledgeGraph


def populate_neo4j(neo_kg):
    start_time = datetime.datetime.now()

    neo_kg.drop_database()

    neo_kg.ontology.create_entity_kind("Human")
    neo_kg.ontology.create_entity_kind("Person", parent="Human")
    neo_kg.ontology.create_entity_kind("Habit")
    neo_kg.ontology.create_entity_kind("interest")

    neo_kg.ontology.create_property_kinds("Person", ["height", "name", "weight"], [int, str, int])
    neo_kg.ontology.create_property_kinds("Habit", ["name"], [str])
    neo_kg.ontology.create_relationship_kind("Person", "LIKES", "Habit")
    neo_kg.ontology.create_relationship_kind("Person", "HATES", "Habit")
    neo_kg.create_entity("Person", "Person/Jack", ["name", "height",], ["Jack Ryan", 180])
    neo_kg.create_entity("Habit", "Habit/Sport", ["name"], ["Sport"])
    neo_kg.create_entity("Person", "Person/Sandy", ["name", "height"], ["Sandy Bates", 160])
    neo_kg.create_entity("Habit", "Habit/Reading", ["name"], ["Reading"])

    neo_kg.create_relationship("Person/Sandy", "LIKES", "Habit/Reading")

    neo_kg.create_or_update_properties_of_entities(["Person/Sandy", "Person/Jack"], ["height", "weight"], [165, 70])
    neo_kg.create_or_update_properties_of_entity("Person/Sandy", ["height", "weight"], [166, 77])
    neo_kg.create_or_update_property_of_entity("Person/Jack", "height", 170)

    neo_kg.get_properties_of_entity("Person/Sandy")
    neo_kg.get_all_entities()

    ts = datetime.datetime(2022,10,30)
    neo_kg.get_entities_by_date(["Person/Sandy"], ts)

    neo_kg.search_for_relationships("LIKES", "Person/Sandy", "Habit/Reading")

    # # neo_kg.ontology.delete_property_kinds("Person", ["HATE"])
    # # neo_kg.ontology.delete_relationship_kind("Person", "LIKES", "Habit")
    # # neo_kg.delete_property_from_entity("Habit/Reading", "name")
    # # neo_kg.delete_properties_from_entity("Person/Sandy", ["height", "weight"])

    neo_kg.delete_entity("Person/Jack")

    print("Neo4j code took: ", datetime.datetime.now() - start_time, " sec")


def populate_terminusdb(terminus_kg):
    start_time = datetime.datetime.now()

    terminus_kg.drop_database()

    terminus_kg.ontology.create_entity_kinds(
        entity_kinds=["Person", "User", "Habit"],
        parents=[None, "Person", None]
    )

    terminus_kg.ontology.create_property_kinds_of_entity_kinds(
        entity_kinds=["Person", "User", "Habit"],
        property_kinds=[
            ["Height", "Weight"],
            ["Login", "Password"],
            ["Start_date"],
        ],
        property_types=[
            [int, int],
            [str, str],
            [datetime.date],
        ]
    )

    terminus_kg.ontology.create_relationship_kinds(
        ["Person", "Person"],
        ["KEEP_UP", "QUIT"],
        ["Habit", "Habit"],
    )

    terminus_kg.create_entities(
        entity_kinds=["User"]*2+["Habit"],
        entity_ids=["User/"+str(id) for id in range(2)]+["Habit/Sport"],
        property_kinds=[
            ["Height", "Login", "Password"],
            ["Weight", "Login", "Password"],
            ["Start_date"],
        ],
        property_values=[
            [170, "Jack333", "12345678"],
            [60, "Sandy111", "00000000"],
            [datetime.date(2010, 10, 10)],
        ]
    )

    terminus_kg.create_relationships(
        ids_a=["User/0", "User/1"],
        relationship_kinds=["KEEP_UP", "QUIT"],
        ids_b=["Habit/Sport"]*2
    )

    # terminus_kg.ontology.delete_property_kinds("Person", ["HATE"])
    # terminus_kg.ontology.delete_relationship_kind("Person", "LIKES")
    # terminus_kg.delete_property_from_entity("Habit/Reading", "name")
    # terminus_kg.delete_properties_from_entity("Person/Sandy", ["height", "weight"])
    # terminus_kg.delete_properties_from_entities(["Person/Sandy", "Person/Jack"], ["height", "name"])

    # terminus_kg.delete_entity("Person/Jack")

    print("Terminusdb code took: ", datetime.datetime.now() - start_time, " sec")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Connect to neo4j or terminusdb')
    parser.add_argument('--neo4j', type=bool, nargs='?', const=True, default=False)
    parser.add_argument('--terminusdb', type=bool, nargs='?', const=True, default=False)

    args = parser.parse_args()

    if args.neo4j:
        NEO4J_BOLT_URL = "bolt://neo4j:neo4j@localhost:7687"
        ONTOLOGY_KINDS_HIERARCHY_PATH = "deeppavlov_kg/database/ontology_kinds_hierarchy.pickle"
        ONTOLOGY_DATA_MODEL_PATH = "deeppavlov_kg/database/ontology_data_model.json"
        DB_IDS_FILE_PATH = "deeppavlov_kg/database/db_ids.txt"
        neo_kg = Neo4jKnowledgeGraph(
                neo4j_bolt_url=NEO4J_BOLT_URL,
                ontology_kinds_hierarchy_path=ONTOLOGY_KINDS_HIERARCHY_PATH,
                ontology_data_model_path=ONTOLOGY_DATA_MODEL_PATH,
                db_ids_file_path=DB_IDS_FILE_PATH,
            )
        populate_neo4j(neo_kg)

    if args.terminusdb:
        DB = "example_db"
        TEAM ="admin"
        terminus_kg = TerminusdbKnowledgeGraph(team=TEAM, db_name=DB, local=True)
        populate_terminusdb(terminus_kg)

    print("end")
