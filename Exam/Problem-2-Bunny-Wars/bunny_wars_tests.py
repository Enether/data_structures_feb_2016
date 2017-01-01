import random
import unittest
from timeout_decorator import timeout
from bunny_wars import BunnyWars


class ListBySuffixTests(unittest.TestCase):
    def setUp(self):
        self.wars = BunnyWars()
        self.suffixes = ["Scars", "Eyes", "Bleeds", "Soldier", "Whip", "SqUuEze", "Hustle"]

    def test_10000_bunnies_without_given_suffix(self):
        bunny_count = 10000
        self.wars.add_room(0)
        for i in range(bunny_count):
            self.wars.add_bunny(str(i) + self.suffixes[3], random.randint(0,4), 0)
        self._10000_bunnies_without_given_suffix()

    @timeout(0.1)
    def _10000_bunnies_without_given_suffix(self):
        for i in range(1000):
            result = self.wars.list_bunnies_by_suffix("DoesntExist")
            self.assertEqual(len(result), 0)

    # FAILS !!!
    def test_10000_bunnies_with_same_suffix_in_one_room(self):
        bunny_count = 10000
        self.wars.add_room(0)
        for i in range(bunny_count):
            self.wars.add_bunny(str(i) + self.suffixes[random.randint(0, len(self.suffixes)-1)], random.randint(0, 4), 0)
        self._10000_bunnies_with_same_suffix_in_one_room()

    @timeout(0.1)
    def _10000_bunnies_with_same_suffix_in_one_room(self):
        for _ in range(1000):
            len(self.wars.list_bunnies_by_suffix('p'))

    # FAILS !!!
    def test_10000_bunnies_with_shared_suffix_multiple_rooms(self):
        room_count = 5000
        bunny_count = 10000
        for i in range(room_count):
            self.wars.add_room(i)
        for i in range(bunny_count):
            self.wars.add_bunny(str(i) + self.suffixes[random.randint(0, len(self.suffixes) - 1)],
                                random.randint(0, 4),
                                random.randint(0, room_count - 1))
        self._10000_bunnies_with_shared_suffix_multiple_rooms()

    @timeout(0.3)
    def _10000_bunnies_with_shared_suffix_multiple_rooms(self):
        for _ in range(1000):
            self.wars.list_bunnies_by_suffix('ars')


