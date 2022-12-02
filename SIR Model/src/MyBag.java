import java.util.*;

    @SuppressWarnings("unchecked")
    public class MyBag<T> implements Iterable<T>
    {
        //initialize bag using linked list
        private int count;
        private Node head;
        private class Node { T key;Node next; }

        //bag c'tor
        public MyBag()
        {
            head = null;
            count = 0;
        }
        //return number of items in the bag
        public int count()
        {
            Node curr = head;
            while(curr != null)
            {
                count++;
                curr = curr.next;
            }
            return count;
        }
        //add new item into the end of the bag or tail of the list
        public void add(T data)
        {
            Node newNode = new Node();

            if(head == null)
            {
                head = newNode;
                head.key = data;
            }
            else
            {
                Node curr = head;
                while(curr.next != null)
                {
                    curr = curr.next;
                }
                curr.next = newNode;
                curr.next.key = data;
            }

        }
        //temp test function
        public void printBag()
        {
            Node curr = head;
            while(curr != null)
            {
                System.out.print(curr.key + " ");
                curr = curr.next;
            }
        }

        private class ListIterator implements Iterator<T>
        {
            //initialize the cursor point to the first item
            Node curr = head;
            public boolean hasNext() { return curr != null; }

            public T next()
            {
                if(!hasNext()){ return null; }
                else
                {
                    T currVal = curr.key;
                    curr = curr.next;
                    return currVal;
                }
            }

            public void remove()
            {
                throw new UnsupportedOperationException();
            }
        }

        public Iterator<T> iterator() { return new ListIterator(); }

    }


   /* class Node<T>
    {
        T key;
        Node next;

        @SuppressWarnings("unchecked")
        Node(T data)
        {
            this.key = data;
            this.next = null;
        }

        public void setNext(Node nextNode)
        {
            this.next = nextNode;
        }

        public Node getNext()
        {
            return this.next;
        }
    }*/