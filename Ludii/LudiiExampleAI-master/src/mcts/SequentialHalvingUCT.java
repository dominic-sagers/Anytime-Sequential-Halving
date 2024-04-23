package mcts;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.concurrent.ThreadLocalRandom;
import game.Game;
import main.collections.FastArrayList;
import other.AI;
import other.RankUtils;
import other.context.Context;
import other.move.Move;
import java.lang.Math.*;

/**
 * A Sequential Halving Agent utilizing UCT.
 * This implementation performs a normal MCTS UCT search until a predetermined iteration limit, then halves the tree from the root node via Sequential Halving.
 * Only supports deterministic, alternating-move games.
 * 
 * 
 * This class is a modified version of the example code provided by Dennis Soemers.
 * @author Dennis Soemers, Dominic Sagers
 */
public class SequentialHalvingUCT extends AI
{
	
	//-------------------------------------------------------------------------
	
	/** Our player index */
	protected int player = -1;
	
	//-------------------------------------------------------------------------
	//Necessary variables for the SH algorithm.
	private final int iterationBudgetMultiplier = 1000;
	private int iterationBudget;
	private int rounds;// A reference for the amount of rounds 
	private int iterPerRound;//Gives how many iterations should be run before halving from the root.
	private int halvingIterations;
	private int numIterations;
	/**
	 * Constructor
	 */
	public SequentialHalvingUCT()
	{
		this.friendlyName = "Sequential Halving UCT";
	}
	
	//-------------------------------------------------------------------------

