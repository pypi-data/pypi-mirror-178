from kepingai import KepingApi


class Strategy:
    def __init__(self, strategy_id: str, api: KepingApi):
        self.api = api
        self.strategy_id = strategy_id

    def open_signal(self,
                    signal_params: dict):
        signal_params.update({"strategy_id": self.strategy_id,
                              "action": "open"})
        return self.api.post(data=signal_params, tag="strategy/publish-signal")

    def close_signal(self,
                     signal_params: dict):
        signal_params.update({"strategy_id": self.strategy_id,
                              "action": "closed"})
        return self.api.post(data=signal_params, tag="strategy/publish-signal")

    def get_active_signals(self):
        params = {"strategy_id": self.strategy_id}
        return self.api.get(params=params, tag="strategy/active-signals")
