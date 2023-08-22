#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void init() {
	setvbuf(stdin, 0, 2, 0);
	setvbuf(stdout, 0, 2, 0);
	setvbuf(stderr, 0, 2, 0);
	alarm(60);
}

void tournament() {
    FILE *fp;
    unsigned long guess;
    unsigned long random_number;
    
    // Open /dev/urandom for reading
    fp = fopen("/dev/urandom", "r");
    if (fp == NULL) {
        printf("Error opening /dev/urandom.\n");
        exit(1);
    }

    // Read 4 bytes from /dev/urandom into the random_number variable
    fread(&random_number, sizeof(unsigned long), 1, fp);

    // Close /dev/urandom
    fclose(fp);

    // Do something with the random number
    printf("Now you enter the Charity Gamble Tournament\n");
    printf("This is the final round\n");
    printf("Win the flag or Lose the game\n");
    printf("Enter your guess:");
    scanf("%s", &guess);

    if (guess == random_number) {
        printf("You are the god of gamblers!\n");
        printf("Here is your flag!\n");
        win();
    } else {      
	    printf("You lose!");
    }
    return 0;
}

void win(){
    FILE *fp;
    char flag[40];;
    // Open the file for reading
    fp = fopen("flag.txt", "r");
    if (fp == NULL) {
        printf("Error opening file.\n");
        exit(1);
    }

    fread(&flag, 40, 1, fp);
    printf("%s", flag);
}


int main() {
    int dice1, dice2, dice3, points, guess, result, bet;
    int balance = 20; // initialize the player's balance to 20
    int goal = 25000000; // set the goal to 25,000,000

	init();

    srand(time(NULL)); // seed the random number generator with the current time

    printf("Welcome to the dice game!\n");
    printf("You have $%d to start with. The goal is to reach $%d.\n", balance, goal);

    while (balance < goal) { // as long as the player has not reached the goal

        printf("Enter your bet (or enter 0 to quit): ");
        scanf("%d", &bet);

        if (bet <= 0) {
            break; // exit the loop if the player chooses to quit
        }

        if (bet > balance) {
            printf("You don't have enough money to place that bet.\n");
            continue; // go back to the top of the loop to ask for a valid bet
        }

        printf("Enter 1 for small or 2 for big: ");
        scanf("%d", &guess);

        dice1 = rand() % 6 + 1; // generate a random number between 1 and 6 for each die
        dice2 = rand() % 6 + 1;
        dice3 = rand() % 6 + 1;
        points = dice1 + dice2 + dice3; // add up the points from the three dice

        // determine if the result is small or big
        if (points >= 3 && points <= 9) {
            result = 1; // small
        } else {
            result = 2; // big
        }

        // determine the winner
        if (guess == result) {
            balance += bet; // player wins
            printf("Congratulations, you win $%d!\n", bet);
        } else {
            balance -= bet; // player loses
            printf("Sorry, you lose $%d.\n", bet);
        }

        printf("The result is %d (dice 1: %d, dice 2: %d, dice 3: %d).\n", points, dice1, dice2, dice3);
        printf("Your balance is now $%d.\n", balance);
    }

    if (balance >= goal) {
        printf("Congratulations, you have reached the goal of $%d!\n", goal);
        tournament();
    } else {
        printf("Thanks for playing! Your final balance is $%d.\n", balance);
    }

    return 0;
}