	@Override
	public Move selectAction
	(
		final Game game,
		final Context context, 
		final double maxSeconds, 
		final int maxIterations, 
		final int maxDepth
	)
	{
		
		
		// Start out by creating a new root node (no tree reuse in this example)
		final Node root = new Node(null, null, context);
		
		// We'll respect any limitations on max seconds and max iterations (don't care about max depth)
		final long stopTime = (maxSeconds > 0.0) ? System.currentTimeMillis() + (long) (maxSeconds * 1000L) : Long.MAX_VALUE;
		final int maxIts = (maxIterations >= 0) ? maxIterations : Integer.MAX_VALUE;
		
		this.iterationBudget = Double.valueOf(maxSeconds).intValue() * iterationBudgetMultiplier;
		this.rounds = (int) Math.ceil(Math.log(iterationBudget));
		this.iterPerRound = (int) Math.ceil(iterationBudget/2);
		this.numIterations = 0;
		this.halvingIterations = 0;

		//ALGORITHM IDEA
		/*while(numIterations < iterationBudget){
			* while(halvingIterations < iterPerRound):
			* 		while(true){
			* 			do UCT from current node
			* 			}
						halvingIterations++

		 * }
		 * if(all root children explored){
		 * halveRoot();
		 * }else{
		 * 
		 * 	currentNode = next child
		 * 
		 * }
		 *	
			}
		 */



		// Our main loop through MCTS iterations
		ArrayList<Integer> hist = new ArrayList<>();
		boolean rootFullyExpanded = false;
		boolean firstRound = true;
		int numPossibleMoves = root.unexpandedMoves.size();
		System.err.println("possible moves: " + numPossibleMoves);
		int rootNodesVisited = 0;

		System.out.println("iterationBudget: " + this.iterationBudget + " \n numIterations: " + this.numIterations);
		System.out.println("Iter per round: " + this.iterPerRound);
		//System.currentTimeMillis() < stopTime && 
		while 
		(
			this.numIterations < (this.iterationBudget) && 					// Respect iteration limit
				// Respect time limit
			!wantsInterrupt								// Respect GUI user clicking the pause button
		)
		{

		// Start in root node
		if(!rootFullyExpanded){
			//System.out.println("starting root search");
			//System.out.println(rootNodesVisited);

			Node current = root;
			
			// Traverse tree
			while (true)
			{
				if (current.context.trial().over())
				{
					// We've reached a terminal state
					break;
				}
				
				current = select(current);
				
				if (current.visitCount == 0)
				{
					// We've expanded a new node, time for playout!
					break;
				}
			}
			
			Context contextEnd = current.context;
			
			if (!contextEnd.trial().over())
			{
				// Run a playout if we don't already have a terminal game state in node
				contextEnd = new Context(contextEnd);
				game.playout
				(
					contextEnd, 
					null, 
					-1.0, 
					null, 
					0, 
					-1, 
					ThreadLocalRandom.current()
				);
			}
			
			// This computes utilities for all players at the of the playout,
			// which will all be values in [-1.0, 1.0]
			final double[] utilities = RankUtils.utilities(contextEnd);
			
			// Backpropagate utilities through the tree
			while (current != null)
			{
				current.visitCount += 1;
				for (int p = 1; p <= game.players().count(); ++p)
				{
					current.scoreSums[p] += utilities[p];
				}
				current = current.parent;
			}
			
			rootNodesVisited++;
			if(rootNodesVisited == numPossibleMoves){
				//System.out.println("First round over");
				firstRound = true;
				rootFullyExpanded = true;
			}

		}else{
			//Exploring nodes still in List
				int nodeIndex = 0;
				Node currentChild = root.children.get(nodeIndex); 
				
				
				while(this.halvingIterations < this.iterPerRound){//checks to see if we are ready to halve from the root
					//System.out.println("running UCT on node: " + nodeIndex);
					//System.out.println(this.halvingIterations);
					//out.println(this.iterPerRound);

					if(firstRound && this.halvingIterations == 0){this.halvingIterations += 1;}
					

						Node current = currentChild;
						
						// Traverse tree
						while (true)
					{
						if (current.context.trial().over())
						{
							// We've reached a terminal state
							break;
						}
						
						current = select(current);
						
						if (current.visitCount == 0)
						{
							// We've expanded a new node, time for playout!
							break;
						}
					}
					
					Context contextEnd = current.context;
					
					if (!contextEnd.trial().over())
					{
						// Run a playout if we don't already have a terminal game state in node
						contextEnd = new Context(contextEnd);
						game.playout
						(
							contextEnd, 
							null, 
							-1.0, 
							null, 
							0, 
							-1, 
							ThreadLocalRandom.current()
						);
					}
					
					// This computes utilities for all players at the of the playout,
					// which will all be values in [-1.0, 1.0]
					final double[] utilities = RankUtils.utilities(contextEnd);
					
					// Backpropagate utilities through the tree
					while (current != null)
					{
						current.visitCount += 1;
						for (int p = 1; p <= game.players().count(); ++p)
						{
							current.scoreSums[p] += utilities[p];
						}
						current = current.parent;
					}
					
					// Increment iteration counts

					hist.add(nodeIndex);
					this.numIterations += 1;
					this.halvingIterations += 1;
					if(nodeIndex + 1 >= numPossibleMoves){
						nodeIndex = 0;
					}else{
						nodeIndex++;
						currentChild = root.children.get(nodeIndex);
					}


				}
			
		//After children have been explored equally, we halve from the root.
			this.halvingIterations = 0;
			//System.out.println("Halving root");
			//System.out.println("numIterations: " + this.numIterations);
			halveRoot(root);
			numPossibleMoves = root.children.size();
			this.iterPerRound = Double.valueOf(Math.ceil(this.iterPerRound / 2)).intValue();
			if(this.iterPerRound <=0){ this.iterPerRound = 2;}
			//System.out.println("iterperround after halving: " + this.iterPerRound);
			firstRound = false;
		}
		}

		
		// Return the move we wish to play
		System.out.println("VisitCounts\n______________");
		displayHist(hist);
		System.out.println("______________");
		return finalMoveSelection(root);
	}

