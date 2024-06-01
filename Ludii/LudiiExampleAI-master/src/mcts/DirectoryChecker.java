package mcts;
import java.io.File;

public class DirectoryChecker {

    // Method to check if a directory exists
    public static boolean doesDirectoryExist(String directoryPath) {
        File directory = new File(directoryPath);
        return directory.exists() && directory.isDirectory();
    }

    // Main method for testing
    public static void main(String[] args) {
        // Example directory path (you can change this to test different paths)
        String testDirectoryPath = "C://Users//domin//Documents//UM//Thesis//Code//Sequential-Halving-With-Time-Constraints-In-Ludii//Ludii//LudiiExampleAI-master//src//mcts//";

        // Check if the directory exists
        if (doesDirectoryExist(testDirectoryPath)) {
            System.out.println("The directory exists.");
        } else {
            System.out.println("The directory does not exist.");
        }
    }
}