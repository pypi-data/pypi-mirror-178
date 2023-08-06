import datetime
import logging
from random import randint
from typing import Tuple, Generator, Optional

from fabulist import Fabulist
import mimesis.random as rand
from mimesis import Generic, Numeric
from mimesis.locales import Locale
from mimesis.schema import Field, Schema

from deeppavlov_kg import KnowledgeGraph

generic = Generic(locale=Locale.EN)
fabulist = Fabulist()

NODE_LABELS = [[fabulist.get_word("noun").capitalize()] for _ in range(10)]
RELATIONSHIP_LABELS = [[fabulist.get_word("verb").upper()] for _ in range(10)]
# TODO: Add USER_RELATIONSHIP_LABELS in order to add more user properities to deepen dataset.
# Properties like: ["INTERESTED_IN", "LIKES", "DISLIKES", "HAS_HOBBY", "WORK_AS"]

_date: datetime.datetime

field = Field(locale=Locale.EN)
numeric = Numeric()

# users generator
users = Schema(
    schema=lambda: {
        str(numeric.increment(accumulator="node_id")): {
            "type": "node",
            "Id": str(numeric.increment(accumulator="same_node_id")),
            "labels": ["User"],
            "properties": {
                "name": field("full_name"),
                "born": field("timestamp", posix=False),
                "gender": rand.get_random_item(["M", "F"]),
                "OCEAN_openness": rand.get_random_item([True, False]),
                "OCEAN_conscientiousness": rand.get_random_item([True, False]),
                "OCEAN_agreeableness": rand.get_random_item([True, False]),
                "OCEAN_extraversion": rand.get_random_item([True, False]),
                "OCEAN_neuroticism": rand.get_random_item([True, False]),
                "_deleted": False,
            },
        }
    }
)

# random entities generator
entities = Schema(
    schema=lambda: {
        str(numeric.increment(accumulator="node_id")): {
            "type": "node",
            "Id": str(numeric.increment(accumulator="same_node_id")),
            "labels": rand.get_random_item(NODE_LABELS),
            "properties": {
                "name": "".join(
                    [fabulist.get_word("adj", "#negative"), "-", generic.payment.cvv()]
                ),
                "has": "".join(
                    [
                        rand.get_random_item(
                            [
                                fabulist.get_word("adj", "#negative"),
                                fabulist.get_word("adj", "#positive"),
                            ]
                        ),
                        " ",
                        fabulist.get_word("noun"),
                    ]
                ),
                "_deleted": False,
            },
        }
    }
)

# random relationships generator
rels = Schema(
    schema=lambda: {
        "Id": numeric.increment(accumulator="rel_id"),
        "type": "relationship",
        "label": rand.get_random_item(RELATIONSHIP_LABELS)[0],
        "properties": {
            "how": rand.get_random_item([fabulist.get_word("adv")]),
            "_deleted": False,
        },
    }
)

# node properties generator
node_properties = Schema(
    schema=lambda: {fabulist.get_word("noun"): fabulist.get_word("adj")}
)
# relationship properties generator
relationship_properties = Schema(schema=lambda: {"sometimes": fabulist.get_word("adv")})


graph = KnowledgeGraph(
    "bolt://neo4j:neo4j@localhost:7687",
    ontology_kinds_hierarchy_path="deeppavlov_kg/database/ontology_kinds_hierarchy.pickle",
    ontology_data_model_path="deeppavlov_kg/database/ontology_data_model.json",
    db_ids_file_path="deeppavlov_kg/database/db_ids.txt"
)


def set_date(date):
    """Initializes the global vaiable date

    Args:
      date: the desired initial date of generated data

    Returns:

    """
    global _date
    _date = date


def generate_rels(iterations: int, nodes: dict) -> list:
    """Generates relationships.

    Generates random relationships using the rels schema, then adds start and end nodes to it.

    Args:
      iterations: number of relationships to generate
      nodes: nodes in database

    Returns:
      generated relationships

    """
    relationships = rels.create(iterations)
    nodes_ids = [k for k in nodes]
    for relationship in relationships:
        relationship.update(
            {
                "start": {"Id": rand.get_random_item(nodes_ids)},
                "end": {"Id": rand.get_random_item(nodes_ids)},
            }
        )
    return relationships


def iterate_generate_1node_and_1rel(
    nodes: dict,
    relationships: list,
) -> Generator:
    """Method 1 to generate data.

    Generates one node and one relationship that links the node with others.
    Adds generated node and rel to database as well as to local variables so that
        they can be used in future linking

    Args:
      nodes: nodes in database
      relationships: relationships in database

    Returns:
      modified nodes and relationships after assigning the generated ones

    """
    global _date
    while True:
        node = entities.create(iterations=1)
        node = node[0][next(iter(node[0]))]
        node["properties"].update(
            {"Id": node["Id"], "_creation_timestamp": _date}
        )
        nodes.update({node["Id"]: node})

        rel = generate_rels(iterations=1, nodes=nodes)
        rel = rel[0]
        rel["end"]["Id"] = node["Id"]
        rel["properties"].update({"Id": rel["Id"], "_creation_timestamp": _date})
        rel_types = [type(value) for value in rel["properties"].values()]
        relationships.append(rel)
        node_kind=node["labels"][0]
        node_types = [type(value) for value in node["properties"].values()]
        node_parent_kind = next(iter(rand.get_random_item(NODE_LABELS)))
        while node_parent_kind == node_kind:
            node_parent_kind = next(iter(rand.get_random_item(NODE_LABELS)))

        if not graph.ontology.is_valid_entity_kind(node_kind):
            graph.ontology.create_entity_kind(
                node_kind,
                parent=node_parent_kind,
                kind_properties=list(node["properties"].keys()),
                kind_property_types=node_types,
            )
        else:
            graph.ontology.create_entity_kind_properties(
                node_kind,
                list(node["properties"].keys()),
                new_property_types=node_types,
            )
        graph.create_entity(
            kind=node_kind,
            id_=node["properties"].pop("Id"),
            property_kinds=list(node["properties"].keys()),
            property_values=list(node["properties"].values()),
            create_date=node["properties"]["_creation_timestamp"],
        )

        graph.ontology.create_relationship_kind(
            rel["label"],
            next(iter(graph.get_entity_by_id(rel["start"]["Id"]).labels)),
            node_kind,
            rel_property_kinds=list(rel["properties"].keys()),
            rel_property_types=rel_types,
        )
        graph.create_relationship(
            id_a=rel["start"]["Id"],
            relationship_kind=rel["label"],
            id_b=rel["end"]["Id"],
            rel_property_kinds=list(rel["properties"].keys()),
            rel_property_values=list(rel["properties"].values()),
            create_date=rel["properties"]["_creation_timestamp"],
        )
        yield nodes, relationships