	public static void halveRoot(Node rootNode){
		int numChildren = rootNode.children.size();
		if(numChildren > 2){
			final int mover = rootNode.context.state().mover();
			double bestValue = Double.NEGATIVE_INFINITY;
			final double twoParentLog = 2.0 * Math.log(Math.max(1, rootNode.visitCount));
			//Make a list sorting each child node by value and then take the best half.

			// A list of lists where the first index of the inner list is the node 
			//index and the second index is the value of that node
			ArrayList<ArrayList<Double>> nodeValues = new ArrayList<>();
			
			for (int i = 0; i < numChildren; ++i) 
			{
				final Node child = rootNode.children.get(i);
				final double exploit = child.scoreSums[mover] / child.visitCount;
				// final double explore = Math.sqrt(twoParentLog / child.visitCount);
				// final double ucb1Value = exploit + explore;
				
				ArrayList<Double> val = new ArrayList<>();

				val.add((double) i);
				val.add(exploit);
				nodeValues.add(val);
				
			}


			//sort descending based on the second index of each inner list:
			nodeValues.sort(Comparator.comparingDouble((ArrayList<Double> list) -> list.get(1)).reversed());

			//System.out.println("nodeValues after sorting descending: " + nodeValues.toString());

			//make a new list which only contains the nodes we want to remove from the tree:
			double halfSizeTemp = Math.ceil(nodeValues.size() / 2);
			int halfSize = Double.valueOf(halfSizeTemp).intValue();
			ArrayList<ArrayList<Double>> lowerHalf = new ArrayList<>(nodeValues.subList(halfSize, nodeValues.size()));

			lowerHalf.sort(Comparator.comparingDouble((ArrayList<Double> list) -> list.get(0)).reversed());//sort based on index in descending order
			//System.out.println("Worst nodes, sorted ascending: " + lowerHalf.toString());
			//Remove the worst nodes from the list, by sorting first, this index based removal should happen in a way that doesn't break./
			for(int i = 0; i < lowerHalf.size();i++){
				rootNode.children.remove(Double.valueOf(lowerHalf.get(i).get(0)).intValue());
			}
		}
		//Keeplist method:

		// List<Node> keepList = new ArrayList<Node>();
		// int[] lowerIndexes = new int[lowerHalf.size()];

		// for(int i = 0;i<lowerHalf.size();i++){
		// 	lowerIndexes[i] = Double.valueOf(lowerHalf.get(i).get(0)).intValue();
		// }
		
		// //Keep the nodes that are not in lowerHalf list
		// for(int i = 0; i < rootNode.children.size(); i++){
		// 	boolean canAdd = true;
		// 	for(int j = 0; j < lowerIndexes.length; j++){
		// 		if(lowerIndexes[j] == i){
		// 			canAdd = false;
		// 		}
		// 	}

		// 	if(canAdd){
		// 		keepList.add(rootNode.children.get(i));
		// 	}
		// }
		

		//Replace the rootNode children list with keeplist
		// rootNode.children = keepList;
		

	}

	public static void displayHist(ArrayList<Integer> hist){
		 
		 // Count occurrences of each integer
		 HashMap<Integer, Integer> counts = new HashMap<>();
		 for (Integer num : hist) {
			 counts.put(num, counts.getOrDefault(num, 0) + 1);
		 }
		 
		 // Display bin counts
		 for (Integer key : counts.keySet()) {
			 System.out.println("Number: " + key + ", Count: " + counts.get(key));
		 }
	}
	
