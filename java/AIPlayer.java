/////////////////////////////////// 
// CS4386 Semester B, 2021-2022 
// Assignment 1 
// Name: [YIP Yiu Cheung] 
// Student ID: [55775890]  
///////////////////////////////////
package com;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

public class AIPlayer {
	String name = "AI2";
	String symbole;
	boolean isAI = true;
	int score = 0;
	final int INFINITY = Integer.MAX_VALUE;

	public boolean get_isAI() {
		return isAI;
	}

	public void add_symbole(String symbole1) {
		symbole = symbole1;
	}

	public void add_isAI(boolean isAI1) {
		isAI = isAI1;
	}

	public String get_symbole() {
		return symbole;
	}

	public void add_score(int score1) {
		score = score + score1;
	}

	public int get_score() {
		return score;
	}

	public int calNewScore(ArrayList state, Boolean isAI, int oldScore, int[] newMove) {
		// if newMove in same row or newMove in same column contain 3/6 adjacent(linked
		// together) cells, then add 3/6 scores.
		int score = 0;
		int row = newMove[0];
		int column = newMove[1];

		ArrayList this_row = (ArrayList) state.get(row);
		ArrayList row0 = (ArrayList) state.get(0);
		ArrayList row1 = (ArrayList) state.get(1);
		ArrayList row2 = (ArrayList) state.get(2);
		ArrayList row3 = (ArrayList) state.get(3);
		ArrayList row4 = (ArrayList) state.get(4);
		ArrayList row5 = (ArrayList) state.get(5);

		// if not contain NULL in same row/horizontal
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

		return isAI ? oldScore + score : oldScore - score;
	}

	public ArrayList makeNewBoard(ArrayList state, int[] newMove) {
		ArrayList<ArrayList> newBorad = new ArrayList<ArrayList>();

		for (int i = 0; i < state.size(); i++) {
			newBorad.add(new ArrayList<ArrayList>((ArrayList) state.get(i)));
		}

		((ArrayList) newBorad.get(newMove[0])).set(newMove[1], "A");

		return newBorad;
	}

	public ABNegamaxResult abNegamax(ArrayList state, int score, int depth, Boolean isAI, int aplha, int beta) {
		if (isEndGame(state) || depth == 5) { // 5/7 is best and running time controlled in 10s
			return new ABNegamaxResult(score, null);
		}

		int[] bestMove = new int[2];
		int bestScore = -INFINITY;

		for (int row = 0; row < 6; row++) {
			for (int column = 0; column < 6; column++) {
				if (((ArrayList) state.get(row)).get(column) == null) {
					int[] newMove = new int[] { row, column };

					ArrayList<ArrayList> newBorad = makeNewBoard(state, newMove);

					int newBoradScore = calNewScore(newBorad, !isAI, score, newMove); // if depth is odd, !isAI

					// Recurse. if depth is even, !isAI
					ABNegamaxResult recursedResult = abNegamax(newBorad, newBoradScore, depth + 1, !isAI,
							-beta,
							-1 * Math.max(aplha, bestScore));
					int currentScore = -recursedResult.bestScore;

					// Update the best score
					if (currentScore > bestScore) {
						bestScore = currentScore;
						bestMove = newMove;
					}

					// prune node
					if (bestScore >= beta)
						break;

				}
			}
		}

		return new ABNegamaxResult(bestScore, bestMove);
	}

	public Boolean isEndGame(ArrayList state) {

		for (int i = 0; i < state.size(); i++) {
			if (((ArrayList) state.get(i)).contains(null)) {
				return false;
			}
		}

		return true;
	}

	public int[] get_move(ArrayList state, String symbole) {
		/* only 3 or 6 linked cells will be marked as 3/6 scores */
		ABNegamaxResult result = null;

		int nullCount = 0;
		//check is this a empty board
			for (int i = 0; i < 6; i++) {
				ArrayList this_row = (ArrayList) state.get(i);
				for (int j = 0; j < 6; j++) {
					if ((this_row.get(j)) == null){
						nullCount++;
					}else{
						break;
					}
				}
			}

		if (nullCount == 36) {
			// random move if the board is just start
			result = new ABNegamaxResult(score, new int[] { (int) (Math.random() * 6), (int) (Math.random() * 6) });
		} else {
			result = abNegamax(state, 0, 0, true, -INFINITY, INFINITY);
		}

		return result.bestMove;
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