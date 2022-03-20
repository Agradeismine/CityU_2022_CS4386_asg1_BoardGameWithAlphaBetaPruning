#include <stdio.h>
#include <iostream>


#include <stdlib.h>
#include <string.h>
using namespace std;
class AIPlayer{
public:
    AIPlayer():name("AI"), symbole('O'),isAI(true),score(0){

    }

    int add_symbole(char symbole1){
    
        symbole = symbole1;
        //cout<<"aiplayer"<<symbole<<endl;
        return 0;
    }
    char get_symbole(){
    	return symbole;
    }
    bool get_isAI(){
    	return isAI;
    }
    int add_score(int score1){
    	score=score+=score1;
    	return 0;
    }
    int add_isAI(bool isAI1){
		isAI=isAI1;
    	return 0;
    }
    int get_score(){
    	return score;
    }

	int* get_move(char state[6][6], char symbole){
		static int* move=new int[2];
	    for (int row=0;row<6;row++){
            for (int column=0;column<6;column++){	
				//cout<<"in ai:"<<state[row][column]<<" ";
            	if (state[row][column]!='X' and state[row][column]!='O' ){
					move[0]=row;
					move[1]=column;

					return move;
                }

            }
            
        }
        return move;
	}

private:
	string name;
	char symbole;
    bool isAI;
    int score;
};



extern "C" {

AIPlayer py;

char get_symbole(){
    return py.get_symbole();
}

int add_symbole(char symbole1){

	return py.add_symbole(symbole1);
}

bool get_isAI(){
    return py.get_isAI();
}
int add_score(int score1){

    return py.add_score(score1);
}
int add_isAI(bool isAI1){

    return py.add_isAI(isAI1);
}
int get_score(){
    return py.get_score();
}

int* get_move(char state[6][6], char symbole){

	return py.get_move(state,symbole);

}
}