	/**
	 * Selects child of the given "current" node according to UCB1 equation.
	 * This method also implements the "Expansion" phase of MCTS, and creates
	 * a new node if the given current node has unexpanded moves.
	 * 
	 * @param current
	 * @return Selected node (if it has 0 visits, it will be a newly-expanded node).
	 */
	public static Node select(final Node current)
	{
		if (!current.unexpandedMoves.isEmpty())
		{
			// randomly select an unexpanded move
			final Move move = current.unexpandedMoves.remove(
					ThreadLocalRandom.current().nextInt(current.unexpandedMoves.size()));
			
			// create a copy of context
			final Context context = new Context(current.context);
			
			// apply the move
			context.game().apply(context, move);
			
			// create new node and return it
			return new Node(current, move, context);
		}
		
		// use UCB1 equation to select from all children, with random tie-breaking
		Node bestChild = null;
        double bestValue = Double.NEGATIVE_INFINITY;
        final double twoParentLog = 2.0 * Math.log(Math.max(1, current.visitCount));
        int numBestFound = 0;
        
        final int numChildren = current.children.size();
        final int mover = current.context.state().mover();

        for (int i = 0; i < numChildren; ++i) 
        {
        	final Node child = current.children.get(i);
        	final double exploit = child.scoreSums[mover] / child.visitCount;
        	final double explore = Math.sqrt(twoParentLog / child.visitCount);
        
            final double ucb1Value = exploit + explore;
            
            if (ucb1Value > bestValue)
            {
                bestValue = ucb1Value;
                bestChild = child;
                numBestFound = 1;
            }
            else if 
            (
            	ucb1Value == bestValue && 
            	ThreadLocalRandom.current().nextInt() % ++numBestFound == 0
            )
            {
            	// this case implements random tie-breaking
            	bestChild = child;
            }
        }
        
        return bestChild;
	}
	
	/**
	 * Selects the move we wish to play using the "Robust Child" strategy
	 * (meaning that we play the move leading to the child of the root node
	 * with the highest visit count).
	 * 
	 * @param rootNode
	 * @return
	 */
	public static Move finalMoveSelection(final Node rootNode)
	{
		Node bestChild = null;
        int bestVisitCount = Integer.MIN_VALUE;
        int numBestFound = 0;
        
        final int numChildren = rootNode.children.size();

        for (int i = 0; i < numChildren; ++i) 
        {
        	final Node child = rootNode.children.get(i);
        	final int visitCount = child.visitCount;
            
            if (visitCount > bestVisitCount)
            {
                bestVisitCount = visitCount;
                bestChild = child;
                numBestFound = 1;
            }
            else if 
            (
            	visitCount == bestVisitCount && 
            	ThreadLocalRandom.current().nextInt() % ++numBestFound == 0
            )
            {
            	// this case implements random tie-breaking
            	bestChild = child;
            }
        }
        
        return bestChild.moveFromParent;
	}
	
	@Override
	public void initAI(final Game game, final int playerID)
	{
		this.player = playerID;
	}
	
	@Override
	public boolean supportsGame(final Game game)
	{
		if (game.isStochasticGame())
			return false;
		
		if (!game.isAlternatingMoveGame())
			return false;
		
		return true;
	}
	
	//-------------------------------------------------------------------------
	
	/**
	 * Inner class for nodes used by example UCT
	 * 
	 * @author Dennis Soemers
	 */
	private static class Node
	{
		/** Our parent node */
		private final Node parent;
		
		/** The move that led from parent to this node */
		private final Move moveFromParent;
		
		/** This objects contains the game state for this node (this is why we don't support stochastic games) */
		private final Context context;
		
		/** Visit count for this node */
		private int visitCount = 0;
		
		/** For every player, sum of utilities / scores backpropagated through this node */
		private final double[] scoreSums;
		
		/** Child nodes */
		private List<Node> children = new ArrayList<Node>();
		
		/** List of moves for which we did not yet create a child node */
		private final FastArrayList<Move> unexpandedMoves;
		
		/**
		 * Constructor
		 * 
		 * @param parent
		 * @param moveFromParent
		 * @param context
		 */
		public Node(final Node parent, final Move moveFromParent, final Context context)
		{
			this.parent = parent;
			this.moveFromParent = moveFromParent;
			this.context = context;
			final Game game = context.game();
			scoreSums = new double[game.players().count() + 1];
			
			// For simplicity, we just take ALL legal moves. 
			// This means we do not support simultaneous-move games.
			unexpandedMoves = new FastArrayList<Move>(game.moves(context).moves());
			
			if (parent != null)
				parent.children.add(this);
		}
		
	}
	
	//-------------------------------------------------------------------------

}
