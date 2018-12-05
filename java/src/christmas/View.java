package christmas;

import christmas.players.*;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.util.*;
import java.util.function.Consumer;
import java.util.function.Function;

public class View implements KeyListener, ActionListener {

    // TODO: Listen for user input

    // TODO: Simple game drawing library
    // TODO: Probably use Swing for drawing everything? Not sure.

    List<Consumer> actionSubscribers;

    public void View() {
        actionSubscribers = new ArrayList<>();
    }

    private void notifySubscribers(Action action) {
        for (Consumer subscriber : actionSubscribers) {
            subscriber.accept(action);
        }
    }

    /**
     * Draw game dialog for user interactions.
     * @param title
     * @param message
     */
    private void dialog(String title, String message) {
        // TODO
    }

    Player selectPlayer() {
        // TODO
        System.out.println("Please select your player: ");
        System.out.println("> You've selected Benjamin!");
        return new Benjamin();
    }

    public void keyPressed(KeyEvent e) {
        // TODO: Detect action based on KeyEvent
        notifySubscribers(Action.UP);
        System.out.println(e.toString());
    }

    @Override
    public void keyReleased(KeyEvent e) {
        notifySubscribers(Action.UP);
        System.out.println(e.toString());
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        notifySubscribers(Action.UP);
        System.out.println(e.toString());
    }

    @Override
    public void keyTyped(KeyEvent e) {
        notifySubscribers(Action.UP);
        System.out.println(e.toString());
    }
}