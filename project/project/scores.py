import yaml
from .score import Score
import typing

class Scores:
    """Contains instances of scores and handles persistence with a YAML file."""

    def __init__(self, max_scores: int, scores: list[Score]) -> None:
        """Initialize the scores."""
        self._max_scores = max_scores
        # Sort the scores in descending order to keep the highest first
        self._scores = sorted(scores, reverse=True)[:max_scores]

    def __iter__(self) -> typing.Iterator[Score]:
        """Iterate over the list of scores."""
        return iter(self._scores)

    def is_highscore(self, score_player: int) -> bool:
        """Check if a player's score qualifies as a high score."""
        return len(self._scores) < self._max_scores or score_player > self._scores[-1].score

    def add_score(self, score_player: Score) -> None:
        """Add a new score or update the existing one."""
        # Check if the player already exists in the scores
        existing_player = next((s for s in self._scores if s.name == score_player.name), None)
        if existing_player:
            # Update the score if the new score is higher
            if score_player.score > existing_player.score:
                existing_player._score = score_player.score  # Update the score
                self._scores.sort(reverse=True)  # Re-sort the scores
                self.save()  # Save changes to the file
        else:
            # Add a new score if it's a high score
            if self.is_highscore(score_player.score):
                if len(self._scores) >= self._max_scores:
                    self._scores.pop()  # Remove the lowest score if the list is full
                self._scores.append(score_player)
                self._scores.sort(reverse=True)
                self.save()  # Save changes to the file

    @staticmethod
    def load(filename: str = "high_scores.yaml") -> "Scores":
        """Load scores from a YAML file or create a file with default scores if it doesn't exist."""
        try:
            with open(filename, "r") as f:
                data = yaml.safe_load(f)
                if not data or 'scores' not in data:  # If the file is empty or malformed
                    print("No valid scores found in file, creating a new file with default scores.")  # Debug
                    return Scores.default(max_scores=5)
                max_scores = data.get("max_scores", 5)
                scores = [
                    Score(score=item["score"], name=item["name"])
                    for item in data.get("scores", [])
                ]
                return Scores(max_scores, scores)
        except FileNotFoundError:
            print(f"File {filename} not found, creating a new file with default scores.")  # Debug
            return Scores.default(max_scores=5)

    @staticmethod
    def default(max_scores: int) -> "Scores":
        """Return a default instance with predefined scores."""
        return Scores(
            max_scores,
            [
                Score(score=-1, name="Joe"),
                Score(score=8, name="Jack"),
                Score(score=0, name="Averell"),
                Score(score=6, name="William"),
            ],
        )

    def save(self, filename: str = "high_scores.yaml") -> None:
        """Save the current scores to a YAML file."""
        print("Saving scores to file...")  # Debug
        data = {
            "max_scores": self._max_scores,
            "scores": [{"name": s.name, "score": s.score} for s in self._scores],
        }
        with open(filename, "w") as f:
            yaml.dump(data, f)
            print(f"Scores saved to {filename}.")  # Debug
