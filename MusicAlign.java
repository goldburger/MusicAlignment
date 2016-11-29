import java.util.Scanner;
import java.util.HashMap;
import java.util.ArrayList;
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

  public static double[][] sim, v, h, subMatrix;
  public static Trace[][] vTrace, hTrace, simTrace;
  public static HashMap<String, Integer> stringMapping;
  public static ArrayList<String> x, y;
  public static String xComment, yComment;
  public static double gapPenaltyA, gapPenaltyB;
  public static double minVal;
  public static boolean alignGlobal = false;

  public static double subCost(String i, String j) {
    return subMatrix[stringMapping.get(i)][stringMapping.get(j)];
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

  // Prints one of the 2-dimensional value arrays, for use in debugging
  public static void printGraph(double[][] g) {
    for (double[] row : g) {
      String line = "";
      for (double cell : row)
        line += cell + " ";
      System.out.println("[ " + line + "]");
    }
  }

  // Assumes FASTA file input with only one string in file
  // First line must be a comment line opening with '>'
  // Returns a string array where first entry is sequence, second is comment
  public static String[] readString(String filename) {
    File file = new File(filename);
    if (!file.exists() || file.isDirectory()) {
      System.out.println(filename + ": file not found");
      System.exit(1);
    }
    Scanner s = null;
    String[] seqPair = new String[2];
    try {
      s = new Scanner(file);
      seqPair[1] = s.nextLine().substring(1);
      seqPair[0] = "";
      do
        seqPair[0] += s.nextLine();
      while (s.hasNextLine());
    } catch (FileNotFoundException e) {
      e.printStackTrace();
    } finally {
      s.close();
    }
    return seqPair;
  }

  // Breaks up argument string into list of tokens, each corresponding to a note
  public static ArrayList<String> tokenize(String str) {
    ArrayList<String> tokens = new ArrayList<String>();
    for (int i = 0; i < str.length(); i += 2) {
      if (str.charAt(i+1) == '#') {
        tokens.add(str.substring(i, i+3));
        i++;
      }
      else {
        tokens.add(str.substring(i, i+2));
      }
    }
    return tokens;
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
      stringMapping = new HashMap<String, Integer>();
      for (int i = 0; i < alphabet.length; i++){
        stringMapping.put(alphabet[i], i);
      }
      subMatrix = new double[alphabet.length][alphabet.length];
      for (int i = 0; i < alphabet.length; i++) {
        String [] row = s.nextLine().split(" ");
        for (int j = 0; j < alphabet.length; j++) {
          subMatrix[i][j] = Double.parseDouble(row[j]);
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
    if (args.length != 5 && !(args.length == 6 && args[5].equals("-g"))) {
      String usage = "";
      usage += "Usage: java MusicAlign <inputX> <inputY> <sub> <A> <B> -g";
      usage += " inputX: file containing first string to align";
      usage += " inputY: file containing second string to align";
      usage += " sub: file containing substitution matrix for alphabet used in input file";
      usage += " A: integer cost for starting term of affine gap penalty";
      usage += " B: integer cost for extending term of affine gap penalty";
      usage += " -g: optional flag for performing global alignment vs local";
      System.out.println(usage);
      System.exit(1);
    }

    String[] pair = readString(args[0]);
    x = tokenize(pair[0]);
    xComment = pair[1];
    pair = readString(args[1]);
    y = tokenize(pair[0]);
    yComment = pair[1];
    readSubMatrix(args[2]);
    gapPenaltyA = Double.parseDouble(args[3]);
    gapPenaltyB = Double.parseDouble(args[4]);
    if (args.length == 6)
      alignGlobal = true;

    int m = x.size();
    int n = y.size();
    h = new double[m+1][n+1];
    v = new double[m+1][n+1];
    sim = new double[m+1][n+1];
    hTrace = new Trace[m+1][n+1];
    vTrace = new Trace[m+1][n+1];
    simTrace = new Trace[m+1][n+1];

    minVal = Integer.MIN_VALUE + gapPenaltyA + gapPenaltyB + 1;
    h[0][0] = minVal;
    v[0][0] = minVal;
    sim[0][0] = 0;
    hTrace[0][0] = Trace.NONE;
    vTrace[0][0] = Trace.NONE;
    simTrace[0][0] = Trace.NONE;

    // Calculate first row
    for (int i = 1; i <= n; i++) {
      h[0][i] = -1 * (gapPenaltyA + i*gapPenaltyB);
      hTrace[0][i] = (i == 1) ? Trace.SLEFT : Trace.LEFT;
      v[0][i] = minVal;
      vTrace[0][i] = Trace.NONE;
      if (alignGlobal) {
        sim[0][i] = h[0][i];
        simTrace[0][i] = Trace.H;
      }
      else {
        sim[0][i] = 0;
        simTrace[0][i] = Trace.NONE;
      }
    }
    // Calculate first column
    for (int i = 1; i <= m; i++) {
      h[i][0] = minVal;
      hTrace[i][0] = Trace.NONE;
      v[i][0] = -1 * (gapPenaltyA + (i-1)*gapPenaltyB);
      vTrace[i][0] = (i == 1) ? Trace.SUP : Trace.UP;
      if (alignGlobal) {
        sim[i][0] = v[i][0];
        simTrace[i][0] = Trace.V;
      }
      else {
        sim[i][0] = 0;
        simTrace[i][0] = Trace.NONE;
      }
    }
    // Calculate for rest of path graphs
    for (int i = 1; i <= m; i++) {
      for (int j = 1; j <= n; j++) {
        // Set H cell
        if (h[i][j-1] > sim[i][j-1] - gapPenaltyA) {
          h[i][j] = h[i][j-1] - gapPenaltyB;
          hTrace[i][j] = Trace.LEFT;
        }
        else {
          h[i][j] = sim[i][j-1] - gapPenaltyA - gapPenaltyB;
          hTrace[i][j] = Trace.SLEFT;
        }
        // Set V cell
        if (v[i-1][j] > sim[i-1][j] - gapPenaltyA) {
          v[i][j] = v[i-1][j] - gapPenaltyB;
          vTrace[i][j] = Trace.UP;
        }
        else {
          v[i][j] = sim[i-1][j] - gapPenaltyA - gapPenaltyB;
          vTrace[i][j] = Trace.SUP;
        }
        // Set Sim cell
        double max = h[i][j];
        simTrace[i][j] = Trace.H;
        if (v[i][j] > max) {
          max = v[i][j];
          simTrace[i][j] = Trace.V;
        }
        if (sim[i-1][j-1] + subCost(x.get(i-1), y.get(j-1)) > max) {
          max = sim[i-1][j-1] + subCost(x.get(i-1), y.get(j-1));
          simTrace[i][j] = Trace.DIAG;
        }
        if (!alignGlobal) {
          if (0 >= max) {
            max = 0;
            simTrace[i][j] = Trace.NONE;
          }
        }
        sim[i][j] = max;
      }
    }

    int i = m;
    int j = n;
    String alignX = "";
    String alignY = "";
    Trace traceLoc = simTrace[i][j];
    double maxScore = sim[i][j];
    if (!alignGlobal) {
      maxScore = minVal;
      for (int row = 0; row <= m; row++) {
        for (int col = 0; col <= n; col++) {
          if (sim[row][col] > maxScore) {
            maxScore = sim[row][col];
            traceLoc = simTrace[row][col];
            i = row;
            j = col;
          }
        }
      }
    }
    while (traceLoc != Trace.NONE) {
      switch (traceLoc)
      {
        case SUP:
          alignX = x.get(i-1) + alignX;
          alignY = ((x.get(i-1).length() == 3) ? "---" : "--") + alignY;
          i--;
          traceLoc = simTrace[i][j];
          break;
        case UP:
          alignX = x.get(i-1) + alignX;
          alignY = ((x.get(i-1).length() == 3) ? "---" : "--") + alignY;
          i--;
          traceLoc = vTrace[i][j];
          break;
        case SLEFT:
          alignX = ((y.get(j-1).length() == 3) ? "---" : "--") + alignX;
          alignY = y.get(j-1) + alignY;
          j--;
          traceLoc = simTrace[i][j];
          break;
        case LEFT:
          alignX = ((y.get(j-1).length() == 3) ? "---" : "--") + alignX;
          alignY = y.get(j-1) + alignY;
          j--;
          traceLoc = hTrace[i][j];
          break;
        case H:
          traceLoc = hTrace[i][j];
          break;
        case V:
          traceLoc = vTrace[i][j];
          break;
        case DIAG:
          String xPadding = (x.get(i-1).length() < y.get(j-1).length()) ? "_" : "";
          String yPadding = (y.get(j-1).length() < x.get(i-1).length()) ? "_" : "";
          alignX = x.get(i-1) + xPadding + alignX;
          alignY = y.get(j-1) + yPadding + alignY;
          i--;
          j--;
          traceLoc = simTrace[i][j];
          break;
        case NONE:
        default:
          break;
      }
    }

    System.out.println(maxScore);
    System.out.println(alignX);
    System.out.println(alignY);
  }
}
