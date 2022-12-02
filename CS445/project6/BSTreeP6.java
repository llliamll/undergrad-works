import java.io.*;
import java.util.*;

///////////////////////////////////////////////////////////////////////////////
class BSTNode<T>
{	T key;
    BSTNode<T> left,right;
    BSTNode( T key, BSTNode<T> left, BSTNode<T> right )
    {	this.key = key;
        this.left = left;
        this.right = right;
    }
}
///////////////////////////////////////////////////////////////////////////////////////
class Queue<T>
{	LinkedList<BSTNode<T>> queue;
    Queue() { queue =  new LinkedList<BSTNode<T>>(); }
    boolean empty() { return queue.size() == 0; }
    void enqueue( BSTNode<T>  node ) { queue.addLast( node ); }
    BSTNode<T>  dequeue() { return queue.removeFirst(); }
    // THROWS NO SUCH ELEMENT EXCEPTION IF Q EMPTY
}
////////////////////////////////////////////////////////////////////////////////
class BSTreeP6<T>
{
    private BSTNode<T> root;
    private int nodeCount;
    private boolean addAttemptWasDupe=false;

    public BSTreeP6()
    {
        nodeCount = 0;
        root=null;
    }

    @SuppressWarnings("unchecked")
    public BSTreeP6( String infileName ) throws Exception
    {
        nodeCount = 0;
        root=null;
        Scanner infile = new Scanner( new File( infileName ) );
        while ( infile.hasNext() )
            add( (T) infile.next() ); // THIS CAST RPODUCES THE WARNING
        infile.close();
    }

    // DUPES BOUNCE OFF & RETURN FALSE ELSE INCR COUNT & RETURN TRUE
    @SuppressWarnings("unchecked")
    public boolean add( T key )
    {	addAttemptWasDupe=false;
        root = addHelper( this.root, key );
        return !addAttemptWasDupe;
    }
    @SuppressWarnings("unchecked")
    private BSTNode<T> addHelper( BSTNode<T> root, T key )
    {
        if (root == null) return new BSTNode<T>(key,null,null);
        int comp = ((Comparable)key).compareTo( root.key );
        if ( comp == 0 )
        { addAttemptWasDupe=true; return root; }
        else if (comp < 0)
            root.left = addHelper( root.left, key );
        else
            root.right = addHelper( root.right, key );

        return root;
    } // END addHelper

    public int size()
    {
        return nodeCount; // LOCAL VAR KEEPING COUNT
    }

    public int countNodes() // DYNAMIC COUNT ON THE FLY TRAVERSES TREE
    {
        return countNodes( this.root );
    }
    private int countNodes( BSTNode<T> root )
    {
        if (root==null) return 0;
        return 1 + countNodes( root.left ) + countNodes( root.right );
    }

    // INORDER TRAVERSAL REQUIRES RECURSION
    public void printInOrder()
    {
        printInOrder( this.root );
        System.out.println();
    }
    private void printInOrder( BSTNode<T> root )
    {
        if (root == null) return;
        printInOrder( root.left );
        System.out.print( root.key + " " );
        printInOrder( root.right );
    }

    public void printLevelOrder()
    {
        if (this.root == null) return;
        Queue<T> q = new Queue<T>();
        q.enqueue( this.root ); // this. just for emphasis/clarity
        while ( !q.empty() )
        {	BSTNode<T> n = q.dequeue();
            System.out.print( n.key + " " );
            if ( n.left  != null ) q.enqueue( n.left );
            if ( n.right != null ) q.enqueue( n.right );
        }
    }

    public int countLevels()
    {
        return countLevels( root );
    }
    private int countLevels( BSTNode root)
    {
        if (root==null) return 0;
        return 1 + Math.max( countLevels(root.left), countLevels(root.right) );
    }

