import java.io.*;
import java.util.*;

public class L1_SetOps
{
    public static void main( String args[] ) throws Exception
    {
        BufferedReader infile1 = new BufferedReader( new FileReader( args[0] ) );
        BufferedReader infile2 = new BufferedReader( new FileReader( args[1] ) );

        String[] set1 = loadSet( infile1 );
        Arrays.sort( set1 );
        String[] set2 = loadSet( infile2 );
        Arrays.sort( set2 );
        printSet( "set1: ",set1 );
        printSet( "set2: ",set2 );

        String[] union = union( set1, set2 );
        Arrays.sort( union );
        printSet( "\nunion: ", union );


        String[] intersection = intersection( set1, set2 );
        Arrays.sort( intersection );
        printSet( "\nintersection: ",intersection );

        String[] difference = difference( set1, set2 );
        Arrays.sort( difference );
        printSet( "\ndifference: ",difference );

        String[] xor = xor( set1, set2 );
        Arrays.sort( xor );
        printSet("\nxor: ", xor );

        System.out.println( "\nSets Echoed after operations.");

        printSet( "set1: ", set1 );
        printSet( "set2: ", set2 );

    }// END MAIN

    // USE AS GIVEN - DO NOT MODIFY
    // CAVEAT: This method will not work *correctly* until you write a working doubleLength() method.

    static String[] loadSet( BufferedReader infile ) throws Exception
    {
        final int INITIAL_LENGTH = 5;
        int cnt=0;
        String[] set = new String[INITIAL_LENGTH];
        while( infile.ready() )
        {
            if (cnt >= set.length)
                set = doubleLength( set );
            set[ cnt++ ] = infile.readLine();
        }
        infile.close();
        return trimArray( set, cnt );
    }

    // USE AS GIVEN - DO NOT MODIFY
    static void printSet( String caption, String [] set )
    {
        System.out.print( caption );
        for ( String s : set )
            System.out.print( s + " " );
        System.out.println();
    }


	/* ###############################################################
		For each of the following set operations you must execute the following steps:
		1) dimension an array that is just big enough to handle the largest possible set for that operation.
		2) add the appropriate elements to the array as the operation prescribes.
		3) before returning the array, resize it to the exact size as the number of elements in it.
	*/

    static String[] union( String[] set1, String[] set2 )
    {
        return null; // change this to return a trimmed full array
    }

    static String[] intersection( String[] set1, String[] set2 )
    {
        int count = 0;
        int maxLen = 0;
        String[] intersecSet;

        if(set1.length < set2.length)
        {
            maxLen = set1.length;
            intersecSet = new String[maxLen];

            for(int i = 0; i < maxLen; i++)
            {
                for(int j = 0; j < set2.length; j++)
                {
                    if(set1[i].equals(set2[j]))
                    {
                        intersecSet[i] = set1[i];
                    }
                }
            }

        }
        else
        {
            maxLen = set2.length;
            intersecSet = new String[maxLen];

            for(int i = 0; i < maxLen; i++)
            {
                for(int j = 0; j < set1.length; j++)
                {
                    if(set2[i].equals(set1[j]))
                    {
                        intersecSet[i] = set2[i];
                    }
                }
            }
        }

        for(int i = 0; i < intersecSet.length; i++)
        {
            if(intersecSet[i] != null)
            {
                count++;
            }
        }
        return trimArray(intersecSet, count); // change this to return a trimmed full array
    }

    static String[] difference( String[] set1, String[] set2 )
    {
        return null; // change this to return a trimmed full array
    }

    static String[] xor( String[] set1, String[] set2 )
    {
        return null; // change this to return a trimmed full array
    }

    // return an array of length 2x with all data from the old array stored in the new array
    static String[] doubleLength( String[] old )
    {
        String[] newList = new String[old.length * 2];

        for(int i = 0; i < old.length; i++)
        {
            newList[i] = old[i];
        }

        return newList; // you change accordingly
    }

    // return an array of length==cnt with all data from the old array stored in the new array
    static String[] trimArray( String[] old, int cnt )
    {
        String[] newArr = new String[cnt];

        for(int i = 0; i < cnt; i++)
        {
            newArr[i] = old[i];
        }

        return newArr; // you change accordingly
    }

} // END CLASS