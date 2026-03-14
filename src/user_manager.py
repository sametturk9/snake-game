import json
import os

USERS_FILE = "users.json"

class UserManager:
    def __init__(self):
        self.users = self._load_users()
        self.current_user = None

    def _load_users(self):
        if os.path.exists(USERS_FILE):
            try:
                with open(USERS_FILE, "r") as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def _save_users(self):
        with open(USERS_FILE, "w") as f:
            json.dump(self.users, f, indent=2)

    def register(self, username):
        for user_id, user_data in self.users.items():
            if user_data.get("username") == username:
                return False, "Bu kullanıcı adı zaten kullanılıyor"

        user_id = username.lower()
        self.users[user_id] = {
            "username": username,
            "scores": []
        }
        self._save_users()
        return True, username

    def login(self, username):
        user_id = username.lower()
        if user_id in self.users:
            self.current_user = user_id
            return True, self.users[user_id]["username"]
        return False, "Kullanıcı bulunamadı"

    def logout(self):
        self.current_user = None

    def add_score(self, score):
        if self.current_user and self.current_user in self.users:
            self.users[self.current_user]["scores"].append(score)
            self.users[self.current_user]["scores"].sort(reverse=True)
            if len(self.users[self.current_user]["scores"]) > 10:
                self.users[self.current_user]["scores"] = self.users[self.current_user]["scores"][:10]
            self._save_users()
            return True
        return False

    def get_scores(self):
        if self.current_user and self.current_user in self.users:
            return self.users[self.current_user].get("scores", [])
        return []

    def get_high_score(self):
        if self.current_user and self.current_user in self.users:
            scores = self.users[self.current_user].get("scores", [])
            return scores[0] if scores else 0
        return 0

    def get_global_high_scores(self):
        all_scores = []
        for user_id, user_data in self.users.items():
            if user_data.get("scores"):
                all_scores.append({
                    "username": user_data["username"],
                    "high_score": user_data["scores"][0]
                })
        
        all_scores.sort(key=lambda x: x["high_score"], reverse=True)
        return all_scores[:10]