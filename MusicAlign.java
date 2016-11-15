import java.util.Scanner;
import java.util.HashMap;
import java.io.File;
import java.io.FileNotFoundException;

public class MusicAlign {

  // Enum for representing directions in path graphs
  // A cell in H will be either SLEFT or LEFT, corresponding to the left cell in Sim or in H, respectively
  // A cell in V will be either SUP or UP, corresponding to the upper cell in Sim or in V, respectively
  // A cell in Sim will be H, V, or D for being based on H cell, V cell, or diagonal up cell in Sim
  public enum Trace { SLEFT, LEFT, SUP, UP, H, V, DIAG, NONE }
  
  public static String getString(MusicAlign.Trace t) {
    switch (t) {
      case SLEFT: return "LS";
      case LEFT: return "L ";
      case SUP: return "US";
      case UP: return "U ";
      case H: return "H ";
      case V: return "V ";
      case DIAG: return "D ";
      case NONE: return "--";
      default: return "  ";
    }
  }
  
  public static int[][] sim, v, h, subMatrix;
  public static Trace[][] vTrace, hTrace, simTrace;
  public static HashMap<Character, Integer> charMapping;
  public static String x, y;
  public static int gapPenaltyA, gapPenaltyB;
  public static int minVal;
  
  public static int subCost(char i, char j) {
    return subMatrix[charMapping.get(i)][charMapping.get(j)];
  }
  
  // Prints one of the 2-dimensional trace arrays, for use in debugging
  public static void printTrace(Trace[][] traceArr) {
    for (Trace[] tr : traceArr) {
      String line = "";
      for (Trace t : tr)
        line += getString(t) + " ";
      System.out.println("[ " + line + "]");
    }
  }
  
  // Prints one of the 2-dimensional int arrays, for use in debugging
  public static void printGraph(int[][] g) {
    for (int[] row : g) {
      String line = "";
      for (int cell : row)
        line += cell + " ";
      System.out.println("[ " + line + "]");
    }
  }
  
  // Sets X and Y to be pair of strings to be aligned
  // Assumes FASTA file input with only two strings in file
  // First line must be a comment line; strings are separated by a line starting with '>'
  public static void readStrings(String filename) {
    File file = new File(filename);
    if (!file.exists() || file.isDirectory()) {
      System.out.println(filename + ": file not found");
      System.exit(1);
    }
    Scanner s = null;
    try {
      s = new Scanner(file);
      s.nextLine();
      x = "";
      String next = s.nextLine();
      while (next.charAt(0) != '>') {
        x += next;
        next = s.nextLine();
      }
      y = s.nextLine();
      while (s.hasNextLine()) {
        y += s.nextLine();
      }
    } catch (FileNotFoundException e) {
      e.printStackTrace();
    } finally {
      s.close();
    }
  }
  
  // First line of file should be space-separated list of characters in alphabet
  // Remaining lines should be space-separated matrix, where nth row and column represent nth alphabet char
  public static void readSubMatrix(String filename){
    File file = new File(filename);
    if (!file.exists() || file.isDirectory()) {
      System.out.println(filename + ": file not found");
      System.exit(1);
    }
    Scanner s = null;
    try {
      s = new Scanner(file);
      String[] alphabet = s.nextLine().split(" ");
      charMapping = new HashMap<Character, Integer>();
      for (int i = 0; i < alphabet.length; i++){
        charMapping.put(alphabet[i].charAt(0), i);
      }
      subMatrix = new int[alphabet.length][alphabet.length];
      for (int i = 0; i < alphabet.length; i++) {
        String [] row = s.nextLine().split(" ");
        for (int j = 0; j < alphabet.length; j++) {
          subMatrix[i][j] = Integer.parseInt(row[j]);
        }
      }
    } catch (FileNotFoundException e) {
      e.printStackTrace();
    } finally {
      s.close();
    }
  }
  
