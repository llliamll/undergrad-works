public static void main(String[] args) throws Exception
{
	BSTreeP6<String> tree1 = new BSTreeP6<String>( args[0] );
		System.out.format( "\ntree1: loaded from %s contains %d nodes on %d levels:\n", args[0], tree1.countNodes(), tree1.countLevels() );
		System.out.print("IN ORDER tree1:    "); tree1.printInOrder();
		System.out.print("LEVEL ORDER tree1: "); tree1.printLevelOrder();
		int[] levelCounts = tree1.calcLevelCounts();
		System.out.println();
		for (int i = 0 ; i<levelCounts.length; ++i )
			System.out.format("level:%2d   %d\n",i,levelCounts[i] );
		
		
		// REMOVE SEVERAL NODES WHO HAVE 2 CHILDREN
		tree1.remove( "C" ); tree1.remove( "I" ); tree1.remove( "P" ); 	tree1.remove( "W" ); 
}