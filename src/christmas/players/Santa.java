package christmas.players;

import christmas.*;

/**
 * Drunken, dickhead Santa Claus.
 */
public class Santa implements Player {

    private int health;
    private int stamina;
    private int specialProgress;
    private int xp;

    private int drunkeness; // TODO: give to each other player, have it diminish their attacks and defends on a scale
                            // of 1% to 100% according to their drunkeness given by Santa

    private Game game;
    private Player opponent;

    public Santa(Game game, Player opponent) {
        this.game = game;
        this.opponent = opponent;
    }

    // Everything Santa says is drunk text. Make the drunkenness random (Drunkness Translator, written by Ben)
    // Drunkenly steps when he tries to move (just a slightly random force pushing him in random directions)

    public void attack() {
        // TODO:
        // questionable gift - "it doesn't quite look right, but he says it was on your Christmas list" targeted to each
        // opponent. 50% chance of being a gift that
        // person genuinely wants and increases their stamina, health, or whatever. 25% chance of whiskey. 20%, it's
        // like a bomb, poison, or some shit. 4% coal. 1% it's vomit.
    }

    public void defend() {
        // TODO:
        // big sip - "Santa take big sip" and becomes more accepting and relaxed to impact. Attacks are diminished by
        // 20%. "That all you got, pussy?"
    }

    public void special() {
        // TODO:
        // elf rain - multiple simple elves travel from top to bottom of screen and you must dodge them. 1 hit does 20%
        //            damage
        // hitman - large will ferrell-esque bot chases you for 15 seconds. Each hit does 10% damage. While chasing you,
        //          says will ferrell quotes from Elf.
    }
}
