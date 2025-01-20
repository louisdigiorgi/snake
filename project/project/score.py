class Score :
    """Define the score with a name and a score (int)."""

    MAX_LENGTH = 8


    def __init__(self, score : int, name : str) -> None:
        """Initialize."""
        self._score=score
        self.name=name #use the property 

    @property
    def name(self) -> str :
        """Return the name."""
        return self._name

    @name.setter
    def name(self, n : str) -> None :
        """Modify the name."""
        self._name=n[:self.MAX_LENGTH]



    @property 
    def score(self) -> int :
        """Return the score."""
        return self._score

    
    # Implemente the comparaison operators to use the function sort in the lists
    def __gt__(self, other : object) -> bool :
        """Define the comparaison operator."""
        return isinstance(other, Score) and self._score > other._score

    def __lt__(self, other : object) -> bool :
        """Define the comparaison operator."""
        return isinstance(other, Score) and self._score < other._score

    def __eq__(self, other : object) -> bool :
        """Define the comparaison operator."""
        return isinstance(other, Score) and self._score == other._score

    def __ge__(self, other : object) -> bool :
        """Define the comparaison operator."""
        return isinstance(other, Score) and self._score >= other._score

    def __le__(self, other : object) -> bool :
        """Define the comparaison operator."""
        return isinstance(other, Score) and self._score <= other._score

    def __ne__(self, other : object) -> bool :
        """Define the comparaison operator."""
        return isinstance(other, Score) and self._score != other._score

    def __repr__(self) -> str:
        """Representation."""
        return f"Score(name={self._name}, score={self._score})"