from utils.data import data

# Массив предметов для отображения
subjects = {
    f"subject_{i}": name for i, name in enumerate(
        [
            "Русский язык", "Иностранный язык", "Информатика",
            "История", "Литература", "Математика",
            "Обществознание", "Биология", "Физика",
            "Химия", "География"
        ], 1
    )
}


def get_speciality(user_data: dict):
    selected_keys = [int(key.replace('subject_', '')) for key, selected in user_data['buttons_state'].items() if selected]
    if selected_keys:
        match_specialities = []
        for key in data:
            if set(key).issubset(set(selected_keys)):
                match_specialities.append(data[key])

        grouped = {}
        for institute_data in match_specialities:
            for institute, specialities in institute_data.items():
                if institute not in grouped:
                    grouped[institute] = {}
                for speciality, directions in specialities.items():
                    if speciality not in grouped[institute]:
                        grouped[institute][speciality] = []
                    for direction in directions:
                        grouped[institute][speciality].append(direction)

        result = []
        for institute, specialities in sorted(grouped.items()):
            specialities_str = []
            for speciality, directions in sorted(specialities.items()):
                directions_str = '\n'.join([f'    — {direction}' for direction in directions])
                if directions_str:
                    specialities_str.append(f"{speciality}:\n{directions_str}")
                else:
                    specialities_str.append(speciality)
            result.append(f"<b>{institute}</b>"
                          f"<blockquote>{'\n\n'.join(specialities_str)}</blockquote>")

        return "\n\n".join(result)
    return
