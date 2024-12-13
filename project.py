import os
import csv


class PriceMachine:
    def __init__(self):
        self.data = []
        self.result = ''
        self.name_length = 0

    def load_prices(self, file_path):
        '''
            Сканирует указанный каталог. Ищет файлы со словом price в названии.
            В файле ищет столбцы с названием товара, ценой и весом.
        '''
        for filename in os.listdir(file_path):
            if 'price' in filename and filename.endswith('.csv'):
                file_path_dir = os.path.join(file_path, filename)
                with open(file_path_dir, 'r', encoding='utf-8') as csvfile:
                    reader = csv.reader(csvfile, delimiter=',')
                    headers = next(reader)
                    price_idx, name_idx, weight_idx = self._search_product_price_weight(
                        headers)

                    for row in reader:
                        if price_idx is not None and name_idx is not None and weight_idx is not None:
                            product_name = row[name_idx].strip()
                            price = float(row[price_idx].strip())
                            weight = float(row[weight_idx].strip())
                            price_per_kg = price / weight if weight != 0 else 0
                            self.data.append({
                                'name': product_name,
                                'price': price,
                                'weight': weight,
                                'file': filename,
                                'price_per_kg': price_per_kg
                            })

    def _search_product_price_weight(self, headers):
        '''
            Возвращает индексы столбцов
        '''
        name_indices = [i for i, h in enumerate(
            headers) if h in ['название', 'продукт', 'товар', 'наименование']]
        price_indices = [i for i, h in enumerate(
            headers) if h in ['цена', 'розница']]
        weight_indices = [i for i, h in enumerate(
            headers) if h in ['фасовка', 'масса', 'вес']]

        if name_indices and price_indices and weight_indices:
            return price_indices[0], name_indices[0], weight_indices[0]
        return None, None, None

    def export_to_html(self, fname='output.html'):
        result = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Позиции продуктов</title>
        </head>
        <body>
            <table border="1">
                <tr>
                    <th>№</th>
                    <th>Название</th>
                    <th>Цена</th>
                    <th>Фасовка</th>
                    <th>Файл</th>
                    <th>Цена за кг.</th>
                </tr>
        '''
        for idx, item in enumerate(sorted(self.data, key=lambda x: x['price_per_kg'])):
            result += f'''
                <tr>
                    <td>{idx + 1}</td>
                    <td>{item['name']}</td>
                    <td>{item['price']}</td>
                    <td>{item['weight']}</td>
                    <td>{item['file']}</td>
                    <td>{item['price_per_kg']:.2f}</td>
                </tr>
            '''
        result += '''
            </table>
        </body>
        </html>
        '''
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f'Данные успешно экпортированы в {fname}')

    def find_text(self, text):
        '''
            Возвращает список позиций, содержащих текст в названии продукта.
        '''
        return [item for item in self.data if text.lower() in item['name'].lower()]


if __name__ == "__main__":
    pm = PriceMachine()
    pm.load_prices(r'D:\DATA\Documents\GitHub\Lists_price')

    while True:
        search_text = input(
            'Введите текст для поиска товара (или напишите "exit" для выхода): ')
        if search_text.lower() == 'exit':
            print('Работа завершена.')
            break

        results = pm.find_text(search_text)
        if results:
            print(f'Найдено {len(results)} позиций:')
            for idx, item in enumerate(sorted(results, key=lambda x: x['price_per_kg'])):
                print(
                    f'{idx + 1} - {item["name"]}, Цена: {item["price"]}, Вес: {item["weight"]}, Файл: {item["file"]}, Цена за кг.: {item["price_per_kg"]:.2f}')
        else:
            print('Не найдено ни одной позиции.')

    pm.export_to_html('output.html')
