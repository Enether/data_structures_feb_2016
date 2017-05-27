from unittest import TestCase

from b_tree import BNode


class BNodeTests(TestCase):

    def assertElementsInExpectedOrder(self, expected_elements, received_elements):
        self.assertEqual(len(expected_elements), len(received_elements))
        for i in range(len(expected_elements)):
            self.assertEqual(expected_elements[i], received_elements[i])

    def test_addition_sorts(self):
        """
            Given a BTree of order 6, lets add some nodes

            10, 3, 15, 50
            should produce the following root

            3, 10, 15, 50
        """
        root = BNode(order=6)
        root.add(50); root.add(10); root.add(3); root.add(15)
        self.assertElementsInExpectedOrder([3, 10, 15, 50], root.values)

    def test_addition_splits(self):
        """
        Given a BTree of order 6, with the following elements
        10, 3, 15, 27
        """
        root = BNode(order=5)
        root.add(50); root.add(10); root.add(3); root.add(15)
        """
        Add 27 to it
        BTree should now become the following

        3|10|15|27|50 - is full

               15
             /    \
          3|10    27|50
        """
        root.add(27)

        self.assertElementsInExpectedOrder(root.values, [15])
        left_node = root.children[0]
        right_node = root.children[1]

        self.assertElementsInExpectedOrder(left_node.values, [3, 10])
        self.assertEqual(left_node.parent, root)
        self.assertElementsInExpectedOrder(right_node.values, [27, 50])
        self.assertEqual(right_node.parent, root)

    def test_addition_in_middle(self):
        """
               20|30
             /   |   \
          1     25    45
             Add 27

               20|30
             /   |   \
            1  25|27  45
        """
        root = BNode()
        root.values = [20, 30]
        left = BNode()
        left.values = [1]
        mid = BNode()
        mid.values = [25]
        right = BNode()
        right.values = [45]
        root.children = [left, mid, right]

        root.add(27)

        self.assertElementsInExpectedOrder([25, 27], mid.values)

    def test_merge_node(self):
        """
        Given two nodes

        100   |   200  | 300   (A)
       /      |        |      \
    15|20   102  (B)250|270    405
                  /    |    \
               202    260   290|299
        Merge A and B
        """
        A = BNode(order=7)
        B = BNode(order=7, parent=A)
        b_left = BNode(order=7, parent=B); b_left.values = [202]
        b_mid = BNode(order=7, parent=B); b_mid.values = [260]
        b_right = BNode(order=7, parent=B); b_right.values = [290, 299]
        B.values=[250, 270]
        B.children = [b_left, b_mid, b_right]
        a_rightest = BNode(order=7, parent=A); a_rightest.values = [405]
        a_leftest = BNode(order=7, parent=A); a_leftest.values = [15, 20]
        a_midleft = BNode(order=7, parent=A); a_midleft.values = [102]
        A.children = [a_leftest, a_midleft, B, a_rightest]
        A.values = [100, 200, 300]
        # Assert we've built it ok
        self.assertElementsInExpectedOrder(A.children[0].values, [15, 20])
        self.assertElementsInExpectedOrder(A.children[1].values, [102])
        self.assertElementsInExpectedOrder(A.children[2].values, [250, 270])
        self.assertElementsInExpectedOrder(A.children[3].values, [405])

        """
        Merging A and B should produce the following

        100    |    200    |    250    |    270    |    300   (A)
      /        |           |           |           |       \
    15|20     102         202         260       290|300    405
    (B)       (C)         (D)         (E)         (F)       (G)


        """
        A.merge_with_child(B)
        self.assertElementsInExpectedOrder([100, 200, 250, 270, 300], A.values)
        self.assertIsNone(A.parent)

        B = A.children[0]
        self.assertElementsInExpectedOrder([15, 20], B.values)
        self.assertEqual(B.parent, A)

        C = A.children[1]
        self.assertElementsInExpectedOrder([102], C.values)
        self.assertEqual(C.parent, A)

        D = A.children[2]
        self.assertElementsInExpectedOrder([202], D.values)
        self.assertEqual(D.parent, A)

        E = A.children[3]
        self.assertElementsInExpectedOrder([260], E.values)
        self.assertEqual(E.parent, A)

        F = A.children[4]
        self.assertElementsInExpectedOrder([290, 299], F.values)
        self.assertEqual(F.parent, A)

        G = A.children[5]
        self.assertElementsInExpectedOrder([405], G.values)
        self.assertEqual(G.parent, A)

    def test_addition_splits_into_parent(self):
        root = BNode(order=5)
        root.add(50); root.add(10); root.add(3); root.add(15); root.add(27); root.add(60); root.add(70)
        """
               15 (A)
             /    \
     (B)  3|10    27|50|60|70| (C)
        """
        # assert we have what we expect
        A = root
        B = root.children[0]
        C = root.children[1]
        self.assertElementsInExpectedOrder([27, 50, 60, 70], C.values)
        """
        Add 80, our C node gets full, as such splits and goes to the top
               15 (A)
             /    \
     (B)  3|10    27|50|60|70|80| (C)
        This is what should happen
            15 | 60 (A)
          /    |        \
     (B)3|10 (C)27|50   (D)70|80
        """
        A.add(80)
        C = A.children[1]
        D = A.children[2]

        self.assertElementsInExpectedOrder([27, 50], C.values)
        self.assertEqual(A, C.parent)
        self.assertFalse(C._BNode__has_children())
        self.assertElementsInExpectedOrder([70, 80], D.values)
        self.assertEqual(A, D.parent)
        self.assertFalse(D._BNode__has_children())

    def functional_test_add_nodes(self):
        # Following https://www.cs.usfca.edu/~galles/visualization/BTree.html
        """
        """
        root = BNode(order=6)
        root.add(100); root.add(200); root.add(300); root.add(400); root.add(500);
        """
        100 | 200 | 300 | 400 | 500 (A)
        """
        A = root
        self.assertElementsInExpectedOrder([100, 200, 300, 400, 500], A.values)
        """
        Add 303, Should split

            300  (A)
           /    \
   (B)100|200   303|400|500 (C)
        """
        A.add(303)
        B = A.children[0]
        C = A.children[1]

        self.assertElementsInExpectedOrder([300], A.values)
        self.assertElementsInExpectedOrder([100, 200], B.values)
        self.assertElementsInExpectedOrder([303, 400, 500], C.values)
        self.assertEqual(C.parent, A)
        self.assertEqual(B.parent, A)

        """
        Add 325, 350, 125, 150, 175
                               300  (A)
                                /    \
           (B)100|125|150|175|200   303|325|350|400|500 (C)
        """
        A.add(175); A.add(125); A.add(150)
        A.add(325); A.add(350)
        self.assertElementsInExpectedOrder([303, 325, 350, 400, 500], C.values)
        self.assertElementsInExpectedOrder([100, 125, 150, 175, 200], B.values)

        """
        Add 279
        B will fill up, split by 150 and add 150 to A
                        150  |  300 (A)___
                      /      |            \
            (B)100|125  (C)175|200|279   303|325|350|400|500 (D)
        """
        A.add(279)
        self.assertElementsInExpectedOrder([150, 300], A.values)
        self.assertEqual(len(A.children), 3)
        B = A.children[0]
        C = A.children[1]
        D = A.children[2]
        self.assertElementsInExpectedOrder([100, 125], B.values)
        self.assertElementsInExpectedOrder([175, 200, 279], C.values)
        self.assertElementsInExpectedOrder([303, 325, 350, 400, 500], D.values)
        """
        Add 235, 266
                        150  |  300 (A)___
                      /      |            \
            (B)100|125  (C)175|200|235|266|279   303|325|350|400|500 (D)
        """
        A.add(235); A.add(266)
        self.assertElementsInExpectedOrder([175, 200, 235, 266, 279], C.values)
        """
        Add 272,
        C will fill up, split by 235
                  150    |     235      |   300 (A)
               /         |              |           \
        (B)100|125   (C)175|200    (D)266|272|279    303|325|350|400|500 (E)
        """
        A.add(272)
        self.assertElementsInExpectedOrder([150, 235, 300], A.values)
        self.assertEqual(len(A.children), 4)
        B = A.children[0]
        C = A.children[1]
        D = A.children[2]
        E = A.children[3]
        self.assertEqual(A, B.parent)
        self.assertEqual(A, C.parent)
        self.assertEqual(A, D.parent)
        self.assertEqual(A, E.parent)

        self.assertElementsInExpectedOrder([100, 125], B.values)
        self.assertElementsInExpectedOrder([175, 200], C.values)
        self.assertElementsInExpectedOrder([266, 272, 279], D.values)
        self.assertElementsInExpectedOrder([303, 325, 350, 400, 500], E.values)
        """
        Add 699,
        E will fill up, split by 350
                  150    |     235      |   300       |   350  (A)
               /         |              |             |               \
        (B)100|125   (C)175|200    (D)266|272|279  303|325 (E)     400|500|699 (F)
        """
        A.add(699)
        self.assertElementsInExpectedOrder([150, 235, 300, 350], A.values)
        self.assertEqual(len(A.children), 5)
        B = A.children[0]
        C = A.children[1]
        D = A.children[2]
        E = A.children[3]
        F = A.children[4]
        self.assertElementsInExpectedOrder([400, 500, 699], F.values)
        self.assertEqual(F.parent, A)
        self.assertElementsInExpectedOrder([303, 325], E.values)
        self.assertEqual(E.parent, A)
        """
        Add 268, 275
                      150       |        235         |            300       |   350  (A)
               /                |                    |                      |            \
        (B)100|125        (C)175|200       (D)266|268|272|275|279        303|325 (E)   400|500|699 (F)
        """
        A.add(268); A.add(275)
        self.assertElementsInExpectedOrder([266, 268, 272, 275, 279], D.values)
        """
        Add 244
        D will fill up, split by 268

                    150         |          235        |           268            |          300          |      350   (A)
               /                |                     |                          |                       |                 \
        (B) 100|125       (C)175|200          (D) 244|266                 (E) 272|275|279              303|325 (F)        400|500|699 (G)
        """
        A.add(244)
        self.assertElementsInExpectedOrder([150, 235, 268, 300, 350], A.values)
        self.assertEqual(len(A.children), 6)

        B = A.children[0]
        C = A.children[1]
        D = A.children[2]
        E = A.children[3]
        F = A.children[4]
        G = A.children[5]

        self.assertElementsInExpectedOrder([100, 125], B.values)
        self.assertElementsInExpectedOrder([175, 200], C.values)
        self.assertElementsInExpectedOrder([244, 266], D.values)
        self.assertEqual(D.parent, A)
        self.assertElementsInExpectedOrder([272, 275, 279], E.values)
        self.assertEqual(E.parent, A)
        self.assertElementsInExpectedOrder([303, 325], F.values)
        self.assertElementsInExpectedOrder([400, 500, 699], G.values)
        # 50, 20, 30
        """
        Add 50, 20, 30
                    150         |          235        |           268            |          300          |      350   (A)
               /                |                     |                          |                       |                 \
 (B) 20|30|50|100|125       (C)175|200          (D) 244|266                 (E) 272|275|279              303|325 (F)        400|500|699 (G)
        """
        A.add(50); A.add(20); A.add(30)
        self.assertElementsInExpectedOrder([20, 30, 50, 100, 125], B.values)
        """
        At this point, our root A is at its max. A new addition will have it be split and create a new root for us
        So let's do just that!
        Add 1, it will overflow B, which will split into [1, 20] and [50, 100, 125]
        30 will go to A, which will then split into
        [30, 150] and [268, 300, 350]


                    _______________________________________235 (A)_______________________________________
                  /                                                                                       \
              30  |  150(B)                                                             268     |        300         |   350 (C)
           /      |        \                                                       /            |                    |            \
    1|20(D) 50|100|125 (E)  175|200 (F)                                       244|266 (G)    272|275|279 (H)       303|325 (I)    400|500|699 (J)
        """
        A.add(1)
        self.assertElementsInExpectedOrder([235], A.values)
        self.assertEqual(len(A.children), 2)
        B = A.children[0]
        # check B subtree
        self.assertElementsInExpectedOrder([30, 150], B.values)
        self.assertEqual(len(B.children), 3)
        self.assertEqual(B.parent, A)
        D = B.children[0]
        E = B.children[1]
        F = B.children[2]
        self.assertElementsInExpectedOrder([1, 20], D.values)
        self.assertEqual(D.parent, B)
        self.assertElementsInExpectedOrder([50, 100, 125], E.values)
        self.assertEqual(E.parent, B)
        self.assertElementsInExpectedOrder([175, 200], F.values)
        self.assertEqual(F.parent, B)

        # check C subtree
        C = A.children[1]
        self.assertElementsInExpectedOrder([268, 300, 350], C.values)
        self.assertEqual(len(C.children), 4)
        self.assertEqual(C.parent, A)

        G = C.children[0]
        H = C.children[1]
        I = C.children[2]
        J = C.children[3]
        self.assertElementsInExpectedOrder([244, 266], G.values)
        self.assertEqual(G.parent, C)
        self.assertElementsInExpectedOrder([272, 275, 279], H.values)
        self.assertEqual(H.parent, C)
        self.assertElementsInExpectedOrder([303, 325], I.values)
        self.assertEqual(I.parent, C)
        self.assertElementsInExpectedOrder([400, 500, 699], J.values)
        self.assertEqual(J.parent, C)

    def test_remove_leaf(self):
        """
            10|20|30 (A)
            /   |   \
      (B)1|2|3 15|16(C)  45|55 (D)
        """
        root = BNode(order=4)
        root.values = [10,20,30]
        B = BNode(order=4, parent=root)
        B.values = [1,2,3]
        C = BNode(order=4, parent=root)
        C.values = [15, 16]
        D = BNode(order=4, parent=root)
        D.values = [45, 55]
        root.children = [B, C, D]

        root.remove(2)
        root.remove(3)
        root.remove(15)
        root.remove(55)

        self.assertElementsInExpectedOrder([1], B.values)
        self.assertElementsInExpectedOrder([16], C.values)
        self.assertElementsInExpectedOrder([45], D.values)
