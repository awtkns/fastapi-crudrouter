def get_pk_type(schema, pk_field) -> type:
    try:
        print(schema, pk_field)
        return schema.__fields__[pk_field].type_
    except KeyError:
        return int
