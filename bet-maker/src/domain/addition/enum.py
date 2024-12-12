from enum import Enum


class ResultEnum(str, Enum):
    ongoing = "незавершённое"
    win = "Cтавка выиграла"
    lose = "Ставка проиграла"


class EventStatus(str, Enum):
    ongoing = "незавершённое"
    team1_win = "завершено выигрышем первой команды"
    team2_win = "завершено выигрышем второй команды"


STATUS_TO_RESULT = {
    EventStatus.team1_win: ResultEnum.win,
    EventStatus.team2_win: ResultEnum.lose,
}
