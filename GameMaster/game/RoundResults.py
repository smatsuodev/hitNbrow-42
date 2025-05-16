from player.PlayerNumber import PlayerNumber


class RoundResults:
    def __init__(self):
        self.results = []

    def append_result(self, winner: PlayerNumber, p1_ap, p2_ap):
        self.results.append((winner, p1_ap, p2_ap))

    def get_winner(self) -> PlayerNumber | None:
        p1_win = len([r for r in self.results if r[0] == PlayerNumber.Player1])
        p2_win = len([r for r in self.results if r[0] == PlayerNumber.Player2])
        if p1_win > p2_win:
            return PlayerNumber.Player1
        elif p1_win < p2_win:
            return PlayerNumber.Player2

        p1_total_ap = sum([r[1] for r in self.results])
        p2_total_ap = sum([r[2] for r in self.results])
        if p1_total_ap < p2_total_ap:
            return PlayerNumber.Player1
        elif p1_total_ap > p2_total_ap:
            return PlayerNumber.Player2

        p1_win_diff_ap = sum(r[1] - r[2] for r in self.results)
        p2_win_diff_ap = sum(r[2] - r[1] for r in self.results)
        if p1_win_diff_ap < p2_win_diff_ap:
            return PlayerNumber.Player1
        elif p1_win_diff_ap > p2_win_diff_ap:
            return PlayerNumber.Player2

    def print_results(self, p1_name: str, p2_name: str):
        print(f"player1:\t{p1_name}\tplayer2:\t{p2_name}")
        for idx, result in enumerate(self.results):
            print(f"round\t{idx+1}\twinner:\t{p1_name if result[0] == PlayerNumber.Player1 else p2_name}\t"
                  f"{p1_name} used ap:\t{result[1]}\t{p2_name} used ap:\t{result[2]}")