class DetonateBunnyTests(unittest.TestCase):
    def setUp(self):
        self.wars = BunnyWars()

    def test_detonate_one_bunny_multiple_times_with_10000_bunnies_in_room(self):
        bunnies_count = 10000
        self.wars.add_room(4)
        for i in range(bunnies_count):
            self.wars.add_bunny(str(i), i % 4, 4)

        random_bunny = str(random.randint(0, 9999))
        self._detonate_one_bunny_multiple_times_with_10000_bunnies_in_room(random_bunny, bunnies_count)
        self.assertEqual(self.wars.bunny_count(), 2500)

    @timeout(0.4)
    def _detonate_one_bunny_multiple_times_with_10000_bunnies_in_room(self, random_bunny, bunny_count):
        for i in range(bunny_count):
            self.wars.detonate(random_bunny)

    def test_10000_random_detonates_with_10000_bunnies_in_room_same_team(self):
        bunnies_count = 10000
        self.wars.add_room(4)
        for i in range(bunnies_count):
            self.wars.add_bunny(str(i), 0, 4)

    @timeout(0.1)
    def _detonate_10000_random_detonates_with_10000_bunnies_in_room_same_team(self, bunnies_count):
        for i in range(bunnies_count):
            self.wars.detonate(str(random.randint(0, bunnies_count-1)))
        self.assertEqual(self.wars.bunny_count(), bunnies_count)

    def test_detonate_with_4_out_of_5_bunnies_detonating_consecutively_in_every_room_with_10000_bunnies_in_2000_rooms_different_teams(self):
        rooms_count = 2000
        bunnies_count = 10000
        for i in range(rooms_count):
            self.wars.add_room(i)
        for i in range(bunnies_count):
            self.wars.add_bunny(str(i), i % 5, i // 5)

    @timeout(0.1)
    def _detonate_with_4_out_of_5_bunnies_detonating_consecutively_in_every_room_with_10000_bunnies_in_2000_rooms_different_teams(self, bunny_count):
        for i in range(bunny_count):
            if i % 5 != 4:
                self.wars.detonate(str(i))
        self.assertEqual(self.wars.bunny_count, 8000)

    def test_detonate_with_10000_detonations_in_reverse_order_10000_bunnies_3334_rooms(self):
        """
        There should be 3 bunnies in a room, therefore there are at most 3 detonations per room,
            which will leave all bunnies at 10HP, not dead
        """
        bunnies_count = 10000
        room_count = 3334
        for i in range(room_count):
            self.wars.add_room(i)
        for i in range(bunnies_count):
            self.wars.add_bunny(str(i), i % 5, i // 3)
        self._detonate_with_10000_detonations_in_reverse_order_10000_bunnies_3334_rooms(bunnies_count)

    @timeout(0.1)
    def _detonate_with_10000_detonations_in_reverse_order_10000_bunnies_3334_rooms(self, bunnies_count):
        for i in reversed(range(bunnies_count)):
            self.wars.detonate(str(i))
        self.assertEqual(self.wars.bunny_count(), bunnies_count)


class AddRoomsTests(unittest.TestCase):
    def setUp(self):
        self.wars = BunnyWars()

    @timeout(0.4)
    def test_add_room_with_50000_rooms(self):
        room_count = 50000
        for i in range(room_count):
            self.wars.add_room(i)
            self.assertEqual(self.wars.room_count(), i+1)


class BunnyWarsAddBunnyTests(unittest.TestCase):
    def setUp(self):
        self.wars = BunnyWars()
        self.name_prefixes = ["Dijkstra", "Krum", "wally", "G", "BBBBBBBbbbbbbbbra"]

    @timeout(0.4)
    def test_add_bunnies_10000_single_room_single_team(self):
        bunny_count = 10000
        self.wars.add_room(0)
        for i in range(bunny_count):
            self.wars.add_bunny(str(i), 0, 0)
            self.assertEqual(self.wars.bunny_count(), i+1)

    @timeout(0.4)
    def test_add_10000_bunnies_with_1000_rooms(self):
        room_count = 1000
        for i in range(room_count):
            self.wars.add_room(i)
        bunny_count = 10000
        for i in range(bunny_count):
            self.wars.add_bunny(str(i), 0, i//10)
            self.assertEqual(self.wars.bunny_count(), i+1)

    @timeout(0.4)
    def test_add_10000_bunnies_with_1000_rooms_5_team(self):
        room_count = 1000
        for i in range(room_count):
            self.wars.add_room(i)
        bunny_count = 10000
        for i in range(bunny_count):
            self.wars.add_bunny(str(i), i % 5, i // 10)
            self.assertEqual(self.wars.bunny_count(), i + 1)

    @timeout(0.4)
    def test_add_10000_random_bunnies_single_room_single_team(self):
        self.wars.add_room(0)
        bunny_count = 10000
        for i in range(bunny_count):
            rand_index = random.randint(0, len(self.name_prefixes)-1)
            name = self.name_prefixes[rand_index] + str(i)
            self.wars.add_bunny(name, 0, 0)
            self.assertEqual(self.wars.bunny_count(), i+1)

    @timeout(0.4)
    def test_add_10000_random_bunnies_1000_room_5_teams(self):
        room_count = 1000
        bunny_count = 10000
        for i in range(room_count):
            self.wars.add_room(i)
        for i in range(bunny_count):
            rand_index = random.randint(0, len(self.name_prefixes) - 1)
            name = self.name_prefixes[rand_index] + str(i)
            self.wars.add_bunny(name, random.randint(0, 4), random.randint(0, 999))
            self.assertEqual(self.wars.bunny_count(), i + 1)


    def test_add_bunny_to_a_non_existing_room(self):
        """ Should throw an exception"""
        with self.assertRaises(Exception):
            self.wars.add_bunny("Ivo", 0, 15)

    def test_add_bunny_with_an_existing_name(self):
        """ Should throw an exception """
        self.wars.add_room(15)
        self.wars.add_bunny("Ivo", 0, 15)
        with self.assertRaises(Exception):
            self.wars.add_bunny("Ivo", 0, 15)

    def test_add_bunny_with_negative_team_id(self):
        """ Should throw an exception """
        self.wars.add_room(15)
        with self.assertRaises(Exception):
            self.wars.add_bunny("Ivo", -1, 15)

    def test_add_bunny_with_an_incorrect_team_id(self):
        """ Should throw an exception """
        self.wars.add_room(15)
        with self.assertRaises(Exception):
            self.wars.add_bunny("Ivo", 5, 15)

    def test_add_bunny_with_no_bunnies_should_increase_count(self):
        self.wars.add_room(15)

        self.assertEqual(self.wars.bunny_count(), 0)

        self.wars.add_bunny("Ivo", 1, 15)

        self.assertEqual(self.wars.bunny_count(), 1)

    def test_add_bunny_with_existing_bunnies_should_increase_count(self):
        self.wars.add_room(15)
        self.wars.add_bunny("Ivo", 1, 15)
        self.wars.add_bunny("Andre", 1, 15)
        self.wars.add_bunny("Heard", 1, 15)
        self.wars.add_bunny("Dall", 1, 15)
        self.wars.add_bunny("Puddle", 1, 15)

        self.assertEqual(self.wars.bunny_count(), 5)
        self.wars.add_bunny('Turn', 2, 15)
        self.assertEqual(self.wars.bunny_count(), 6)

    def test_add_bunny_with_no_bunnies(self):
        """ Should add the bunny with correct parameters """
        bunny_name = "Dal"
        bunny_team = 3
        bunny_room = 15
        bunny_health = 100
        bunny_score = 0
        self.wars.add_room(bunny_room)
        self.wars.add_bunny(bunny_name, bunny_team, bunny_room)

        bunnies = self.wars.list_bunnies_by_team(bunny_team)
        result_bunny = next(bunnies)

        self.assertEqual(result_bunny.name, bunny_name)
        self.assertEqual(result_bunny.team, bunny_team)
        self.assertEqual(result_bunny.room, bunny_room)
        self.assertEqual(result_bunny.health, bunny_health)
        self.assertEqual(result_bunny.score, bunny_score)


if __name__ == '__main__':
    unittest.main()
