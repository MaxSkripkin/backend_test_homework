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
    M_IN_KM = 1000  # Константа для перевода значений из метров в километры
    LEN_STEP = 0.65  # Расстояние в шагах

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
        pass

    def show_training_info(self) -> InfoMessage:
        """Сообщения о результатах тренировки"""
        return InfoMessage(self.__class__.__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    def __init__(self, action, duration, weight) -> None:
        """Инициализация атрибутов класса родителя"""
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Возвращает количество калорий за бег"""
        # coeff_calorie_1 = 18
        # coeff_calorie_2 = 20
        return (18 * self.get_mean_speed()
                - 20) * self.weight / self.M_IN_KM * (self.duration * 60)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self, action, duration, weight, height) -> None:
        """Инициализация атрибутов класса родителя"""
        super().__init__(action, duration, weight)
        self.height = height  # Доп параметр - рост

    def get_spent_calories(self):
        """Возвращает количество калорий за спорт ходьбу"""
        return (0.035 * self.weight
                + (self.get_mean_speed() ** 2 // self.height)
                * 0.029 * self.weight) * self.duration * 60


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38

    def __init__(self, action, duration, weight,
                 length_pool, count_pool) -> None:
        """Инициализация атрибутов класса родителя"""
        super().__init__(action, duration, weight)
        self.length_pool = length_pool  # Длина бассейна
        self.count_pool = count_pool   # Сколько раз переплыл(а) бассейн

    def get_mean_speed(self) -> float:
        """Рассчитываем среднюю скорость"""
        return self.length_pool * self.count_pool / 1000 / self.duration

    def get_spent_calories(self) -> float:
        """Метод вернёт кол-во калорий"""
        return (self.get_mean_speed() + 1.1) * 2 * self.weight


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type == 'SWM':
        return Swimming(* data)
    elif workout_type == 'RUN':
        return Running(* data)
    elif workout_type == 'WLK':
        return SportsWalking(* data)
    else:
        return None


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