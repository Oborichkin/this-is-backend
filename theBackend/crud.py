from .db import conn


def get_all_entity_names():
    query = "MATCH (e:Entity) RETURN e.name as name"
    return [f' {record["name"]} 'for record in conn.query(query)]


def search_entity(name):
    query = f"""
            MATCH (e:Entity)<-[:CONTAINS]-(sent:Sentence)<-[:CONTAINS]-(sec:Section)<-[:CONTAINS]-(ch:Chapter)
            WHERE toLower(e.name) CONTAINS "{name.lower()}"
            RETURN e, sent, sec, ch
            """
    return [record.data() for record in conn.query(query)]
