class VoteManager:

    def __init__(self):
        # { assembly_id: { motion_id: { user_id: vote } } }
        self.votes = {}

        # { assembly_id: { motion_id: status } }
        self.motion_status = {}

    # =========================
    # 🟢 INICIAR MOCIÓN
    # =========================
    def start_motion(self, assembly_id, motion_id):

        if assembly_id not in self.motion_status:
            self.motion_status[assembly_id] = {}

        # ❗ evitar reiniciar si ya existe
        if motion_id in self.motion_status[assembly_id]:
            return False

        self.motion_status[assembly_id][motion_id] = "OPEN"

        if assembly_id not in self.votes:
            self.votes[assembly_id] = {}

        self.votes[assembly_id][motion_id] = {}

        return True

    # =========================
    # 🔴 CERRAR MOCIÓN
    # =========================
    def close_motion(self, assembly_id, motion_id):

        if assembly_id not in self.motion_status:
            return False

        if motion_id not in self.motion_status[assembly_id]:
            return False

        self.motion_status[assembly_id][motion_id] = "CLOSED"
        return True

    # =========================
    # 🔍 ESTADO
    # =========================
    def is_open(self, assembly_id, motion_id):
        return self.motion_status.get(assembly_id, {}).get(motion_id) == "OPEN"

    # =========================
    # 🚫 YA VOTÓ
    # =========================
    def has_voted(self, assembly_id, motion_id, user_id):
        return str(user_id) in self.votes.get(assembly_id, {}).get(motion_id, {})

    # =========================
    # 🗳️ REGISTRAR VOTO
    # =========================
    def register_vote(self, assembly_id, motion_id, user_id, vote):

        if not self.is_open(assembly_id, motion_id):
            return False

        if self.has_voted(assembly_id, motion_id, user_id):
            return False

        self.votes[assembly_id][motion_id][str(user_id)] = vote
        return True

    # =========================
    # 📊 RESULTADOS
    # =========================
    def get_results(self, assembly_id, motion_id):

        results = {
            "YES": 0,
            "NO": 0,
            "ABSTAIN": 0,
            "TOTAL": 0
        }

        votes = self.votes.get(assembly_id, {}).get(motion_id, {})

        for v in votes.values():
            if v in ["YES", "NO", "ABSTAIN"]:
                results[v] += 1
                results["TOTAL"] += 1

        return results