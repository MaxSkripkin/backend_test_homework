from typing import Dict, List, Type


class InfoMessage:
    """Информационное сообщение о тренировке"""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Информация о проделанной тренировке"""
        return(f'Тип тренировки: {self.training_type};'
               f' Длительность: {self.duration:.3f} ч.;'
               f' Дистанция: {self.distance:.3f} км;'
               f' Ср. скорость: {self.speed:.3f} км/ч;'
               f' Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    COEFF_CALORIE_1: int = 18
    COEFF_CALORIE_2: int = 20
    TIME_M: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Метод еще не реализован.')

    def show_training_info(self) -> InfoMessage:
        """Сообщения о результатах тренировки"""
        return InfoMessage(self.__class__.__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        """Возвращает количество калорий за бег"""
        return (self.COEFF_CALORIE_1 * self.get_mean_speed()
                - self.COEFF_CALORIE_2) * self.weight / self.M_IN_KM * (
                    self.duration * self.TIME_M)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEF_CAL_WALK_1: float
    COEF_CAL_WALK_1 = 0.035
    COEF_CAL_WALK_2: float
    COEF_CAL_WALK_2 = 0.029

    def __init__(self, action, duration, weight, height) -> None:
        """Инициализация атрибутов класса родителя"""
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self):
        """Возвращает количество калорий за спорт ходьбу"""
        return (self.COEF_CAL_WALK_1 * self.weight
                + (self.get_mean_speed() ** 2 // self.height)
                * self.COEF_CAL_WALK_2 * self.weight
                ) * self.duration * self.TIME_M


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float
    LEN_STEP = 1.38
    CAL_SWIM_1: float
    CAL_SWIM_1 = 1.1
    CAL_SWIM_2: int
    CAL_SWIM_2 = 2

    def __init__(self, action, duration, weight,
                 length_pool, count_pool) -> None:
        """Инициализация атрибутов класса родителя"""
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Рассчитываем среднюю скорость"""
        return (
            self.length_pool * self.count_pool
            / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Метод вернёт кол-во калорий"""
        return (self.get_mean_speed() + self.CAL_SWIM_1
                ) * self.CAL_SWIM_2 * self.weight


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    return workout[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    message = info.get_message()
    print(message)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
