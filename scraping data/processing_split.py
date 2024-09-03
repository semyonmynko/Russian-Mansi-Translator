def processing_split(translation):
    # Обрезать по I II III
    translation = translation.replace('X. ', '$')
    translation = translation.replace('IX. ', '$')
    translation = translation.replace('VIII. ', '$')
    translation = translation.replace('VII. ', '$')
    translation = translation.replace('VI. ', '$')
    translation = translation.replace('V. ', '$')
    translation = translation.replace('IV. ', '$')
    translation = translation.replace('III. ', '$')
    translation = translation.replace('II. ', '$')
    translation = translation.replace('I. ', '$')

    # Обрезать по 1) 2) 3)
    for i in range(10, 0, -1):
        translation = translation.replace(f'{i}) ', '$')

    # Обрезать по 1. 2. 3.
    for i in range(10, 0, -1):
        translation = translation.replace(f'{i}. ', '$')

    # Обрезать ; ,
    translation = translation.replace(', ', '$')
    translation = translation.replace('; ', '$')

    # Сократить $
    translation = translation.replace('$$$$$', '$')
    translation = translation.replace('$$$$', '$')
    translation = translation.replace('$$$', '$')
    translation = translation.replace('$$', '$')

    # Split $
    translation = translation.split('$')

    translation_result = []
    for i in range(0, len(translation)):
        if translation[i] == '':
            continue
        else:
            translation_result.append(translation[i])
        translation_result[-1] = translation[i].split(' (')
        translation_result[-1][-1] = translation_result[-1][-1].replace(')', '')
        if len(translation_result[-1]) == 1:
            translation_result[-1].append(None)

    return translation_result