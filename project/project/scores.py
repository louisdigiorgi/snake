import typing

from .score import Score


class Scores :
    """Contains instances of scores."""

    def __init__(self, max_scores : int, scores : list[Score]) -> None :
        """Define the scores."""
        self._max_scores=max_scores
        self._scores=sorted(scores, reverse = True)[:max_scores]

    @classmethod
    def default(cls, max_scores : int ) -> "Scores" :
        """Classmethod."""
        return cls(max_scores, [Score (score=-1, name="Joe"), Score(score=8, name="Jack"), Score(score=0,name="Averell"), Score(score=6, name="William")])

    def __iter__(self) -> typing.Iterator[Score]:
        """Iterate on the list of scores."""
        return iter(self._scores)


    def is_highscore(self, score_player : int) -> bool :
        """Define the case highscore."""
        return len(self._scores)<self._max_scores or score_player > self._scores[-1]

    def add_score(self, score_player: Score) -> None:
        """Add a score and sort the list."""
        if self.is_highscore(score_player.score):
            if len(self._scores)>=self._max_scores :
                self._scores.pop()
            self._scores.append(score_player)
            self._scores.sort(reverse=True)


























