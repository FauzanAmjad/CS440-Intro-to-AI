/**
 * 
 */

/**
 * @author fauzanamjad
 *
 */

import java.util.*;
public class Grid_Generation {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		// TODO Auto-generated method stub
	
		
		int x = 100;
		int y = 50;
		
		
		int txt_rows = (x*y) + 3;
		
		
			
		int[][] txt_data = new int[3][txt_rows];
		
		int start_x;
		int start_y;
		int end_x;
		int end_y;
		
		while(true) {
			start_x = (int)Math.floor(Math.random()*(x-1+1)+1);
			start_y = (int)Math.floor(Math.random()*(y-1+1)+1);
			end_x = (int)Math.floor(Math.random()*(x-1+1)+1);
			end_y = (int)Math.floor(Math.random()*(y-1+1)+1);
			
			
			if(!(start_x == end_x && start_y == end_y)) {
				break;
			}
			
		}
		
		int[][] txt_array = new int[txt_rows][3];
		
		txt_array[0][0] = start_y;
		txt_array[0][1] = start_x;
		txt_array[0][1] = -1;
		txt_array[1][0] = end_y;
		txt_array[1][1] = end_x;
		txt_array[1][1] = -1;
		txt_array[2][0] = x;
		txt_array[2][1] = y;
		txt_array[2][1] = -1;
		
		System.out.println(start_x + " " + start_y);
		System.out.println(end_x + " " + end_y);
		System.out.println("100 50");
		
		int number_grey = (int)(0.1 * (x*y));
		ArrayList<Integer> grey_or_not = new ArrayList<Integer>();
		
		for(int i = 0; i < ((x*y) - number_grey); i++) {
			grey_or_not.add(0);
		}
		for(int i = 0; i < (number_grey); i++) {
			grey_or_not.add(1);
			
		}
		
		Collections.shuffle(grey_or_not);
		Collections.shuffle(grey_or_not);
		Collections.shuffle(grey_or_not);
		Collections.shuffle(grey_or_not);
		Collections.shuffle(grey_or_not);
		Collections.shuffle(grey_or_not);
		Collections.shuffle(grey_or_not);
		
		Random rand = new Random();
		
		
		for(int i = 1; i <= x; i++) {
			
			for(int j = 1; j <= y; j++) {
				
				int location = rand.nextInt(grey_or_not.size());
				int random_number = grey_or_not.get(location);
				grey_or_not.remove(location);
				System.out.println(i + " " + j + " " + random_number);
				
			}
			
		}
			
		
		

	}

}
