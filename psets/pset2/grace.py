class MinimaxAgent(MultiAgentSearchAgent):
    def get_action(self, game_state: GameState) -> Action:
        """*** YOUR CODE HERE ***"""
        _, action = self.max_val(game_state) if self.index == 0 else self.min_val(game_state)
        return action

    def max_val(self, game_state: GameState) -> Tuple[float, Optional[Action]]:
        """
        Given a `GameState` object, this function should return a tuple that contains
         - the maximum value that this agent is able to guarantee against any opponent
         - the action necessary to take from the current state corresponding to the maximum value that is returned
            - if `game_state` is already a terminal state, then this should be `None`.
        """
        """*** YOUR CODE HERE ***"""
        # if terminal
        if game_state.is_terminal():
            return (game_state.value(), None)
        
        # values and action
        v, best_action = float("-inf"), None

        # Iterate through actions
        for action in game_state.get_actions():
            succ_val, _ = self.min_val(game_state.generate_successor(action))
            if succ_val > v:
                v = succ_val
                best_action = action
        
        return (v, best_action)

    def min_val(self, game_state: GameState) -> Tuple[float, Optional[Action]]:
        """
        Given a `GameState` object, this function should return a tuple that contains
         - the minimum value that this agent is able to guarantee against any opponent
         - the action necessary to take from the current state corresponding to the minimum value that is returned
            - if `game_state` is already a terminal state, then this should be `None`.
        """
        "*** YOUR CODE HERE ***"
        """*** YOUR CODE HERE ***"""
        if game_state.is_terminal():
            return (game_state.value(), None)
        
        # values and action
        v, best_action = float("inf"), None

        # Iterate through actions
        for action in game_state.get_actions():
            succ_val, _ = self.max_val(game_state.generate_successor(action))
            if succ_val < v:
                v = succ_val
                best_action = action
        
        return (v, best_action)
    

class AlphaBetaAgent(MultiAgentSearchAgent):
    def get_action(self, game_state: GameState):
        alpha = float("-inf")
        beta = float("inf")
        _, action = self.max_val(game_state, alpha, beta) if self.index == 0 else self.min_val(game_state, alpha, beta)
        return action

    def max_val(self, game_state: GameState, alpha: float, beta: float) -> Tuple[float, Optional[Action]]:
        if game_state.is_terminal():
            return (game_state.value(), None)
        
        # values and action
        v, best_action = float("-inf"), None

        # Iterate through actions
        for action in game_state.get_actions():
            succ_val, _ = self.min_val(game_state.generate_successor(action), alpha, beta)
            if succ_val > v:
                v = succ_val
                best_action = action
            if v == beta:
                return (v, best_action)
            alpha = max(alpha, v)
        
        return (v, best_action)

    def min_val(self, game_state: GameState, alpha: float, beta: float) -> Tuple[float, Optional[Action]]:
        if game_state.is_terminal():
            return (game_state.value(), None)
        
        # values and action
        v, best_action = float("inf"), None

        # Iterate through actions
        for action in game_state.get_actions():
            succ_val, _ = self.max_val(game_state.generate_successor(action), alpha, beta)
            if succ_val < v:
                v = succ_val
                best_action = action
            if v == alpha:
                return (v, best_action)
            beta = min(beta, v)
        
        return (v, best_action)
