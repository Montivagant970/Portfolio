(define (problem minigrid-p1)
    (:domain minigrid)
    (:objects agent1
              key1
              ball1 box1 
              cell1_1 cell1_2 cell1_3 cell1_4 
              cell2_1 cell2_2 cell2_3 cell2_4 
              cell3_1 cell3_2 cell3_3 cell3_4 
              cell4_1 cell4_2 cell4_3 cell4_4
              cell5_1
              cell6_1 cell6_2 cell6_3 cell6_4
              cell7_1 cell7_2 cell7_3 cell7_4
              cell8_1 cell8_2 cell8_3 cell8_4
              cell9_1 cell9_2 cell9_3 cell9_4)

    (:init (connected cell1_1 cell2_1) (connected cell2_1 cell1_1)
           (connected cell1_1 cell1_2) (connected cell1_2 cell1_1)
           (connected cell1_2 cell2_2) (connected cell2_2 cell1_2)
           (connected cell1_2 cell1_3) (connected cell1_3 cell1_2)
           (connected cell1_3 cell2_3) (connected cell2_3 cell1_3)
           (connected cell1_3 cell1_4) (connected cell1_4 cell1_3)
           (connected cell1_4 cell2_4) (connected cell2_4 cell1_4)
           (connected cell2_1 cell3_1) (connected cell3_1 cell2_1)
           (connected cell2_1 cell2_2) (connected cell2_2 cell2_1)
           (connected cell2_2 cell3_2) (connected cell3_2 cell2_2)
           (connected cell2_2 cell2_3) (connected cell2_3 cell2_2)
           (connected cell2_3 cell3_3) (connected cell3_3 cell2_3)
           (connected cell2_3 cell2_4) (connected cell2_4 cell2_3)
           (connected cell2_4 cell3_4) (connected cell3_4 cell2_4)
           (connected cell3_1 cell4_1) (connected cell4_1 cell3_1)
           (connected cell3_1 cell3_2) (connected cell3_2 cell3_1)
           (connected cell3_2 cell4_2) (connected cell4_2 cell3_2)
           (connected cell3_2 cell3_3) (connected cell3_3 cell3_2)
           (connected cell3_3 cell4_3) (connected cell4_3 cell3_3)
           (connected cell3_3 cell3_4) (connected cell3_4 cell3_3)
           (connected cell3_4 cell4_4) (connected cell4_4 cell3_4)
           (connected cell4_1 cell4_2) (connected cell4_2 cell4_1)
           (connected cell4_2 cell4_3) (connected cell4_3 cell4_2)
           (connected cell4_3 cell4_4) (connected cell4_4 cell4_3)

           (connected cell4_1 cell5_1) (connected cell5_1 cell4_1)
           (connected cell5_1 cell6_1) (connected cell6_1 cell5_1)

           (connected cell6_1 cell7_1) (connected cell7_1 cell6_1)
           (connected cell6_1 cell6_2) (connected cell6_2 cell6_1)
           (connected cell6_2 cell7_2) (connected cell7_2 cell6_2)
           (connected cell6_2 cell6_3) (connected cell6_3 cell6_2)
           (connected cell6_3 cell7_3) (connected cell7_3 cell6_3)
           (connected cell6_3 cell6_4) (connected cell6_4 cell6_3)
           (connected cell6_4 cell7_4) (connected cell7_4 cell6_4)
           (connected cell7_1 cell8_1) (connected cell8_1 cell7_1)
           (connected cell7_1 cell7_2) (connected cell7_2 cell7_1)
           (connected cell7_2 cell8_2) (connected cell8_2 cell7_2)
           (connected cell7_2 cell7_3) (connected cell7_3 cell7_2)
           (connected cell7_3 cell8_3) (connected cell8_3 cell7_3)
           (connected cell7_3 cell7_4) (connected cell7_4 cell7_3)
           (connected cell7_4 cell8_4) (connected cell8_4 cell7_4)
           (connected cell8_1 cell9_1) (connected cell9_1 cell8_1)
           (connected cell8_1 cell8_2) (connected cell8_2 cell8_1)
           (connected cell8_2 cell9_2) (connected cell9_2 cell8_2)
           (connected cell8_2 cell8_3) (connected cell8_3 cell8_2)
           (connected cell8_3 cell9_3) (connected cell9_3 cell8_3)
           (connected cell8_3 cell8_4) (connected cell8_4 cell8_3)
           (connected cell8_4 cell9_4) (connected cell9_4 cell8_4)
           (connected cell9_1 cell9_2) (connected cell9_2 cell9_1)
           (connected cell9_2 cell9_3) (connected cell9_3 cell9_2)
           (connected cell9_3 cell9_4) (connected cell9_4 cell9_3)

           (cell cell1_1) (cell cell1_2) (cell cell1_3) (cell cell1_4)
           (cell cell2_1) (cell cell2_2) (cell cell2_3) (cell cell2_4)
           (cell cell3_1) (cell cell3_2) (cell cell3_3) (cell cell3_4)
           (cell cell4_1) (cell cell4_2) (cell cell4_3) (cell cell4_4)
           (cell cell5_1) (locked cell5_1)
           (cell cell6_1) (cell cell6_2) (cell cell6_3) (cell cell6_4)
           (cell cell7_1) (cell cell7_2) (cell cell7_3) (cell cell7_4)
           (cell cell8_1) (cell cell8_2) (cell cell8_3) (cell cell8_4)
           (cell cell9_1) (cell cell9_2) (cell cell9_3) (cell cell9_4)
           
           (agent agent1)
           (free agent1)
           (key key1)
           (obj box1)
           (obj ball1)
           (at agent1 cell1_2)
           (at ball1 cell4_1) (blocked cell4_1)
           (at key1 cell3_3) (blocked cell3_3)
           (at box1 cell9_4) (blocked cell9_4))

    (:goal (hold agent1 box1))
)