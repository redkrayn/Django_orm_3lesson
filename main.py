import os
import random
import django
import argparse

os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'
django.setup()

from datacenter.models import Schoolkid, Mark, Lesson, Commendation, Chastisement, Subject


PRAISE = [
    'Молодец!', 'Отлично!', 'Хорошо!', 'Гораздо лучше, чем я ожидал!', 'Ты меня приятно удивил!',
    'Великолепно!', 'Прекрасно!', 'Ты меня очень обрадовал!', 'Именно этого я давно ждал от тебя!',
    'Сказано здорово – просто и ясно!', 'Ты, как всегда, точен!', 'Очень хороший ответ!', 'Талантливо!',
    'Ты сегодня прыгнул выше головы!', 'Я поражен!', 'Уже существенно лучше!', 'Потрясающе!',
    'Замечательно!', 'Прекрасное начало!', 'Так держать!', 'Ты на верном пути!', 'Здорово!',
    'Это как раз то, что нужно!', 'Я тобой горжусь!', 'С каждым разом у тебя получается всё лучше!',
    'Мы с тобой не зря поработали!', 'Я вижу, как ты стараешься!', 'Ты растешь над собой!',
    'Ты многое сделал, я это вижу!', 'Теперь у тебя точно все получится!'
]


def get_schoolkid(schoolkid):
    schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid, year_of_study=6, group_letter='А')
    return schoolkid


def fix_marks(schoolkid):
    Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3]).update(points=5)


def delete_chastisement(schoolkid):
    chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    chastisements.delete()


def create_commendation(schoolkid, subject):
    subject = Subject.objects.get(title=subject, year_of_study=6)
    lesson = Lesson.objects.filter(year_of_study=6, group_letter='А', subject=subject).order_by('?').first()
    if lesson is None:
        exit('Такого урока в расписании нет, попробуйте ещё раз')
    text = random.choice(PRAISE)
    Commendation.objects.create(
        text=text,
        created=lesson.date,
        schoolkid=schoolkid,
        subject=lesson.subject,
        teacher=lesson.teacher
    )
    print("Оценки исправлены, замечания удалены, похвала добавлена")


def main():
    parser = argparse.ArgumentParser(description='Введите имя и предмет')
    parser.add_argument('name', help='Введите имя')
    parser.add_argument('subject', help='Введите предмет')
    args = parser.parse_args()
    schoolkid = args.name.title()
    subject = args.subject.title()

    try:
        schoolkid = get_schoolkid(schoolkid)
        fix_marks(schoolkid)
        delete_chastisement(schoolkid)
        create_commendation(schoolkid, subject)
    except Schoolkid.DoesNotExist:
        exit('Не верный ввод, такой фамилии нет, попробуйте ещё раз')
    except Subject.DoesNotExist:
        exit('Не верный ввод, такого предмета нет, попробуйте ещё раз')
    except Schoolkid.MultipleObjectsReturned:
        exit('Людей с такими именами несколько, введите фамилию и имя ученика через пробел')


if __name__ == '__main__':
    main()
