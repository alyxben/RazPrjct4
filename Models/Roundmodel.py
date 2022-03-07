from datetime import datetime



class Round:
    def __init__(self, match_list, start_time, end_time=False):
        self.match_list = match_list
        self.start_time = start_time
        self.end_time = end_time

    def __repr__(self):
        if not self.end_time:
            return f"A débuté le: {self.start_time}\n" \
                    f"Les duels pour ce round sont: {self.match_list}\n"
        else:
            return f"A débuté le: {self.start_time}\n" \
                   f"Les matchs de ce round sont: {self.match_list}\n" \
                   f"Le round a été clôturé le: {self.end_time}\n"

    def serialize_round_info(self):
        self.end_time = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        return {'match_list': self.serialize_match_list(),
                'start_time': self.start_time,
                'end_time': self.end_time}

    def serialize_match_list(self):
        for m in self.match_list:
            m[0][0] = m[0][0].serialize_player_info()
            m[1][0] = m[1][0].serialize_player_info()
        return self.match_list

