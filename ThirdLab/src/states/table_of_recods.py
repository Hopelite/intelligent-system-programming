import json
import os

class TableRecord:
    def __init__(self, name: str, score: int) -> None:
        self.name = name
        self.score = score

class TableOfRecords:
    def __init__(self) -> None:
        file_path = os.path.join(os.path.dirname(__file__), "records.json")
        self.__reader = JsonReader(file_path)
        self.__writer = JsonWriter(file_path)

    def get_records(self) -> list[TableRecord]:
        return self.__reader.read()[0:10]

    def save_record(self, new_record: TableRecord) -> None:
        records = self.__reader.read()
        records.sort(key=lambda x: x.score, reverse=True)
        index = 0
        for record in records:
            if record.score < new_record.score:
                break
            index += 1

        records.insert(index, new_record)

        self.__writer.write(records)

class JsonReader:
    def __init__(self, path: str) -> None:
        self.__path = path

    def read(self) -> list[TableRecord]:
        records = []
        with open(self.__path, 'r') as file:
            data = json.load(file)

            for record in data:
                records.append(TableRecord(record['name'], int(record['score'])))

        return records

class JsonWriter:
    def __init__(self, path: str) -> None:
        self.__path = path

    def write(self, records: list[TableRecord]) -> None:
        json_records = json.dumps([ob.__dict__ for ob in records], indent=4)
        
        with open(self.__path, 'w') as file:
            file.write(json_records)