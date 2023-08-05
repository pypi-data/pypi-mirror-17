"""
This file contains a dictionary of matplotlib subplot layouts

They are used during multiplotting. Sooner or later they should be accessible
with something other than integer keys, as this is hard to comprehend...
"""

layouts = {1: [(1, 2, 1),
               (1, 2, 2)],
           2: [(1, 2, 1),
               (1, 3, 2),
               (1, 3, 3)],
           3: [(1, 2, 1),
               (3, 2, 2),
               (3, 2, 4),
               (3, 2, 6)],
           3.5: [(2, 1, 1),
               (2, 3, 4),
               (2, 3, 5),
               (2, 3, 6)],
           4: [(1, 2, 1),
               (2, 4, 3),
               (2, 4, 4),
               (2, 4, 7),
               (2, 4, 8)],
           5: [(3, 3, (1, 5)),
                (3, 3, 3),
                (3, 3, 6),
                (3, 3, 7),
                (3, 3, 8),
                (3, 3, 9)],
           6: [(1, 2, 1),
               (3, 4, 3),
               (3, 4, 4),
               (3, 4, 7),
               (3, 4, 8),
               (3, 4, 11),
               (3, 4, 12)],
           6.5: [(4, 2, (6, 8)),
               (4, 2, 1),
               (4, 2, 2),
               (4, 2, 3),
               (4, 2, 4),
               (4, 2, 5),
               (4, 2, 7)],               
           9: [(1, 5, (1, 2)),
               (3, 5, 3),
               (3, 5, 4),
               (3, 5, 5),
               (3, 5, 8),
               (3, 5, 9),
               (3, 5, 10),
               (3, 5, 13),
               (3, 5, 14),
               (3, 5, 15)],
           9.5: [(1, 6, (1, 3)),
               (3, 6, 4),
               (3, 6, 5),
               (3, 6, 6),
               (3, 6, 10),
               (3, 6, 11),
               (3, 6, 12),
               (3, 6, 16),
               (3, 6, 17),
               (3, 6, 18)],
           12: [(4, 1, 1),
               (4, 4, 5),
               (4, 4, 6),
               (4, 4, 7),
               (4, 4, 8),
               (4, 4, 9),
               (4, 4, 10),
               (4, 4, 11),
               (4, 4, 12),
               (4, 4, 13),
               (4, 4, 14),
               (4, 4, 15),
               (4, 4, 16)],
           12.5: [(4, 4, (1, 6)),
                (4, 4, 3),
                (4, 4, 4),
                (4, 4, 7),
                (4, 4, 8),
                (4, 4, 9),
                (4, 4, 10),
                (4, 4, 11),
                (4, 4, 12),
                (4, 4, 13),
                (4, 4, 14),
                (4, 4, 15),
                (4, 4, 16)],
           14: [(6, 3, (1, 5)),
                (6, 3, 3),
                (6, 3, 6),
                (6, 3, 7),
                (6, 3, 8),
                (6, 3, 9),
                (6, 3, 10),
                (6, 3, 11),
                (6, 3, 12),
                (6, 3, 13),
                (6, 3, 14),
                (6, 3, 15),
                (6, 3, 16),
                (6, 3, 17),
                (6, 3, 18)]
          }
