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
        return {'match_list': self.format_match_list(),
                'start_time': self.start_time,
                'end_time': self.end_time}

    def format_match_list(self):
        """
        format player object in match list so it can be stored in db
        :return: match list with serialized player object inside
        """
        for m in self.match_list:
            m[0][0] = m[0][0].last_name
            m[1][0] = m[1][0].last_name
        return self.match_list
