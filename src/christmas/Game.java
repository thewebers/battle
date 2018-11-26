package christmas;

import christmas.players.*;

public class Game {

    // TODO: Simple game drawing library

    private Player santa;
    private Player opponent;
    public long ticker = 0;

    public void World() {
        opponent = startMenu();
        santa = new Santa(this, opponent);
    }

    public Player startMenu() {
        // TODO: User selects player and world map
        return new Benjamin();
    }

    /**
     * Handle game logic.
     */
    public void play() {

        ticker++;
    }

    /**
     * Draw game dialog for user interactions.
     * @param title
     * @param message
     */
    private void dialog(String title, String message) {
        // TODO
    }
}
