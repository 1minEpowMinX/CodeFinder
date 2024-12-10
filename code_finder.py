import os
import sys
import xml.etree.ElementTree as ET


def load_target_codes(file_path):
    """
    Загружает список целевых ContractCode из текстового файла.

    :param file_path: Путь к файлу со списком кодов.
    :return: Множество целевых кодов.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return set(line.strip() for line in f if line.strip())
    except FileNotFoundError:
        print(f"Файл {file_path} не найден. Проверьте путь.")
        return set()


def process_xml_files_recursively(directory, target_code, results_file):
    """
    Рекурсивно обрабатывает все XML-файлы в указанной директории и подкаталогах,
    ищет элементы <ContractCode>, указанные в списке, и сохраняет найденные результаты в файл.

    :param directory: Путь к директории с XML-файлами.
    :param target_code: Целевой код для поиска.
    :param results_file: Путь к файлу для сохранения результатов.
    """
    with open(results_file, 'a', encoding='utf-8') as result_f:
        for root_dir, _, files in os.walk(directory):  # Рекурсивный обход
            for filename in files:
                if filename.lower().endswith(".xml"):  # Только XML файлы
                    filepath = os.path.join(root_dir, filename)
                    try:
                        # Парсинг XML-файла
                        tree = ET.parse(filepath)
                        root = tree.getroot()

                        # Извлечение пространства имен
                        namespace = {'ns': root.tag.split('}')[0].strip(
                            '{')}  # Получение xmlns

                        # Поиск всех элементов <ContractCode>
                        contract_codes = root.findall(
                            './/ns:ContractCode', namespace)
                        for code_element in contract_codes:
                            contract_code = code_element.text.strip()
                            if contract_code == target_code:
                                # Запись найденного результата в файл
                                result_line = f"Файл: {
                                    filepath}, ContractCode найден: {contract_code}\n"
                                result_f.write(result_line)
                                print(result_line.strip())

                    except ET.ParseError as e:
                        print(f"Ошибка при обработке файла {filepath}: {e}")
                    except Exception as e:
                        print(f"Непредвиденная ошибка с файлом {
                              filepath}: {e}")


def main():
    """ Основная функция программы. """
    # Определение директории, где находится текущий исполняемый файл
    if getattr(sys, 'frozen', False):  # Проверка, если скрипт заморожен в exe
        script_dir = os.path.dirname(sys.executable)
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))

    # Пути к папке, файлу с кодами и файлу для результатов
    directory = script_dir
    codes_file = os.path.join(script_dir, "codes_file.txt")
    results_file = os.path.join(script_dir, "results.txt")

    # Очистка или создание файла результатов
    open(results_file, 'w').close()

    # Проверка существования файла с кодами
    if not os.path.exists(codes_file):
        print(f"Файл с кодами не найден: {codes_file}")
        print("Пожалуйста, проверьте, что файл существует.")
        return

    # Загрузка целевых кодов
    target_codes = load_target_codes(codes_file)

    if target_codes:
        for target_code in target_codes:
            process_xml_files_recursively(directory, target_code, results_file)
        print(f"Результаты сохранены в файл: {results_file}")
    else:
        print("Список целевых кодов пуст.")


if __name__ == "__main__":
    main()
