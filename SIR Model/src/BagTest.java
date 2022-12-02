import java.util.*;
public class BagTest {
    public static void main(String[] args)
    {
        MyBag<Integer> intbag = new MyBag<>();
        intbag.add(1);
        intbag.add(2);
        intbag.add(3);

        System.out.println(intbag.count() + " items added to the Integer bag: ");
        intbag.printBag();

        MyBag<String> strbag = new MyBag<>();
        strbag.add("alpha");
        strbag.add("bravo");
        strbag.add("charlie");
        strbag.add("echo");

        System.out.println("\n" + strbag.count() + " items added to the String bag: ");
        strbag.printBag();

        System.out.println();

        MyBag<String> bag ;
        Iterator<String> i ;
        bag = new MyBag<String>() ;
        bag.add("a") ; bag.add("b") ; bag.add("c") ; bag.add("d") ; bag.add("e") ;
        for (String s : bag) { System.out.print( s + " " ) ; }
        System.out.println() ;
        i = bag.iterator() ;

    }


}

/*
public class TestMyBag {
    public static void main(String[] args) {
        MyBag<String> bag ;
        Iterator<String> i ;
        bag = new MyBag<String>() ;
        bag.add("a") ; bag.add("b") ; bag.add("c") ; bag.add("d") ; bag.add("e") ;
        for (String s : bag) { System.out.print( s + " " ) ; }
        System.out.println() ;
        i = bag.iterator() ;
        while (i.hasNext()) { String s = i.next() ; if (s.equals("c")) i.remove() ; }
        for (String s : bag) { System.out.print( s + " " ) ; }
        System.out.println() ;
    }
}*/