def fake_update(
    generator: Generator,
    nodes: dict,
    relationships: list,
    n_updates: int,
    interval_in_days: datetime.timedelta,
) -> Optional[Tuple[dict, list]]:
    """Updates the database.

    Adds new relationships and entities & updates existing ones by adding properties.

    Args:
      generator: one-node-and-one-relationship generator
      nodes: nodes in database
      relationships: relationships in database
      n_updates: the number of changes we want to make on the fake-database
      updates_interval: the number of years during which the changes were made

    Returns:
      modified nodes and relationships after assigning the generated ones

    """
    global _date
    for _ in range(n_updates):
        _date += interval_in_days
        operation = rand.get_random_item(["generate", "update"])
        if operation == "update":
            to_update = rand.get_random_item(["nodes", "rels"])
            if to_update == "nodes":
                node_id = rand.get_random_item(nodes)
                new_properties = node_properties.create(iterations=randint(1, 3))
                properties_dict = {}
                for item in new_properties:
                    properties_dict.update(item)
                entity = graph.get_entity_by_id(node_id)
                if not entity:
                    logging.error(
                        "Node with Id %s is not in database\nNothing has been updated", node_id
                    )
                    return None
                kinds_frozenset = entity.labels
                kind = next(iter(kinds_frozenset))
                graph.ontology.create_entity_kind_properties(
                    kind,
                    new_property_kinds=list(properties_dict.keys())
                )

                graph.ontology.create_entity_kind_properties(
                    kind,
                    list(properties_dict.keys())
                )
                graph.create_or_update_properties_of_entity(
                    id_=node_id,
                    list_of_property_kinds=list(properties_dict.keys()),
                    list_of_property_values=list(properties_dict.values()),
                    change_date=_date,
                )
            else:
                rel = rand.get_random_item(relationships)
                new_property = relationship_properties.create(iterations=1)[0]
                rel_types = [type(value) for value in new_property.values()]
                graph.ontology.create_relationship_kind_properties(
                    next(iter(graph.get_entity_by_id(rel["start"]["Id"]).labels)),
                    rel["label"],
                    next(iter(graph.get_entity_by_id(rel["end"]["Id"]).labels)),
                    new_property_kinds=list(new_property.keys()),
                    new_property_types=rel_types,
                )
                graph.update_relationship(
                    relationship_kind=rel["label"],
                    id_a=rel["start"]["Id"],
                    id_b=rel["end"]["Id"],
                    updated_property_kinds=list(new_property.keys()),
                    updated_property_values=list(new_property.values()),
                    change_date=_date,
                )
        elif operation == "generate":
            nodes, relationships = next(generator)
    return nodes, relationships


def generate_specific_amount_of_data(
    num_users, num_entities, num_relationships, interval_in_days
) -> Tuple[dict, list]:
    """Method 2 to generate data.

    Generates specific number of: user entities, other random entities, and relationships.

    Args:
      num_users: number of users to generate
      num_entities: number of random entities to generate
      num_relationships: number of random relationships to generate
      interval_in_days: the period, after which the next change happens

    Returns:
      generated nodes and relationships

    """
    global _date

    some_users = users.create(iterations=num_users)
    some_entities = entities.create(iterations=num_entities)
    nodes = some_users + some_entities
    nodes_dict = {}
    for item in nodes:
        nodes_dict.update(**item)
    relationships = generate_rels(num_relationships, nodes_dict)

    for node in nodes:
        node = node[next(iter(node))]
        node["properties"].update(
            {"Id": node["Id"], "_creation_timestamp": _date}
        )

        node_kind = node["labels"][0]
        node_parent_kind = next(iter(rand.get_random_item(NODE_LABELS)))
        while node_parent_kind == node_kind:
            node_parent_kind = next(iter(rand.get_random_item(NODE_LABELS)))

        graph.ontology.create_entity_kind(
            node_kind,
            parent=node_parent_kind,
            kind_properties=list(node["properties"].keys())
        )
        graph.create_entity(
            kind=node_kind,
            id_=node["properties"].pop("Id"),
            property_kinds=list(node["properties"].keys()),
            property_values=list(node["properties"].values()),
            create_date=node["properties"]["_creation_timestamp"],
        )
    for rel in relationships:
        _date += interval_in_days
        rel["properties"].update({"Id": rel["Id"], "_creation_timestamp": _date})
        graph.create_relationship(
            id_a=rel["start"]["Id"],
            relationship_kind=rel["label"],
            rel_property_kinds=list(rel["properties"].keys()),
            rel_property_values=list(rel["properties"].values()),
            id_b=rel["end"]["Id"],
            create_date=rel["properties"]["_creation_timestamp"],
        )
    return nodes_dict, relationships
