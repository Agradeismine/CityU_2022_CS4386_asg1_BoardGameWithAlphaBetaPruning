import java.util.ArrayList;
import java.util.Arrays;

public class TestMain {
    final static int INFINITY = Integer.MAX_VALUE;

    public static int calNewScore(ArrayList state, Boolean isAI, int oldScore, int[] newMove) {
        // if newMove in same row or newMove in same column contain 3/6 adjacent
        // (linked together) cells, then add 3/6 scores.
        // int newScore = oldScore;
        int score=0;
        int row = newMove[0];
        int column = newMove[1];

        ArrayList this_row = (ArrayList) state.get(row);
        // if not contain NULL in row/1horizontal
        if (!this_row.contains(null)) {
            score += 6;
        } else {
            // count is there "only 3" continuous cells near newMove
            if (this_row.get(0) != null && this_row.get(1) != null && this_row.get(2) != null
                    && this_row.get(3) == null) {
                if (column == 0 || column == 1 || column == 2) {
                    score += 3;
                    // System.out.println("1horizontal 3");
                }
            } else if (this_row.get(0) == null && this_row.get(1) != null && this_row.get(2) != null
                    && this_row.get(3) != null && this_row.get(4) == null) {
                if (column == 1 || column == 2 || column == 3) {
                    score += 3;
                    // System.out.println("2horizontal 3");
                }
            } else if (this_row.get(1) == null && this_row.get(2) != null && this_row.get(3) != null
                    && this_row.get(4) != null && this_row.get(5) == null) {
                if (column == 2 || column == 3 || column == 4) {
                    score += 3;
                    // System.out.println("3horizontal 3");
                }
            } else if (this_row.get(2) == null && this_row.get(3) != null && this_row.get(4) != null
                    && this_row.get(5) != null) {
                if (column == 3 || column == 4 || column == 5) {
                    score += 3;
                    // System.out.println("4horizontal 3");
                }
            }
        }

        ArrayList row0 = (ArrayList) state.get(0);
        ArrayList row1 = (ArrayList) state.get(1);
        ArrayList row2 = (ArrayList) state.get(2);
        ArrayList row3 = (ArrayList) state.get(3);
        ArrayList row4 = (ArrayList) state.get(4);
        ArrayList row5 = (ArrayList) state.get(5);
        // if not contain NULL in column/vertical
        if (row0.get(column) != null && row1.get(column) != null && row2.get(column) != null && row3.get(column) != null
                && row4.get(column) != null && row5.get(column) != null) {
                    score += 6;
            // System.out.println("vertical 6");
        } else {
            if (row0.get(column) != null && row1.get(column) != null && row2.get(column) != null
                    && row3.get(column) == null) {
                if (row == 0 || row == 1 || row == 2) {
                    score += 3;
                    // System.out.println("1vertical 3");
                }
            } else if (row0.get(column) == null && row1.get(column) != null && row2.get(column) != null
                    && row3.get(column) != null && row4.get(column) == null) {
                if (row == 1 || row == 2 || row == 3) {
                    score += 3;
                    // System.out.println("2vertical 3");
                }
            } else if (row1.get(column) == null && row2.get(column) != null && row3.get(column) != null
                    && row4.get(column) != null && row5.get(column) == null) {
                if (row == 2 || row == 3 || row == 4) {
                    score += 3;
                    // System.out.println("3vertical 3");
                }
            } else if (row2.get(column) == null && row3.get(column) != null && row4.get(column) != null
                    && row5.get(column) != null) {
                if (row == 3 || row == 4 || row == 5) {
                    score += 3;
                    // System.out.println("4vertical 3");
                }
            }
        }

        return isAI? oldScore+score : oldScore-score;
    }


    public static Boolean isEndGame(ArrayList state) {
        boolean isEndGame = true;

        for (int i = 0; i < state.size(); i++) {
            if (((ArrayList) state.get(i)).contains(null)) {
                isEndGame = false;
                break;
            }
        }

        return isEndGame;
    }

    public static ABNegamaxResult abNegamax(ArrayList state, int score, Boolean isAI, int aplha, int beta) {
        if (isEndGame(state) ) { //|| depth ==3
            System.out.println("Line 110, Current board:");
            for (int i = 0; i < 6; i++) { // test, print board state
                System.out.println(state.get(i));
            }
            // quit method
            return new ABNegamaxResult(score, null);
        }

        int[] bestMove = new int[2];
        int bestScore = -INFINITY;

        for (int row = 0; row < 6; row++) {
            for (int column = 0; column < 6; column++) {
                if (((ArrayList) state.get(row)).get(column) == null) {
                    ArrayList<ArrayList> newBorad = new ArrayList<ArrayList>();
                    for (int i = 0; i < state.size(); i++) {
                        newBorad.add(new ArrayList<ArrayList>((ArrayList) state.get(i)));
                    }

                    ((ArrayList) newBorad.get(row)).set(column, "A");
                    int[] newMove = new int[] { row, column };
                    /* here to calcu the score for newBoard? */
                    int newBoradScore = calNewScore(newBorad, !isAI, score, newMove);

                    // Recurse
                    ABNegamaxResult recursedResult = abNegamax(newBorad, newBoradScore, !isAI, -beta,
                            -1 * Math.max(aplha, bestScore));
                    int currentScore = -recursedResult.bestScore;

                    // Update the best score
                    if (currentScore > bestScore) {
                        bestScore = currentScore;
                        bestMove = newMove;
                    }

                    if (bestScore >= beta)
                        break;

                    /***** for test *****/
                    // System.out.println();
                    // System.out.println("loop: row:" + row + ", col:" + column);
                    // // Print current state before AI Move:
                    // for (int i = 0; i < 6; i++) {
                    // System.out.println(newBorad.get(i));
                    // }
                    /***** for test *****/
                }
            }
        }

        // retrun bestScore, bestMove
        return new ABNegamaxResult(bestScore, bestMove);
    }