  // Currently costs A + (k-1)B for gap of k
  // This differs from the Gotoh algorithm! Change to other convention?
  public static void main(String [] args) {
    if (args.length != 4) {
      String usage = "";
      usage += "Usage: java MusicAlign <input> <sub> <A> <B>";
      usage += " input: FASTA file containing two strings to align";
      usage += " sub: file containing substitution matrix for alphabet used in input file";
      usage += " A: integer cost for starting term of affine gap penalty";
      usage += " B: integer cost for extending term of affine gap penalty";
      System.out.println(usage);
      System.exit(1);
    }
    readStrings(args[0]);
    readSubMatrix(args[1]);
    gapPenaltyA = Integer.parseInt(args[2]);
    gapPenaltyB = Integer.parseInt(args[3]);
    minVal = Integer.MIN_VALUE + gapPenaltyA + gapPenaltyB + 1;

    int m = x.length();
    int n = y.length();
    h = new int[m+1][n+1];
    v = new int[m+1][n+1];
    sim = new int[m+1][n+1];
    hTrace = new Trace[m+1][n+1];
    vTrace = new Trace[m+1][n+1];
    simTrace = new Trace[m+1][n+1];
    
    h[0][0] = minVal;
    v[0][0] = minVal;
    sim[0][0] = 0;
    hTrace[0][0] = Trace.NONE;
    vTrace[0][0] = Trace.NONE;
    simTrace[0][0] = Trace.NONE;

    // Calculate first row
    for (int i = 1; i <= n; i++) {
      h[0][i] = -1 * (gapPenaltyA + (i-1)*gapPenaltyB);
      hTrace[0][i] = (i == 1) ? Trace.SLEFT : Trace.LEFT;
      v[0][i] = minVal;
      vTrace[0][i] = Trace.NONE;
      sim[0][i] = h[0][i];
      simTrace[0][i] = Trace.H;
    }
    // Calculate first column
    for (int i = 1; i <= m; i++) {
      h[i][0] = minVal;
      hTrace[i][0] = Trace.NONE;
      v[i][0] = -1 * (gapPenaltyA + (i-1)*gapPenaltyB);
      vTrace[i][0] = (i == 1) ? Trace.SUP : Trace.UP;
      sim[i][0] = v[i][0];
      simTrace[i][0] = Trace.V;
    }
    // Calculate for rest of path graphs
    for (int i = 1; i <= m; i++) {
      for (int j = 1; j <= n; j++) {
        // Set H cell
        if (h[i][j-1] - gapPenaltyB > sim[i][j-1] - gapPenaltyA) {
          h[i][j] = h[i][j-1] - gapPenaltyB;
          hTrace[i][j] = Trace.LEFT;
        }
        else {
          h[i][j] = sim[i][j-1] - gapPenaltyA;
          hTrace[i][j] = Trace.SLEFT;
        }
        // Set V cell
        if (v[i-1][j] - gapPenaltyB > sim[i-1][j] - gapPenaltyA) {
          v[i][j] = v[i-1][j] - gapPenaltyB;
          vTrace[i][j] = Trace.UP;
        }
        else {
          v[i][j] = sim[i-1][j] - gapPenaltyA;
          vTrace[i][j] = Trace.SUP;
        }
        // Set Sim cell
        int max = h[i][j];
        simTrace[i][j] = Trace.H;        
        if (v[i][j] > max) {
          max = v[i][j];
          simTrace[i][j] = Trace.V;
        }
        if (sim[i-1][j-1] + subCost(x.charAt(i-1), y.charAt(j-1)) > max) {
          max = sim[i-1][j-1] + subCost(x.charAt(i-1), y.charAt(j-1));
          simTrace[i][j] = Trace.DIAG;
        }
        sim[i][j] = max;
      }
    }
    
    // Probably does traceback wrong, likely needs correction based on Altschul's fix for Gotoh's traceback
    int i = m;
    int j = n;
    String alignX = "";
    String alignY = "";
    while (simTrace[i][j] != Trace.NONE) {
      switch (simTrace[i][j])
      {
        case V:
          alignX = x.charAt(i-1) + alignX;
          alignY = "-" + alignY;
          i--;
          break;
        case H:
          alignX = "-" + alignX;
          alignY = y.charAt(j-1) + alignY;
          j--;
          break;
        case DIAG:
          alignX = x.charAt(i-1) + alignX;
          alignY = y.charAt(j-1) + alignY;
          i--;
          j--;
          break;
        case NONE:
        default:
          break;
      }
    }
    
    System.out.println(sim[m][n]);
    System.out.println(alignX);
    System.out.println(alignY);
    //printTrace(simTrace);
    //printGraph(sim);
  }
}
