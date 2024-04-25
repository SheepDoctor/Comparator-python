package Java;

import java.util.Scanner;

public class test {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt();
        for(int i = 0; i < n; i++){
            int temp = scanner.nextInt();
            System.out.print(temp + " ");
        }
        System.out.println();
        scanner.close();
    }
}