    public static void main(String[] args) {
        ArrayList<ArrayList> state = new ArrayList<>();
        int[] move = new int[2];

        // state.add(new ArrayList<>(Arrays.asList("O", "O", "O", "O", "O", "O")));
        // state.add(new ArrayList<>(Arrays.asList("O", "O", "O", "O", "O", "O")));
        // state.add(new ArrayList<>(Arrays.asList("O", "O", "O", "O", "O", "O")));
        // state.add(new ArrayList<>(Arrays.asList("O", "O", "O", "O", "O", "O")));
        // state.add(new ArrayList<>(Arrays.asList(null, "O", "O", "O", "O", null)));
        // state.add(new ArrayList<>(Arrays.asList("O", "O", "O", "O", null, "O")));

        // state.add(new ArrayList<>(Arrays.asList("o", "O", "O", "O", "O", "O")));
        // state.add(new ArrayList<>(Arrays.asList("O", "O", "O", "O", "O", "O")));
        // state.add(new ArrayList<>(Arrays.asList("O", "O", "O", "O", "O", "O")));
        // state.add(new ArrayList<>(Arrays.asList("O", "O", "O", "O", "O", null)));
        // state.add(new ArrayList<>(Arrays.asList("O", "O", "O", "O", "O", null)));
        // state.add(new ArrayList<>(Arrays.asList("O", "O", "O", "O", null, "O")));

        // state.add(new ArrayList<>(Arrays.asList("O", "O", "O", "O", null, "O")));
        // state.add(new ArrayList<>(Arrays.asList("O", "O", "O", "O", "O", "O")));
        // state.add(new ArrayList<>(Arrays.asList("O", "O", "O", null, "O", "O")));
        // state.add(new ArrayList<>(Arrays.asList("O", "O", "O", null, "O", "O")));
        // state.add(new ArrayList<>(Arrays.asList(null, "O", "O", "O", "O", "O")));
        // state.add(new ArrayList<>(Arrays.asList(null, "O", "O", "O", "O", "O")));

        // state.add(new ArrayList<>(Arrays.asList("o", "O", "O", "O", "O", "O")));
        // state.add(new ArrayList<>(Arrays.asList("O", "O", "O", "O", "O", "O")));
        // state.add(new ArrayList<>(Arrays.asList("O", "O", "O", "O", "O", "O")));
        // state.add(new ArrayList<>(Arrays.asList("O", "O", "O", "O", "O", null)));
        // state.add(new ArrayList<>(Arrays.asList("O", "O", "O", "O", null, "O")));
        // state.add(new ArrayList<>(Arrays.asList(null, "O", "O", null, "O", null)));

        // state.add(new ArrayList<>(Arrays.asList("o", "O", "O", "O", "O", "O")));
        // state.add(new ArrayList<>(Arrays.asList("O", "O", "O", "O", null, null)));
        // state.add(new ArrayList<>(Arrays.asList("O", "O", "O", "O", "O", "O")));
        // state.add(new ArrayList<>(Arrays.asList("O", "O", "O", "O", "O", "O")));
        // state.add(new ArrayList<>(Arrays.asList("O", "O", "O", "O", "O", "O")));
        // state.add(new ArrayList<>(Arrays.asList(null, "O", "O", null, "O", null)));

        // state.add(new ArrayList<>(Arrays.asList("O", "O", "O", "O", "O", "O")));
        // state.add(new ArrayList<>(Arrays.asList(null, "O", "O", "O", "O", null)));
        // state.add(new ArrayList<>(Arrays.asList("O", "O", "O", "O", "O", "O")));
        // state.add(new ArrayList<>(Arrays.asList("O", "O", "O", "O", "O", "O")));
        // state.add(new ArrayList<>(Arrays.asList("O", "O", "O", "O", "O", "O")));
        // state.add(new ArrayList<>(Arrays.asList(null, "O", "O","O", null, null)));

        state.add(new ArrayList<>(Arrays.asList("O", "O", "O", "O", "O", "O")));
        state.add(new ArrayList<>(Arrays.asList("O", "O", "O", "O", null,  "O")));
        state.add(new ArrayList<>(Arrays.asList("O", "O", "O", "O", null, "O")));
        state.add(new ArrayList<>(Arrays.asList("O", null, null, null, "O", "O")));
        state.add(new ArrayList<>(Arrays.asList(null, "O", "O", "O", "O", "O")));
        state.add(new ArrayList<>(Arrays.asList(null, "O", "O","O",  "O",  "O")));



        // move = abNegamax(state, 0, true, -INFINITY, INFINITY).bestMove;
        System.out.println("john" == "johnn");

        // System.out.println("Line213: Returned move: " + move[0] + "," + move[1]);

    }
}

class ABNegamaxResult {
    int bestScore;
    int[] bestMove = new int[2];

    ABNegamaxResult(int bestScore, int[] bestMove) {
        this.bestScore = bestScore;
        this.bestMove = bestMove;
    }
}