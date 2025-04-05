class CustomerAgent:
    def __init__(self):
        self.satisfaction_score = 100

    def update_satisfaction(self, stock_out=False):
        if stock_out:
            self.satisfaction_score -= 10
        else:
            self.satisfaction_score += 1
        return self.satisfaction_score
