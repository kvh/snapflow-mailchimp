from snapflow import graph, produce


def test():
    import {module}

    g = graph()

    # Initial graph
    orders = g.create_node(
        {module}.snaps.Snap,
        params={"config_val": "val"},
    )
    output = produce(orders, modules=[{module}])
    records = output.as_records()
    assert len(records) > 0


if __name__ == "__main__":
    test()