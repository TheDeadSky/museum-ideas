from aiogram.fsm.scene import Scene


class StartScene(Scene, reset_data_on_enter=True, reset_history_on_enter=True, callback_query_without_state=True):
    pass
