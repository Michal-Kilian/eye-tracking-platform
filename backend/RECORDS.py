import uuid
from enum import Enum

import ndjson


class RecordType(Enum):
    def __str__(self):
        return str(self.value)

    OFFLINE = "Offline"
    REAL_TIME = "Real-Time"


class Record:
    id: uuid.UUID
    timestamp: float
    type: RecordType
    raw_data: list[dict]


def get_records() -> list[Record]:
    with open('backend/RECORDS.ndjson') as f:
        data = ndjson.load(f)
        records = []
        for item in data:
            record = Record()
            record.id = item["id"]
            record.timestamp = item["timestamp"]
            record.type = RecordType(item["type"])
            record.raw_data = item["raw_data"]
            records.append(record)
    return records


def get_record_from_id(record_id) -> Record:
    for record in RECORDS:
        if record.id == record_id:
            return record


def sorted_records() -> list[Record]:
    return sorted(RECORDS, key=lambda x: x.timestamp, reverse=True)


def append_record(new_record: Record) -> None:
    with open('backend/RECORDS.ndjson') as f:
        records = ndjson.load(f)
        records.append({
            "id": str(new_record.id),
            "timestamp": new_record.timestamp,
            "type": new_record.type.value,
            "raw_data": new_record.raw_data
        })

        RECORDS.append(new_record)

        with open("backend/RECORDS.ndjson", "w") as file:
            ndjson.dump(records, file)


def clear_records_file() -> None:
    open('backend/RECORDS.ndjson', 'w').close()


clear_records_file()


RECORDS: list[Record] = get_records()