    public int[] calcLevelCounts()
    {
        int levelCounts[] = new int[countLevels()];
        calcLevelCounts( root, levelCounts, 0 );
        return levelCounts;
    }
    private void calcLevelCounts( BSTNode root, int levelCounts[], int level )
    {
        if (root==null)return;
        ++levelCounts[level];
        calcLevelCounts( root.left, levelCounts, level+1 );
        calcLevelCounts( root.right, levelCounts, level+1 );
    }

    /////////////////////////////////////////////////
    // WRITE THE REMOVE METHOD
    // return true only if it finds/removes the node
    public boolean remove( T key2remove )
    {
    	BSTNode<T> parentNode = findParent(key2remove);
        if(parentNode == null)
        {
            return false;
        }

        if(parentNode == this.root && this.root.key.equals(key2remove)) //check if the dead node is current root
        {
        	if(this.root.left == null)
        	{
        		this.root = this.root.right;
        		return true;
        	}
        	else
        	{
				T tempKey = findRightMost(this.root.left).key;
            	remove(tempKey);
            	this.root.key = tempKey;
            	return true;
        	}
        }
        //if dead node is the left child
        if( parentNode.left  != null && parentNode.left.key.equals(key2remove))
        {
        	
            BSTNode<T> deadNode = parentNode.left;                      //set the dead node to the left child
            if(checkLeaf(deadNode))										//leaf case
            {
                parentNode.left = null;
                return true;
            }
            else if(checkOneChild(deadNode))							//one child case
            {
                parentNode.left = findOneChild(deadNode, key2remove);
                return true;
            }
            else 														//two child case
            {
                T tempKey = findRightMost(deadNode.left).key;
                remove(tempKey);
                deadNode.key = tempKey;
                return true;
            }
        }
		//if dead node is the right child
        if( parentNode.right  != null && parentNode.right.key.equals(key2remove))
        {
            BSTNode<T> deadNode = parentNode.right; //set the dead node to the right child
            if(checkLeaf(deadNode))
            {
                parentNode.right = null;
                return true;
            }
            else if(checkOneChild(deadNode))
            {
                parentNode.right = findOneChild(deadNode, key2remove);
                return true;
            }
            else
            {
                T tempKey = findRightMost(deadNode.left).key;
                remove(tempKey);
                deadNode.key = tempKey;
                return true;
            }
        }
        return false;
    }

    //helper functions
    private BSTNode<T> findParent(T key) // find the predecesser of the dead node
    {
        if (this.root == null) return null;
        if(this.root.key.equals(key))
        {
        	return this.root;
        }
        Queue<T> q = new Queue<T>();
        q.enqueue( this.root );
        while ( !q.empty() )
        {
            BSTNode<T> parentNode = q.dequeue();
            if ( parentNode.left  != null && parentNode.left.key.equals(key))
            {
                return parentNode;
            }
            if ( parentNode.right != null && parentNode.right.key.equals(key))
            {
                return parentNode;
            }
            if( parentNode.left != null)
            {
                q.enqueue( parentNode.left );
            }
            if( parentNode.right != null)
            {
                q.enqueue( parentNode.right );
            }

        }
        return null;
    }

    private boolean checkLeaf(BSTNode<T> node)
    {
        if(node.left == null && node.right == null)
        {
            return true;
        }
        else
        {
            return false;
        }
    }

    private boolean checkOneChild(BSTNode<T> deadNode)
    {
        if(deadNode.left != null && deadNode.right != null)//this make sure that it seperates one child case and two child case
        {
            return false;
        }
        if(deadNode.left != null || deadNode.right != null)
        {
            return true;
        }
        return false;
    }

    private BSTNode<T> findOneChild(BSTNode<T> deadNode, T key)
    {

        if(deadNode.left != null)
        {
            return deadNode.left;
        }
        else
        {
            return deadNode.right;
        }
    }

    private BSTNode<T> findRightMost(BSTNode<T> node) //search for the largest node of the left branch
    {
        while(node != null && node.right != null)
        {
            node = node.right;
        }
        return node;
    }


} // END BSTREEP6 CLASS
