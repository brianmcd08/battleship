from battleship.fleet import Fleet


def test_add_ship(submarine_horizontal):
    fleet = Fleet()
    assert fleet.get_ships_count() == 0
    fleet.add_ship(submarine_horizontal)
    assert fleet.get_ships_count() == 1


def test_unique_type(submarine_horizontal, submarine_vertical):
    fleet = Fleet()
    assert fleet.add_ship(submarine_horizontal)
    assert not fleet.add_ship(submarine_vertical)
    assert fleet.get_ships_count() == 1


def test_overlap(destroyer, battleship):
    fleet = Fleet()
    assert fleet.add_ship(destroyer)
    assert not fleet.add_ship(battleship)
    assert fleet.get_ships_count() == 1
