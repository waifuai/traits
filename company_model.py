from personality import Personality

class Company:
    def __init__(self, name: str):
        self.name = name

    def _calculate_distance(self, p1: Personality, p2: Personality) -> float:
        return ((p1.friendliness - p2.friendliness) ** 2 + (p1.dominance - p2.dominance) ** 2) ** 0.5

    def _analyze_description(self, description: str) -> dict:
        words = description.lower().split()
        trait_weights = {}
        for word in words:
            trait_weights[word] = 1.0 # Default weight
        return trait_weights

    def _weighted_average(self, traits: dict, weights: dict) -> Personality:
        avg_friendliness = 0
        avg_dominance = 0
        total_weight = sum(weights.values())
        if total_weight == 0:
            return Personality(0, 0)

        for trait_name, personality in traits.items():
            weight = weights.get(trait_name, 0)
            avg_friendliness += personality.friendliness * weight
            avg_dominance += personality.dominance * weight

        return Personality(
            friendliness=avg_friendliness / total_weight if total_weight else 0,
            dominance=avg_dominance / total_weight if total_weight else 0
        )